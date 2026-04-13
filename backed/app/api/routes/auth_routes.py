from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.infrastructure.db.session import get_db
from app.core.config import settings
from app.schemas.auth_schema import (
    RegisterVendorRequest,
    LoginRequest,
    AuthResponse,
    VendorProfileResponse,
)
from app.services.auth_service import register_vendor, login_vendor, get_vendor_by_id

router = APIRouter()


@router.post("/auth/register", response_model=AuthResponse)
def auth_register(
    payload: RegisterVendorRequest,
    db: Session = Depends(get_db),
):
    result = register_vendor(db=db, payload=payload)
    return result


@router.post("/auth/login", response_model=AuthResponse)
def auth_login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    result = login_vendor(db=db, payload=payload)
    return result


@router.get("/auth/me", response_model=VendorProfileResponse)
def auth_me(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido.")

    token = authorization.replace("Bearer ", "").strip()

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        vendor_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="No fue posible validar el token.")

    vendor = get_vendor_by_id(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")

    return vendor
