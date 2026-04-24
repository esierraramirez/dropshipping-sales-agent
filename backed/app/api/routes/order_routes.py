from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_vendor
from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.order_schema import (
    OrderCreateRequest,
    OrderResponse,
    OrderListResponse,
    OrderStatusUpdateRequest,
)
from app.services.order_service import (
    create_order,
    list_orders_by_vendor,
    get_order_by_id,
    update_order_status,
)

router = APIRouter()

# Crea una nueva orden manualmente (vendedor registra compra de cliente).
@router.post("/orders/me", response_model=OrderResponse)
def create_my_order(
    payload: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return create_order(db=db, vendor=current_vendor, payload=payload)

# Lista todas las órdenes del vendor (creadas por agente, webhook o manual).
@router.get("/orders/me", response_model=OrderListResponse)
def list_my_orders(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return list_orders_by_vendor(db=db, vendor=current_vendor)

# Obtiene los detalles completos de una orden específica.
@router.get("/orders/me/{order_id}", response_model=OrderResponse)
def get_my_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return get_order_by_id(db=db, vendor=current_vendor, order_id=order_id)

# Actualiza el estado de una orden (pending → confirmed → processed → shipped → cancelled).
@router.patch("/orders/me/{order_id}/status", response_model=OrderResponse)
def patch_my_order_status(
    order_id: int,
    payload: OrderStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return update_order_status(
        db=db,
        vendor=current_vendor,
        order_id=order_id,
        new_status=payload.status
    )
