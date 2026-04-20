from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.services.retrieval_service import retrieve_vendor_context, build_context_block
from app.agent.policies import is_within_business_hours, resolve_tone_instruction
from app.agent.prompts import build_sales_agent_system_prompt


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


def generate_agent_reply(
    db: Session,
    vendor: Vendor,
    user_message: str,
    conversation_history: Optional[List[dict]] = None,
    top_k: int = 3
) -> dict:
    """
    Orquesta todo el flujo del agente:
    settings -> horario -> retrieval mejorado -> prompt -> LLM -> respuesta
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

    return {
        "vendor_name": vendor.name,
        "user_message": user_message,
        "agent_response": agent_reply,
        "context_used": context_block,
        "matches_found": len(results),
    }
