from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessengerConnectionRequest(BaseModel):
    """Request para crear/actualizar conexión de Messenger"""
    page_id: str = Field(..., description="Facebook Page ID")
    page_name: Optional[str] = Field(None, description="Nombre de la página")
    page_access_token: str = Field(..., description="Token de acceso de la página")
    verify_token: str = Field(..., description="Token para verificar webhook")


class MessengerConnectionResponse(BaseModel):
    """Response con datos de conexión de Messenger"""
    id: int
    vendor_id: int
    page_id: Optional[str]
    page_name: Optional[str]
    page_access_token: Optional[str]
    verify_token: Optional[str]
    is_connected: bool
    connected_at: Optional[datetime]

    class Config:
        from_attributes = True
