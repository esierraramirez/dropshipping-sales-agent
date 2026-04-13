from typing import List, Optional, Literal
from pydantic import BaseModel, Field


OrderStatus = Literal["pending", "confirmed", "processed", "shipped", "cancelled"]


class OrderItemInput(BaseModel):
    product_id: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0)


class OrderCreateRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=150)
    customer_phone: str = Field(..., min_length=5, max_length=50)
    customer_address: Optional[str] = Field(default=None, max_length=500)
    items: List[OrderItemInput] = Field(..., min_length=1)


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    id: int
    vendor_id: int
    customer_name: str
    customer_phone: str
    customer_address: Optional[str] = None
    items: List[OrderItemResponse]
    total_amount: float
    status: str
    created_at: str


class OrderListResponse(BaseModel):
    vendor_name: str
    total_orders: int
    orders: List[OrderResponse]
