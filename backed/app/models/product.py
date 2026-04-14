from typing import Optional

from sqlalchemy import String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), nullable=False, index=True)

    product_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    stock_status: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, default="disponible")

    min_shipping_days: Mapped[int] = mapped_column(Integer, nullable=False)
    max_shipping_days: Mapped[int] = mapped_column(Integer, nullable=False)

    short_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    full_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    brand: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    shipping_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    shipping_regions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    returns_policy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    warranty_policy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    specs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    variants: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    vendor = relationship("Vendor", back_populates="products")