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


def generate_agent_reply(
    db: Session,
    vendor: Vendor,
    user_message: str,
    top_k: int = 3
) -> dict:
    """
    Orquesta todo el flujo del agente:
    settings -> horario -> retrieval -> prompt -> LLM -> respuesta
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

    retrieval_result = retrieve_vendor_context(
        vendor=vendor,
        query=user_message,
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
