from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_vendor
from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_message

router = APIRouter()


@router.post("/chat/me", response_model=ChatResponse)
def chat_with_agent(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return process_chat_message(
        db=db,
        vendor=current_vendor,
        message=payload.message
    )
