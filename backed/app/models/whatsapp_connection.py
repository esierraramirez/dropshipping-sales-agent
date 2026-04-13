from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class WhatsAppConnection(Base):
    __tablename__ = "whatsapp_connections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), unique=True, nullable=False)

    phone_number_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    business_account_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verify_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    is_connected: Mapped[bool] = mapped_column(Boolean, default=False)
    connected_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    vendor = relationship("Vendor", back_populates="whatsapp_connection")