from pydantic import BaseModel, Field
from typing import Optional, List


class ChatMessage(BaseModel):
    """Un mensaje individual en el historial."""
    role: str = Field(..., description="'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")


class CartItem(BaseModel):
    """Un item en el carrito de compra del cliente."""
    product_id: str = Field(..., description="ID del producto")
    product_name: str = Field(..., description="Nombre del producto")
    quantity: int = Field(default=1, ge=1, description="Cantidad")
    unit_price: float = Field(..., gt=0, description="Precio unitario")


class PurchaseContext(BaseModel):
    """Contexto sobre la intención de compra del cliente."""
    customer_name: Optional[str] = Field(None, description="Nombre del cliente")
    customer_phone: Optional[str] = Field(None, description="Teléfono del cliente")
    customer_address: Optional[str] = Field(None, description="Dirección de envío")
    items: List[CartItem] = Field(default=[], description="Items a comprar")
    total_amount: float = Field(default=0.0, description="Monto total")
    is_confirmed: bool = Field(default=False, description="¿Cliente confirmó compra?")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=3000)
    history: Optional[List[ChatMessage]] = Field(
        default=None, 
        description="Historial de conversación anterior (opcional)"
    )
    purchase_context: Optional[PurchaseContext] = Field(
        default=None,
        description="Contexto de compra si está disponible"
    )


class ChatResponse(BaseModel):
    vendor_name: str
    user_message: str
    agent_response: str
    context_used: str
    matches_found: int
    purchase_context: Optional[PurchaseContext] = None
    order_created: Optional[dict] = None  # Si se creó una orden
