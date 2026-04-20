from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
import json
import re

from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.services.retrieval_service import retrieve_vendor_context, build_context_block
from app.services.order_service import create_order_from_chat
from app.agent.policies import is_within_business_hours, resolve_tone_instruction
from app.agent.prompts import build_sales_agent_system_prompt
from app.schemas.chat_schema import PurchaseContext, CartItem


def get_vendor_settings(db: Session, vendor_id: int) -> VendorSettings | None:
    return db.query(VendorSettings).filter(VendorSettings.vendor_id == vendor_id).first()


def _build_enhanced_query(user_message: str, history: Optional[List[dict]] = None) -> str:
    """
    Si hay historial conversacional, agrega el contexto anterior 
    para mejorar la búsqueda de similitud.
    """
    if not history or len(history) == 0:
        return user_message
    
    # Extrae el último mensaje del agente para contexto
    # Esto ayuda a mantener el tema de conversación
    context_parts = [user_message]
    
    for msg in reversed(history[-4:]):  # Toma últimos 4 mensajes
        if msg.get("role") == "user":
            context_parts.insert(0, msg.get("content", ""))
            break  # Solo el último mensaje del usuario anterior
    
    # Combina para crear una query más contextual
    return " ".join(context_parts)


def _detect_purchase_keywords(text: str) -> bool:
    """Detecta palabras clave de intención de compra."""
    purchase_keywords = [
        r"\bquiero\b",
        r"\bme interesa\b",
        r"\bme lo envíen\b",
        r"\bacéptalo\b",
        r"\bconfirmo\b",
        r"\bcuánto cuesta\b",
        r"\bcómo pago\b",
        r"\bde acuerdo\b",
        r"\bsí, dale\b",
        r"\bperfecto\b",
        r"\besto es\b",
        r"\bfinalizar\b",
        r"\bcomprar\b",
    ]
    
    text_lower = text.lower()
    for keyword in purchase_keywords:
        if re.search(keyword, text_lower):
            return True
    return False


def _create_order_from_response(
    db: Session,
    vendor: Vendor,
    agent_response: str,
    purchase_context: Optional[PurchaseContext]
) -> Optional[dict]:
    """
    Intenta crear una orden si el contexto está completo y el cliente confirmó.
    """
    if not purchase_context:
        return None
    
    # Verifica que tenga datos del cliente
    if not purchase_context.customer_name or not purchase_context.customer_phone:
        return None
    
    # Verifica que haya items
    if not purchase_context.items or len(purchase_context.items) == 0:
        return None
    
    # Verifica que el agente haya confirmado la orden
    confirm_keywords = [
        "registré tu orden",
        "registrar tu orden",
        "orden registrada",
        "procesará tu orden",
        "gracias por comprar",
        "¡excelente!",
    ]
    
    response_lower = agent_response.lower()
    if not any(kw in response_lower for kw in confirm_keywords):
        return None
    
    # Crea la orden
    try:
        items_data = [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in purchase_context.items
        ]
        
        order = create_order_from_chat(
            db=db,
            vendor=vendor,
            customer_name=purchase_context.customer_name,
            customer_phone=purchase_context.customer_phone,
            customer_address=purchase_context.customer_address or "",
            items=items_data,
            conversation_summary="Creada desde chat del agente"
        )
        
        return order
    except Exception as e:
        print(f"Error al crear orden: {str(e)}")
        return None


def generate_agent_reply(
    db: Session,
    vendor: Vendor,
    user_message: str,
    conversation_history: Optional[List[dict]] = None,
    purchase_context: Optional[dict] = None,
    top_k: int = 3
) -> dict:
    """
    Orquesta todo el flujo del agente:
    settings -> horario -> retrieval mejorado -> prompt -> LLM -> respuesta -> posible creación de orden
    """
    settings = get_vendor_settings(db=db, vendor_id=vendor.id)

    # Configuración por defecto si no existe
    agent_enabled = True
    business_start_hour = None
    business_end_hour = None
    off_hours_message = (
        "Hola, en este momento estamos fuera de horario de atención. "
        "Déjanos tu mensaje y te responderemos pronto."
    )
    tone = "friendly"

    if settings:
        agent_enabled = settings.agent_enabled
        business_start_hour = settings.business_start_hour
        business_end_hour = settings.business_end_hour
        off_hours_message = settings.off_hours_message or off_hours_message
        tone = settings.tone or tone

    if not agent_enabled:
        raise HTTPException(status_code=403, detail="El agente de esta empresa está desactivado.")

    if not is_within_business_hours(business_start_hour, business_end_hour):
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": off_hours_message,
            "context_used": "Fuera de horario. No se utilizó contexto del catálogo.",
            "matches_found": 0,
        }

    # Mejora la query si hay historial para mejor contexto
    enhanced_query = _build_enhanced_query(user_message, conversation_history)

    retrieval_result = retrieve_vendor_context(
        vendor=vendor,
        query=enhanced_query,
        top_k=top_k
    )

    results = retrieval_result["results"]
    context_block = build_context_block(results)
    tone_instruction = resolve_tone_instruction(tone)

    system_prompt = build_sales_agent_system_prompt(
        vendor_name=vendor.name,
        tone_instruction=tone_instruction,
        context_block=context_block
    )

    adapter = OpenAIAdapter()
    agent_reply = adapter.generate_reply(
        system_prompt=system_prompt,
        user_message=user_message
    )

    # Convertir purchase_context a objeto si viene como dict
    pc_obj = None
    if purchase_context:
        if isinstance(purchase_context, dict):
            try:
                pc_obj = PurchaseContext(**purchase_context)
            except Exception:
                pc_obj = None
        else:
            pc_obj = purchase_context

    # Crear orden si es apropiado
    order_created = None
    if pc_obj and _detect_purchase_keywords(user_message):
        order_created = _create_order_from_response(db, vendor, agent_reply, pc_obj)

    response = {
        "vendor_name": vendor.name,
        "user_message": user_message,
        "agent_response": agent_reply,
        "context_used": context_block,
        "matches_found": len(results),
    }
    
    if order_created:
        response["order_created"] = order_created
    
    return response
