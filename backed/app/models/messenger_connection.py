from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class MessengerConnection(Base):
    __tablename__ = "messenger_connections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), unique=True, nullable=False)

    page_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)  # Facebook Page ID
    page_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Page name
    page_access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Token para enviar
    verify_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Token para verificar webhook
    
    is_connected: Mapped[bool] = mapped_column(Boolean, default=False)
    connected_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    vendor = relationship("Vendor", back_populates="messenger_connection")
