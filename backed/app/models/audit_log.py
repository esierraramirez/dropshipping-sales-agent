from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class AuditLog(Base):
    """Tabla de auditoría para registrar cambios en modelos críticos"""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Información de la acción
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # created, updated, deleted, restored
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # "Product", "Order", "Vendor", etc.
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # ID del objeto modificado
    
    # Quién realizó la acción
    vendor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vendors.id"), nullable=True, index=True)
    
    # Datos antes y después (para DELETE: guardamos datos completos)
    old_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON stringificado
    new_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON stringificado
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Descripción legible de la acción
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # IP del cliente (si aplica)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    vendor = relationship("Vendor", foreign_keys=[vendor_id])
    
    def __repr__(self):
        return f"<AuditLog {self.action} {self.entity_type}#{self.entity_id} by vendor#{self.vendor_id} at {self.created_at}>"
