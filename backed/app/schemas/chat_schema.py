from pydantic import BaseModel, Field
from typing import Optional, List


class ChatMessage(BaseModel):
    """Un mensaje individual en el historial."""
    role: str = Field(..., description="'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=3000)
    history: Optional[List[ChatMessage]] = Field(
        default=None, 
        description="Historial de conversación anterior (opcional)"
    )


class ChatResponse(BaseModel):
    vendor_name: str
    user_message: str
    agent_response: str
    context_used: str
    matches_found: int
