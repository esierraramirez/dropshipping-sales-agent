from pydantic import BaseModel, EmailStr, Field


class RegisterVendorRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class VendorProfileResponse(BaseModel):
    id: int
    name: str
    slug: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    vendor: VendorProfileResponse
