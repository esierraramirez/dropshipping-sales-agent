from datetime import datetime
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.vendor import Vendor
from app.models.messenger_connection import MessengerConnection
from app.schemas.messenger_schema import MessengerConnectionRequest
from app.agent.orchestrator import generate_agent_reply


def get_or_create_messenger_connection(db: Session, vendor: Vendor) -> MessengerConnection:
    connection = (
        db.query(MessengerConnection)
        .filter(MessengerConnection.vendor_id == vendor.id)
        .first()
    )

    if connection:
        return connection

    connection = MessengerConnection(
        vendor_id=vendor.id,
        is_connected=False
    )
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def upsert_messenger_connection(
    db: Session,
    vendor: Vendor,
    payload: MessengerConnectionRequest
) -> MessengerConnection:
    connection = get_or_create_messenger_connection(db=db, vendor=vendor)

    connection.page_id = payload.page_id
    connection.page_name = payload.page_name
    connection.page_access_token = payload.page_access_token
    connection.verify_token = payload.verify_token
    connection.is_connected = True
    connection.connected_at = datetime.utcnow()

    db.commit()
    db.refresh(connection)
    return connection


def get_messenger_connection_by_vendor(db: Session, vendor: Vendor) -> MessengerConnection:
    connection = (
        db.query(MessengerConnection)
        .filter(MessengerConnection.vendor_id == vendor.id)
        .first()
    )

    if not connection:
        raise HTTPException(status_code=404, detail="La empresa no tiene conexión de Messenger registrada.")

    return connection


def get_messenger_connection_by_page_id(db: Session, page_id: str) -> MessengerConnection | None:
    return (
        db.query(MessengerConnection)
        .filter(MessengerConnection.page_id == page_id)
        .first()
    )


async def send_messenger_text_message(
    page_id: str,
    page_access_token: str,
    recipient_id: str,
    message: str
) -> dict:
    """
    Envía un mensaje de texto por Facebook Messenger Graph API.
    """
    url = f"https://graph.instagram.com/v25.0/{page_id}/messages"

    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        }
    }

    headers = {
        "Authorization": f"Bearer {page_access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar mensaje por Messenger: {response.text}"
        )

    return response.json()


async def process_incoming_messenger_message(db: Session, payload: dict) -> dict:
    """
    Extrae mensaje entrante del webhook, identifica empresa,
    llama al orquestador y responde por Messenger.
    """
    try:
        entry = payload.get("entry", [])
        if not entry:
            return {"status": "ignored", "reason": "No entries"}

        page_id = entry[0].get("id")
        messaging = entry[0].get("messaging", [])

        if not messaging:
            return {"status": "ignored", "reason": "No messages"}

        message_event = messaging[0]
        sender_id = message_event.get("sender", {}).get("id")
        message_data = message_event.get("message", {})

        if not message_data:
            return {"status": "ignored", "reason": "No message data"}

        user_text = message_data.get("text")
        if not user_text:
            return {"status": "ignored", "reason": "No text"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payload de Messenger inválido: {str(e)}")

    connection = get_messenger_connection_by_page_id(db=db, page_id=page_id)
    if not connection:
        raise HTTPException(status_code=404, detail="No se encontró empresa asociada a esta página de Messenger.")

    vendor = connection.vendor
    if not vendor:
        raise HTTPException(status_code=404, detail="No se encontró la empresa asociada a la conexión.")

    orchestrated = generate_agent_reply(
        db=db,
        vendor=vendor,
        message=user_text,
        history=[],
        purchase_context=None
    )

    agent_response = orchestrated.get("agent_response", "")

    if agent_response:
        await send_messenger_text_message(
            page_id=page_id,
            page_access_token=connection.page_access_token,
            recipient_id=sender_id,
            message=agent_response
        )

    return {
        "status": "processed",
        "message": user_text,
        "response": agent_response
    }
