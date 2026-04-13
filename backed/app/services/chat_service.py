from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.agent.orchestrator import generate_agent_reply


def process_chat_message(
    db: Session,
    vendor: Vendor,
    message: str
) -> dict:
    return generate_agent_reply(
        db=db,
        vendor=vendor,
        user_message=message,
        top_k=3
    )
