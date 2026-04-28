from datetime import datetime
import httpx
import re
import unicodedata
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.vendor import Vendor
from app.models.whatsapp_connection import WhatsAppConnection
from app.schemas.whatsapp_schema import WhatsAppConnectionRequest
from app.agent.orchestrator import generate_agent_reply


_WA_SESSION_STATE: dict[str, dict] = {}


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _session_key(vendor_id: int, from_phone: str) -> str:
    return f"{vendor_id}:{from_phone}"


def _extract_customer_fields(message: str) -> dict[str, str]:
    extracted: dict[str, str] = {}

    name_match = re.search(r"(?im)^\s*nombre\s*[:\-]\s*(.+)$", message)
    if name_match:
        extracted["customer_name"] = name_match.group(1).strip()

    phone_match = re.search(
        r"(?im)^\s*(?:telefono|tel[eé]fono|celular|whatsapp)\s*[:\-]?\s*([+\d][\d\s\-]{6,})$",
        message,
    )
    if phone_match:
        extracted["customer_phone"] = re.sub(r"\D", "", phone_match.group(1))

    address_match = re.search(r"(?im)^\s*(?:direccion|direcci[oó]n)\s*[:\-]?\s*(.+)$", message)
    if address_match:
        extracted["customer_address"] = address_match.group(1).strip()

    return extracted


def _is_order_confirmation_intent(message: str) -> bool:
    normalized = _normalize_text(message)
    confirm_terms = [
        "quiero hacer el pedido",
        "confirmo compra",
        "confirmar compra",
        "finalizar compra",
        "finalizar pedido",
        "confirmo el pedido",
        "procedamos",
        "si lo quiero",
        "lo compro",
    ]
    return any(term in normalized for term in confirm_terms)


def _looks_like_product_selection(message: str) -> bool:
    normalized = _normalize_text(message)
    product_terms = [
        "quiero",
        "producto",
        "talla",
        "color",
        "modelo",
        "jean",
        "camisa",
        "zapato",
        "zapatilla",
        "blusa",
        "pantalon",
        "pedido",
    ]
    found = sum(1 for term in product_terms if term in normalized)
    return found >= 2


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

    session_key = _session_key(vendor.id, from_phone)
    session = _WA_SESSION_STATE.get(
        session_key,
        {
            "history": [],
            "customer_name": None,
            "customer_phone": None,
            "customer_address": None,
            "last_product_message": None,
            "is_confirmed": False,
        },
    )

    extracted_fields = _extract_customer_fields(user_text)
    if extracted_fields.get("customer_name"):
        session["customer_name"] = extracted_fields["customer_name"]
    if extracted_fields.get("customer_phone"):
        session["customer_phone"] = extracted_fields["customer_phone"]
    if extracted_fields.get("customer_address"):
        session["customer_address"] = extracted_fields["customer_address"]

    if _looks_like_product_selection(user_text):
        session["last_product_message"] = user_text.strip()

    if _is_order_confirmation_intent(user_text):
        session["is_confirmed"] = True

    purchase_context = {
        "customer_name": session.get("customer_name"),
        "customer_phone": session.get("customer_phone"),
        "customer_address": session.get("customer_address"),
        "items": [],
        "total_amount": 0.0,
        "is_confirmed": bool(
            session.get("is_confirmed")
            and session.get("customer_name")
            and session.get("customer_phone")
            and session.get("last_product_message")
        ),
    }

    history_for_agent = session.get("history", [])[-12:]
    history_for_agent.append({"role": "user", "content": user_text})

    orchestrated = generate_agent_reply(
        db=db,
        vendor=vendor,
        user_message=user_text,
        conversation_history=history_for_agent,
        purchase_context=purchase_context,
        top_k=4
    )

    reply_text = orchestrated["agent_response"]
    order_created = orchestrated.get("order_created")
    if order_created:
        order_id = order_created.get("id")
        if order_id and f"#{order_id}" not in reply_text:
            reply_text = (
                f"{reply_text}\n\n"
                f"✅ Tu pedido fue confirmado y registrado con el numero #{order_id}."
            )

    session_history = history_for_agent
    session_history.append({"role": "assistant", "content": reply_text})
    session["history"] = session_history[-12:]

    if order_created:
        session["is_confirmed"] = False
        session["last_product_message"] = None

    _WA_SESSION_STATE[session_key] = session

    await send_whatsapp_text_message(
        phone_number_id=connection.phone_number_id,
        access_token=connection.access_token,
        to_phone=from_phone,
        message=reply_text
    )

    return {
        "status": "ok",
        "vendor_name": vendor.name,
        "incoming_message": user_text,
        "reply_sent": reply_text
    }
