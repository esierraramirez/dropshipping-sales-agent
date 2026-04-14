from typing import Optional, List
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    vendor_id: int
    product_id: str
    name: str
    category: str
    price: float
    currency: str
    stock_status: Optional[str] = None
    min_shipping_days: int
    max_shipping_days: int
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    brand: Optional[str] = None
    shipping_cost: Optional[float] = None
    shipping_regions: Optional[str] = None
    returns_policy: Optional[str] = None
    warranty_policy: Optional[str] = None
    specs: Optional[str] = None
    variants: Optional[str] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    vendor_name: str
    total_products: int
    products: List[ProductResponse]