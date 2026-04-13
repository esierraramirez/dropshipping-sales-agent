from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    products = relationship("Product", back_populates="vendor", cascade="all, delete-orphan")
    settings = relationship("VendorSettings", back_populates="vendor", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="vendor", cascade="all, delete-orphan")
    whatsapp_connection = relationship("WhatsAppConnection", back_populates="vendor", uselist=False, cascade="all, delete-orphan")