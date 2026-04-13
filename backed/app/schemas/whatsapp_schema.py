from typing import Optional
from pydantic import BaseModel, Field


class WhatsAppConnectionRequest(BaseModel):
    phone_number_id: str = Field(..., min_length=1, max_length=150)
    business_account_id: Optional[str] = Field(default=None, max_length=150)
    access_token: str = Field(..., min_length=10)
    verify_token: str = Field(..., min_length=6, max_length=255)


class WhatsAppConnectionResponse(BaseModel):
    vendor_id: int
    phone_number_id: Optional[str] = None
    business_account_id: Optional[str] = None
    is_connected: bool
    verify_token: Optional[str] = None

    class Config:
        from_attributes = True
