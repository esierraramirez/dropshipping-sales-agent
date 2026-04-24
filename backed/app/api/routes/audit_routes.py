from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_vendor
from app.models.vendor import Vendor
from app.models.product import Product
from app.models.audit_log import AuditLog
from app.services.audit_service import get_audit_logs, get_entity_history, log_action
from datetime import datetime

router = APIRouter()


# Obtiene el histórico de cambios de un producto específico (para auditoría).
@router.get("/audit/products/{product_id}/history")
def get_product_audit_history(
    product_id: int,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    """Obtiene el histórico completo de cambios de un producto (auditoría)"""
    
    # Verificar que el producto pertenece al vendor
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.vendor_id == current_vendor.id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Obtener histórico de auditoría
    history = get_entity_history(db=db, entity_type="Product", entity_id=product_id)
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_changes": len(history),
        "history": [
            {
                "action": log.action,
                "timestamp": log.created_at.isoformat(),
                "vendor_id": log.vendor_id,
                "description": log.description,
                "changed_at": log.created_at.isoformat(),
            }
            for log in history
        ]
    }


# Obtiene todos los productos eliminados del vendor (archivados).
@router.get("/audit/products/deleted")
def get_deleted_products(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    """Lista todos los productos eliminados/archivados del vendor"""
    
    deleted_products = db.query(Product).filter(
        Product.vendor_id == current_vendor.id,
        Product.is_deleted == True
    ).order_by(Product.deleted_at.desc()).all()
    
    return {
        "vendor_name": current_vendor.name,
        "total_deleted": len(deleted_products),
        "deleted_products": [
            {
                "id": p.id,
                "product_id": p.product_id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "currency": p.currency,
                "deleted_at": p.deleted_at.isoformat(),
            }
            for p in deleted_products
        ]
    }


# Restaura un producto eliminado (lo marca como no eliminado).
@router.post("/audit/products/{product_id}/restore")
def restore_deleted_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    """Restaura un producto que fue eliminado previamente"""
    
    # Buscar producto eliminado
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.vendor_id == current_vendor.id,
        Product.is_deleted == True
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto eliminado no encontrado")
    
    product_name = product.name
    
    # Registrar restauración en auditoría
    log_action(
        db=db,
        action="restored",
        entity_type="Product",
        entity_id=product_id,
        vendor=current_vendor,
        new_values=product,
        description=f"Producto restaurado: {product_name}"
    )
    
    # Restaurar producto
    product.is_deleted = False
    product.deleted_at = None
    db.commit()
    
    return {
        "message": f"Producto '{product_name}' restaurado correctamente",
        "product_id": product_id,
        "restored_at": datetime.utcnow().isoformat()
    }


# Obtiene logs de auditoría del vendor (todos sus cambios).
@router.get("/audit/logs")
def get_vendor_audit_logs(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    """Obtiene el log de auditoría de todas las acciones del vendor"""
    
    logs = get_audit_logs(
        db=db,
        vendor_id=current_vendor.id,
        limit=limit
    )
    
    return {
        "vendor_name": current_vendor.name,
        "total_logs": len(logs),
        "logs": [
            {
                "id": log.id,
                "action": log.action,
                "entity_type": log.entity_type,
                "entity_id": log.entity_id,
                "description": log.description,
                "timestamp": log.created_at.isoformat(),
            }
            for log in logs
        ]
    }
