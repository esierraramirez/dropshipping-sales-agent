from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_current_vendor
from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.models.product import Product
from app.models.order import Order
from app.schemas.vendor_schema import VendorResponse, VendorUpdateRequest
from app.services.audit_service import log_action

router = APIRouter()

# Obtiene la información completa de la empresa del vendor autenticado.
@router.get("/empresa/me", response_model=VendorResponse)
def get_my_empresa(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    """Obtener información completa de la empresa"""
    return current_vendor

# Actualiza datos de la empresa (RFC, sector, teléfono, website, dirección, etc).
@router.patch("/empresa/me", response_model=VendorResponse)
def update_my_empresa(
    payload: VendorUpdateRequest,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    """Actualizar información de la empresa"""
    if payload.rfc is not None:
        current_vendor.rfc = payload.rfc
    if payload.sector is not None:
        current_vendor.sector = payload.sector
    if payload.phone is not None:
        current_vendor.phone = payload.phone
    if payload.website is not None:
        current_vendor.website = payload.website
    if payload.address is not None:
        current_vendor.address = payload.address
    if payload.city is not None:
        current_vendor.city = payload.city
    if payload.state is not None:
        current_vendor.state = payload.state
    if payload.country is not None:
        current_vendor.country = payload.country
    if payload.postal_code is not None:
        current_vendor.postal_code = payload.postal_code
    if payload.description is not None:
        current_vendor.description = payload.description
    if payload.payment_methods is not None:
        current_vendor.payment_methods = payload.payment_methods

    db.commit()
    db.refresh(current_vendor)
    return current_vendor

# Retorna estadísticas de la empresa (total productos, órdenes, clientes únicos).
@router.get("/empresa/me/stats")
def get_empresa_stats(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    """Obtener estadísticas de la empresa"""
    total_products = db.query(func.count(Product.id)).filter(
        Product.vendor_id == current_vendor.id
    ).scalar() or 0

    total_orders = db.query(func.count(Order.id)).filter(
        Order.vendor_id == current_vendor.id
    ).scalar() or 0

    total_customers = db.query(func.count(func.distinct(Order.customer_name))).filter(
        Order.vendor_id == current_vendor.id
    ).scalar() or 0

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_customers": total_customers,
    }


# Desactiva la empresa autenticada (eliminacion logica).
@router.delete("/empresa/me")
def delete_my_empresa(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor)
):
    if not current_vendor.is_active:
        return {
            "message": "La empresa ya se encontraba inactiva.",
            "vendor_id": current_vendor.id,
            "is_active": current_vendor.is_active,
        }

    log_action(
        db=db,
        action="deleted",
        entity_type="Vendor",
        entity_id=current_vendor.id,
        vendor=current_vendor,
        old_values=current_vendor,
        new_values=None,
        description=f"Empresa desactivada: {current_vendor.name}",
    )

    current_vendor.is_active = False
    db.commit()
    db.refresh(current_vendor)

    return {
        "message": "Empresa desactivada correctamente.",
        "vendor_id": current_vendor.id,
        "is_active": current_vendor.is_active,
    }
