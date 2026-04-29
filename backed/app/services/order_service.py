import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order
from app.models.vendor import Vendor
from app.schemas.order_schema import OrderCreateRequest
from app.services.audit_service import log_delete


VALID_ORDER_STATUSES = {"en_proceso", "enviado", "entregado", "cancelado"}


def create_order(db: Session, vendor: Vendor, payload: OrderCreateRequest) -> dict:
    total_amount = 0.0
    normalized_items = []

    for item in payload.items:
        item_total = item.quantity * item.unit_price
        total_amount += item_total

        normalized_items.append({
            "product_id": item.product_id,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "unit_price": item.unit_price
        })

    order = Order(
        vendor_id=vendor.id,
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        customer_address=payload.customer_address,
        items_json=json.dumps(normalized_items, ensure_ascii=False),
        total_amount=total_amount,
        status="en_proceso",
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return serialize_order(order)


def list_orders_by_vendor(db: Session, vendor: Vendor) -> dict:
    orders = (
        db.query(Order)
        .filter(Order.vendor_id == vendor.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return {
        "vendor_name": vendor.name,
        "total_orders": len(orders),
        "orders": [serialize_order(order) for order in orders]
    }


def get_order_by_id(db: Session, vendor: Vendor, order_id: int) -> dict:
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.vendor_id == vendor.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")

    return serialize_order(order)


def update_order_status(db: Session, vendor: Vendor, order_id: int, new_status: str) -> dict:
    if new_status not in VALID_ORDER_STATUSES:
        raise HTTPException(status_code=400, detail="Estado de orden inválido.")

    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.vendor_id == vendor.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")

    order.status = new_status
    db.commit()
    db.refresh(order)

    return serialize_order(order)


def delete_order(db: Session, vendor: Vendor, order_id: int) -> dict:
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.vendor_id == vendor.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")

    # Registrar auditoria antes de eliminar fisicamente la orden.
    log_delete(
        db=db,
        entity_type="Order",
        entity_id=order.id,
        entity_object=order,
        vendor=vendor,
        description=f"Orden eliminada: {order.id}",
    )

    deleted_order_id = order.id
    db.delete(order)
    db.commit()

    return {
        "message": "Orden eliminada correctamente.",
        "order_id": deleted_order_id,
    }


def serialize_order(order: Order) -> dict:
    try:
        items = json.loads(order.items_json)
    except Exception:
        items = []

    return {
        "id": order.id,
        "vendor_id": order.vendor_id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "customer_address": order.customer_address,
        "items": items,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }


def create_order_from_chat(
    db: Session,
    vendor: Vendor,
    customer_name: str,
    customer_phone: str,
    items: list[dict],
    conversation_summary: str = "",
    customer_address: str = ""
) -> dict:
    """
    Crea una orden desde la conversación del chat del agente.
    
    Items format: [{"product_id": "...", "product_name": "...", "quantity": 1, "unit_price": 50000}, ...]
    """
    total_amount = 0.0
    normalized_items = []

    for item in items:
        item_total = item.get("quantity", 1) * item.get("unit_price", 0)
        total_amount += item_total

        normalized_items.append({
            "product_id": item.get("product_id", ""),
            "product_name": item.get("product_name", ""),
            "quantity": item.get("quantity", 1),
            "unit_price": item.get("unit_price", 0)
        })

    order = Order(
        vendor_id=vendor.id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_address=customer_address,
        items_json=json.dumps(normalized_items, ensure_ascii=False),
        total_amount=total_amount,
        status="en_proceso",
        chat_summary=conversation_summary,
        conversation_notes="Orden creada desde conversación de chat del agente"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return serialize_order(order)
