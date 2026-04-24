from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_vendor
from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.messenger_schema import (
    MessengerConnectionRequest,
    MessengerConnectionResponse,
)
from app.services.messenger_service import (
    upsert_messenger_connection,
    get_messenger_connection_by_vendor,
    process_incoming_messenger_message,
)

router = APIRouter()

# Guarda o actualiza las credenciales de Messenger del vendor (page ID, token).
@router.put("/messenger/me", response_model=MessengerConnectionResponse)
def upsert_my_messenger_connection(
    payload: MessengerConnectionRequest,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    """Upsert Messenger connection for current vendor"""
    return upsert_messenger_connection(
        db=db,
        vendor=current_vendor,
        payload=payload
    )

# Obtiene la configuración de Messenger conectada del vendor.
@router.get("/messenger/me", response_model=MessengerConnectionResponse)
def get_my_messenger_connection(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    """Get Messenger connection for current vendor"""
    return get_messenger_connection_by_vendor(db=db, vendor=current_vendor)

# Verifica el webhook de Messenger con Meta (desafío para validación).
@router.get("/messenger/webhook")
def verify_messenger_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
    db: Session = Depends(get_db),
):
    """Verify Messenger webhook with Meta"""
    from app.models.messenger_connection import MessengerConnection

    connection = (
        db.query(MessengerConnection)
        .filter(MessengerConnection.verify_token == hub_verify_token)
        .first()
    )

    if hub_mode == "subscribe" and connection:
        return PlainTextResponse(content=hub_challenge, status_code=200)

    return PlainTextResponse(content="Invalid verification token", status_code=403)

# Recibe mensajes de Messenger de Meta y los procesa con el agente IA.
@router.post("/messenger/webhook")
async def receive_messenger_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """Receive incoming Messenger message from Meta"""
    payload = await request.json()
    return await process_incoming_messenger_message(db=db, payload=payload)
