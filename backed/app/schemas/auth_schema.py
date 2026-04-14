from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterVendorRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    rfc: Optional[str] = Field(None, max_length=50)
    sector: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field("México", max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=2000)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class VendorProfileResponse(BaseModel):
    id: int
    name: str
    slug: str
    email: EmailStr
    is_active: bool
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

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    vendor: VendorProfileResponse
