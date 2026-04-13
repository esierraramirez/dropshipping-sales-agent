from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class VendorSettings(Base):
    __tablename__ = "vendor_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), unique=True, nullable=False)

    business_start_hour: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    business_end_hour: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    off_hours_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    agent_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    tone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    vendor = relationship("Vendor", back_populates="settings")