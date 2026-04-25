from datetime import datetime
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.vendor import Vendor
from app.models.whatsapp_connection import WhatsAppConnection
from app.schemas.whatsapp_schema import WhatsAppConnectionRequest
from app.agent.orchestrator import generate_agent_reply


def get_or_create_whatsapp_connection(db: Session, vendor: Vendor) -> WhatsAppConnection:
    connection = (
        db.query(WhatsAppConnection)
        .filter(WhatsAppConnection.vendor_id == vendor.id)
        .first()
    )

    if connection:
        return connection

    connection = WhatsAppConnection(
        vendor_id=vendor.id,
        is_connected=False
    )
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def upsert_whatsapp_connection(
    db: Session,
    vendor: Vendor,
    payload: WhatsAppConnectionRequest
) -> WhatsAppConnection:
    connection = get_or_create_whatsapp_connection(db=db, vendor=vendor)

    duplicate_connections = (
        db.query(WhatsAppConnection)
        .filter(
            WhatsAppConnection.phone_number_id == payload.phone_number_id,
            WhatsAppConnection.vendor_id != vendor.id,
            WhatsAppConnection.is_connected.is_(True),
        )
        .all()
    )
    for duplicate in duplicate_connections:
        duplicate.is_connected = False

    connection.phone_number = payload.phone_number
    connection.phone_number_id = payload.phone_number_id
    connection.business_account_id = payload.business_account_id
    connection.access_token = payload.access_token
    connection.verify_token = payload.verify_token
    connection.is_connected = True
    connection.connected_at = datetime.utcnow()

    db.commit()
    db.refresh(connection)
    return connection


def get_whatsapp_connection_by_vendor(db: Session, vendor: Vendor) -> WhatsAppConnection:
    connection = (
        db.query(WhatsAppConnection)
        .filter(WhatsAppConnection.vendor_id == vendor.id)
        .first()
    )

    if not connection:
        raise HTTPException(status_code=404, detail="La empresa no tiene conexión de WhatsApp registrada.")

    return connection


def get_whatsapp_connection_by_phone_number_id(db: Session, phone_number_id: str) -> WhatsAppConnection | None:
    return (
        db.query(WhatsAppConnection)
        .filter(
            WhatsAppConnection.phone_number_id == phone_number_id,
            WhatsAppConnection.is_connected.is_(True),
        )
        .order_by(
            WhatsAppConnection.connected_at.desc().nullslast(),
            WhatsAppConnection.id.desc(),
        )
        .first()
    )


async def send_whatsapp_text_message(
    phone_number_id: str,
    access_token: str,
    to_phone: str,
    message: str
) -> dict:
    """
    Envía un mensaje de texto por WhatsApp Cloud API.
    """
    url = f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}/{phone_number_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {
            "body": message
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar mensaje por WhatsApp: {response.text}"
        )

    return response.json()


async def process_incoming_whatsapp_message(db: Session, payload: dict) -> dict:
    """
    Extrae mensaje entrante del webhook, identifica empresa,
    llama al orquestador y responde por WhatsApp.
    """
    try:
        entry = payload["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        metadata = value.get("metadata", {})
        phone_number_id = metadata.get("phone_number_id")

        messages = value.get("messages", [])
        if not messages:
            return {"status": "ignored", "reason": "No incoming messages"}

        message_obj = messages[0]
        from_phone = message_obj.get("from")
        message_type = message_obj.get("type")

        if message_type != "text":
            return {"status": "ignored", "reason": f"Unsupported message type: {message_type}"}

        user_text = message_obj["text"]["body"]

    except Exception:
        raise HTTPException(status_code=400, detail="Payload de WhatsApp inválido.")

    print(f"[WHATSAPP] Incoming message for phone_number_id={phone_number_id} from={from_phone}")

    connection = get_whatsapp_connection_by_phone_number_id(db=db, phone_number_id=phone_number_id)
    if not connection:
        print(f"[WHATSAPP] No connected vendor found for phone_number_id={phone_number_id}")
        raise HTTPException(status_code=404, detail="No se encontró empresa asociada a este número de WhatsApp.")

    vendor = connection.vendor
    if not vendor:
        print(f"[WHATSAPP] Connection id={connection.id} has no vendor")
        raise HTTPException(status_code=404, detail="No se encontró la empresa asociada a la conexión.")

    print(f"[WHATSAPP] Routed to vendor_id={vendor.id} vendor_name={vendor.name!r}")

    orchestrated = generate_agent_reply(
        db=db,
        vendor=vendor,
        user_message=user_text,
        top_k=3
    )

    await send_whatsapp_text_message(
        phone_number_id=connection.phone_number_id,
        access_token=connection.access_token,
        to_phone=from_phone,
        message=orchestrated["agent_response"]
    )

    return {
        "status": "ok",
        "vendor_name": vendor.name,
        "incoming_message": user_text,
        "reply_sent": orchestrated["agent_response"]
    }
