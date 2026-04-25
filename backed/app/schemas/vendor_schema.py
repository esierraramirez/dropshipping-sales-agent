from typing import Optional
from pydantic import BaseModel, EmailStr


class VendorResponse(BaseModel):
    id: int
    name: str
    slug: str
    email: EmailStr
    rfc: Optional[str]
    sector: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    description: Optional[str]
    payment_methods: Optional[str]

    class Config:
        from_attributes = True


class VendorUpdateRequest(BaseModel):
    rfc: Optional[str] = None
    sector: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    description: Optional[str] = None
    payment_methods: Optional[str] = None
