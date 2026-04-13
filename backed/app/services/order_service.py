import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order
from app.models.vendor import Vendor
from app.schemas.order_schema import OrderCreateRequest


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
        status="pending",
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
