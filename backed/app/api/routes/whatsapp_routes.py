from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_vendor
from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.whatsapp_schema import (
    WhatsAppConnectionRequest,
    WhatsAppConnectionResponse,
)
from app.services.whatsapp_service import (
    upsert_whatsapp_connection,
    get_whatsapp_connection_by_vendor,
    process_incoming_whatsapp_message,
)

router = APIRouter()


@router.put("/whatsapp/me", response_model=WhatsAppConnectionResponse)
def upsert_my_whatsapp_connection(
    payload: WhatsAppConnectionRequest,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return upsert_whatsapp_connection(
        db=db,
        vendor=current_vendor,
        payload=payload
    )


@router.get("/whatsapp/me", response_model=WhatsAppConnectionResponse)
def get_my_whatsapp_connection(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return get_whatsapp_connection_by_vendor(db=db, vendor=current_vendor)


@router.get("/whatsapp/webhook")
def verify_whatsapp_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
    db: Session = Depends(get_db),
):
    # Busca una conexión cuyo verify_token coincida
    from app.models.whatsapp_connection import WhatsAppConnection

    connection = (
        db.query(WhatsAppConnection)
        .filter(WhatsAppConnection.verify_token == hub_verify_token)
        .first()
    )

    if hub_mode == "subscribe" and connection:
        return PlainTextResponse(content=hub_challenge, status_code=200)

    return PlainTextResponse(content="Invalid verification token", status_code=403)


@router.post("/whatsapp/webhook")
async def receive_whatsapp_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.json()
    return await process_incoming_whatsapp_message(db=db, payload=payload)
