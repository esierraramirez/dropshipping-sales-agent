from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.agent.orchestrator import generate_agent_reply


def process_chat_message(
    db: Session,
    vendor: Vendor,
    message: str
) -> dict:
    # top_k=2 para optimizar tokens (vs 3)
    # Solo recupera los 2 productos más relevantes para ahorrar contexto
    return generate_agent_reply(
        db=db,
        vendor=vendor,
        user_message=message,
        top_k=2  # Reducido de 3 para ahorrar tokens
    )
