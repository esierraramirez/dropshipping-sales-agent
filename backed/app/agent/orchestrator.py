from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
import json
import re
import unicodedata

from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.services.retrieval_service import retrieve_vendor_context, build_context_block
from app.services.order_service import create_order_from_chat
from app.agent.policies import is_within_business_hours, resolve_tone_instruction
from app.agent.prompts import build_sales_agent_system_prompt
from app.schemas.chat_schema import PurchaseContext, CartItem


NO_KNOWLEDGE_REPLY = (
    "Por ahora no tengo esa informacion disponible en el catalogo. "
    "Si quieres, puedo ayudarte con los productos y datos que tengo registrados."
)


def _is_simple_greeting(text: str) -> bool:
    normalized = _normalize_text(text)
    greeting_words = {
        "hola",
        "buenas",
        "buen",
        "dia",
        "dias",
        "tarde",
        "tardes",
        "noche",
        "noches",
        "hey",
        "hello",
        "saludos",
    }
    words = normalized.split()
    return bool(words) and all(word in greeting_words for word in words)


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _is_catalog_or_sales_query(text: str) -> bool:
    normalized_words = set(_normalize_text(text).split())
    catalog_terms = {
        "catalogo",
        "menu",
        "producto",
        "productos",
        "precio",
        "precios",
        "cuesta",
        "vale",
        "valor",
        "disponible",
        "disponibilidad",
        "stock",
        "tienen",
        "tienes",
        "venden",
        "vendes",
        "recomiendas",
        "recomiendame",
        "comprar",
        "compra",
        "pedido",
        "orden",
        "talla",
        "tallas",
        "color",
        "colores",
        "envio",
        "envios",
        "domicilio",
        "garantia",
        "devolucion",
        "cambio",
        "pagar",
        "pago",
    }
    return bool(normalized_words & catalog_terms)


def _build_general_reply(vendor_name: str, user_message: str) -> str:
    normalized = _normalize_text(user_message)
    if normalized in {"gracias", "muchas gracias", "ok gracias", "listo gracias"}:
        return "¡Con mucho gusto! 😊 Estoy aquí para ayudarte cuando lo necesites."

    if normalized in {"como estas", "que tal", "como vas"}:
        return f"¡Muy bien, gracias por preguntar! 😊 Aquí estoy para ayudarte con {vendor_name}."

    if normalized in {"ok", "listo", "perfecto", "vale", "bueno"}:
        return "Perfecto 😊 Quedo atento a lo que necesites."

    return "Claro 😊 Estoy aquí para ayudarte. Cuéntame qué estás buscando o qué necesitas saber."


def _is_general_social_message(text: str) -> bool:
    normalized = _normalize_text(text)
    social_phrases = {
        "gracias",
        "muchas gracias",
        "ok gracias",
        "listo gracias",
        "como estas",
        "que tal",
        "como vas",
        "ok",
        "listo",
        "perfecto",
        "vale",
        "bueno",
    }
    return normalized in social_phrases


def _build_welcome_reply(vendor_name: str) -> str:
    return f"¡Hola! 👋 Soy el asistente de {vendor_name}. ¿En qué puedo ayudarte hoy?"


def get_vendor_settings(db: Session, vendor_id: int) -> VendorSettings | None:
    # Obtiene la configuración del vendor (horarios, tono, habilitación).
    return db.query(VendorSettings).filter(VendorSettings.vendor_id == vendor_id).first()


def _build_enhanced_query(user_message: str, history: Optional[List[dict]] = None) -> str:
    # Mejora la búsqueda semántica agregando contexto del historial conversacional.
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
    # Detecta palabras clave de intención de compra (DEPRECADA - no se usa).
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


def _strip_repeated_intro(reply: str) -> str:
    intro_patterns = [
        r"^\s*[¡!]?hola[!¡,. ]*\s*",
        r"^\s*soy el asistente(?: virtual)?(?: de [^.?!\n]+)?[.?!]?\s*",
        r"^\s*[¿?¡!]*en qu[eé] puedo ayudarte hoy[?¿!¡]*\s*[,.;:-]?\s*",
    ]

    cleaned = reply
    previous = None
    while previous != cleaned:
        previous = cleaned
        for pattern in intro_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip() or reply


def _create_order_from_response(
    db: Session,
    vendor: Vendor,
    agent_response: str,
    purchase_context: Optional[PurchaseContext]
) -> Optional[dict]:
    # Crea una orden automáticamente cuando el agente confirma la venta y tiene datos del cliente.
    if not purchase_context:
        print("  └─ No hay purchase_context")
        return None
    
    # Verifica que tenga datos del cliente
    if not purchase_context.customer_name:
        print(f"  └─ Sin nombre del cliente")
        return None
    
    if not purchase_context.customer_phone:
        print(f"  └─ Sin teléfono del cliente")
        return None
    
    # Verifica que el agente haya confirmado la orden
    confirm_keywords = [
        "registré tu orden",
        "registrar tu orden",
        "orden registrada",
        "procesará tu orden",
        "gracias por comprar",
        "¡excelente!",
        "perfecto, hemos registrado",
        "hemos registrado tu orden",
        "tu orden quedó lista",
        "orden lista",
    ]
    
    response_lower = agent_response.lower()
    found_keyword = False
    for kw in confirm_keywords:
        if kw in response_lower:
            found_keyword = True
            print(f"  └─ Palabra clave de confirmación encontrada: '{kw}'")
            break
    
    if not found_keyword:
        print(f"  └─ No se encontró palabra clave de confirmación en: {agent_response[:100]}")
        return None
    
    # Si hay items, úsalos. Si no, crea un item genérico con el resumen de la conversación
    items_data = []
    
    if purchase_context.items and len(purchase_context.items) > 0:
        items_data = [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in purchase_context.items
        ]
    else:
        # Crea un item genérico con resumen de la orden
        summary_text = "Compra realizada desde chat del agente"
        total = purchase_context.total_amount or 0.0
        
        items_data = [
            {
                "product_id": "chat_order",
                "product_name": f"Compra en línea - {summary_text}",
                "quantity": 1,
                "unit_price": total if total > 0 else 0,
            }
        ]
    
    # Crea la orden
    try:
        order = create_order_from_chat(
            db=db,
            vendor=vendor,
            customer_name=purchase_context.customer_name,
            customer_phone=purchase_context.customer_phone,
            customer_address=purchase_context.customer_address or "",
            items=items_data,
            conversation_summary="Creada desde chat del agente"
        )
        
        print(f"  └─ ✅ Orden creada exitosamente, ID: {order.get('id')}")
        return order
    except Exception as e:
        print(f"  └─ ❌ Error al crear orden: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def generate_agent_reply(
    db: Session,
    vendor: Vendor,
    user_message: str,
    conversation_history: Optional[List[dict]] = None,
    purchase_context: Optional[dict] = None,
    top_k: int = 3
) -> dict:
    # Orquesta el flujo: carga settings → verifica horario → busca contexto → LLM → crea orden si aplica.
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

    if _is_simple_greeting(user_message):
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": _build_welcome_reply(vendor.name),
            "context_used": "Saludo inicial. No se utilizó contexto del catálogo.",
            "matches_found": 0,
        }

    if _is_general_social_message(user_message):
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": _build_general_reply(vendor.name, user_message),
            "context_used": "Conversación general. No se utilizó contexto del catálogo.",
            "matches_found": 0,
        }

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
    if not retrieval_result.get("knowledge_base_ready") or not results:
        if not _is_catalog_or_sales_query(user_message):
            return {
                "vendor_name": vendor.name,
                "user_message": user_message,
                "agent_response": _build_general_reply(vendor.name, user_message),
                "context_used": "Conversación general. No se utilizó contexto del catálogo.",
                "matches_found": 0,
            }

        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": NO_KNOWLEDGE_REPLY,
            "context_used": "No se encontraron datos relevantes en la base de conocimiento.",
            "matches_found": 0,
        }

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
    agent_reply = _strip_repeated_intro(agent_reply)

    # Convertir purchase_context a objeto si viene como dict
    pc_obj = None
    if purchase_context:
        if isinstance(purchase_context, dict):
            try:
                pc_obj = PurchaseContext(**purchase_context)
            except Exception as e:
                print(f"Error al convertir purchase_context: {e}")
                pc_obj = None
        else:
            pc_obj = purchase_context

    # Crear orden si es apropiado
    # IMPORTANTE: Crear orden si el AGENTE confirmó (no si el usuario pidió)
    order_created = None
    if pc_obj:
        print(f"🔍 [ORDEN] Verificando creación de orden:")
        print(f"   - purchase_context existe: ✓")
        print(f"   - customer_name: {pc_obj.customer_name}")
        print(f"   - customer_phone: {pc_obj.customer_phone}")
        print(f"   - agent_reply contiene 'registr': {'registr' in agent_reply.lower()}")
        
        # Intenta crear orden si el agente confirmó
        order_created = _create_order_from_response(db, vendor, agent_reply, pc_obj)
        
        if order_created:
            print(f"✅ [ORDEN] Orden creada: {order_created}")
        else:
            print(f"❌ [ORDEN] No se pudo crear orden")

    response = {
        "vendor_name": vendor.name,
        "user_message": user_message,
        "agent_response": agent_reply,
        "context_used": context_block,
        "matches_found": len(results),
    }
    
    if order_created:
        response["order_created"] = order_created
    
    # Retorna el contexto de compra actualizado
    if pc_obj:
        response["purchase_context"] = pc_obj.model_dump()
    
    return response
