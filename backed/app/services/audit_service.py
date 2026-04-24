import json
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.vendor import Vendor


def serialize_object(obj: Any) -> str:
    """
    Serializa un objeto ORM a JSON string para almacenamiento en auditoría.
    """
    if obj is None:
        return None
    
    # Convertir objeto ORM a dict
    data = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        
        # Convertir tipos especiales
        if isinstance(value, datetime):
            data[column.name] = value.isoformat()
        elif hasattr(value, '__dict__'):  # Objeto relacionado
            data[column.name] = str(value)
        else:
            data[column.name] = value
    
    return json.dumps(data, ensure_ascii=False, default=str)


def log_action(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: int,
    vendor: Optional[Vendor] = None,
    old_values: Optional[Any] = None,
    new_values: Optional[Any] = None,
    description: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """
    Registra una acción en la tabla de auditoría.
    
    Parámetros:
    - action: "created", "updated", "deleted", "restored"
    - entity_type: "Product", "Order", "Vendor", etc.
    - entity_id: ID del objeto afectado
    - vendor: Vendor que realiza la acción (puede ser None para acciones del sistema)
    - old_values: Datos anteriores (para updated/deleted)
    - new_values: Datos nuevos (para created/updated)
    - description: Descripción legible de la acción
    - ip_address: IP del cliente (opcional)
    """
    
    # Serializar valores si son objetos
    old_values_str = serialize_object(old_values) if old_values else None
    new_values_str = serialize_object(new_values) if new_values else None
    
    audit_log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        vendor_id=vendor.id if vendor else None,
        old_values=old_values_str,
        new_values=new_values_str,
        description=description or f"{action} {entity_type}",
        ip_address=ip_address,
        created_at=datetime.utcnow(),
    )
    
    db.add(audit_log)
    db.flush()  # Flush sin commit (se hace en el llamador)
    
    return audit_log


def log_delete(
    db: Session,
    entity_type: str,
    entity_id: int,
    entity_object: Any,
    vendor: Vendor,
    description: Optional[str] = None,
) -> AuditLog:
    """
    Registra una eliminación con todos los datos del objeto.
    """
    return log_action(
        db=db,
        action="deleted",
        entity_type=entity_type,
        entity_id=entity_id,
        vendor=vendor,
        old_values=entity_object,  # Guardar datos completos antes de eliminar
        new_values=None,
        description=description or f"Eliminado: {entity_type} (ID: {entity_id})",
    )


def get_audit_logs(
    db: Session,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    action: Optional[str] = None,
    limit: int = 100,
) -> list[AuditLog]:
    """
    Recupera logs de auditoría con filtros opcionales.
    """
    query = db.query(AuditLog)
    
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)
    if vendor_id:
        query = query.filter(AuditLog.vendor_id == vendor_id)
    if action:
        query = query.filter(AuditLog.action == action)
    
    return query.order_by(AuditLog.created_at.desc()).limit(limit).all()


def get_entity_history(
    db: Session,
    entity_type: str,
    entity_id: int,
) -> list[AuditLog]:
    """
    Recupera todo el histórico de cambios de una entidad específica.
    """
    return db.query(AuditLog).filter(
        AuditLog.entity_type == entity_type,
        AuditLog.entity_id == entity_id,
    ).order_by(AuditLog.created_at.desc()).all()
