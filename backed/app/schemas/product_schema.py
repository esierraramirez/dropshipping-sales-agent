from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


class ProductSchema(BaseModel):
    product_id: str = Field(..., min_length=1, description="Identificador único del producto")
    name: str = Field(..., min_length=3, description="Nombre del producto")
    category: str = Field(..., min_length=2, description="Categoría del producto")
    price: float = Field(..., ge=0, description="Precio del producto")
    currency: Literal["COP", "USD", "EUR"]
    stock_status: Literal["in_stock", "out_of_stock", "limited", "preorder"]
    min_shipping_days: int = Field(..., ge=0, description="Tiempo mínimo de envío")
    max_shipping_days: int = Field(..., ge=0, description="Tiempo máximo de envío")

    short_description: Optional[str] = Field(default=None, description="Descripción corta del producto")
    full_description: Optional[str] = Field(default=None, description="Descripción completa del producto")
    brand: Optional[str] = Field(default=None, description="Marca del producto")
    shipping_cost: Optional[float] = Field(default=None, ge=0, description="Costo de envío")
    shipping_regions: Optional[str] = Field(default=None, description="Regiones o ciudades de envío")
    returns_policy: Optional[str] = Field(default=None, description="Política de devoluciones")
    warranty_policy: Optional[str] = Field(default=None, description="Política de garantía")
    specs: Optional[str] = Field(default=None, description="Especificaciones técnicas")
    variants: Optional[str] = Field(default=None, description="Variantes del producto")
    source: Optional[str] = Field(default=None, description="Proveedor u origen del producto")

    @field_validator("max_shipping_days")
    @classmethod
    def validate_shipping_days(cls, value, info):
        min_days = info.data.get("min_shipping_days")
        if min_days is not None and value < min_days:
            raise ValueError("max_shipping_days must be greater than or equal to min_shipping_days")
        return value