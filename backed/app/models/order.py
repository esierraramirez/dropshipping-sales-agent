from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), nullable=False, index=True)

    # Información del cliente
    customer_name: Mapped[str] = mapped_column(String(150), nullable=False)
    customer_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Productos de la orden
    items_json: Mapped[str] = mapped_column(Text, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Estado y seguimiento
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, confirmed, packed, shipped, delivered
    
    # Contexto conversacional
    conversation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    chat_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    vendor = relationship("Vendor", back_populates="orders")