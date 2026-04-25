import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.schemas.auth_schema import RegisterVendorRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def register_vendor(db: Session, payload: RegisterVendorRequest) -> dict:
    existing_email = db.query(Vendor).filter(Vendor.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Ya existe una empresa registrada con este correo.")

    vendor_slug = slugify(payload.name)
    existing_slug = db.query(Vendor).filter(Vendor.slug == vendor_slug).first()
    if existing_slug:
        raise HTTPException(status_code=400, detail="Ya existe una empresa registrada con ese nombre.")

    vendor = Vendor(
        name=payload.name,
        slug=vendor_slug,
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
        rfc=payload.rfc,
        sector=payload.sector,
        phone=payload.phone,
        website=payload.website,
        address=payload.address,
        city=payload.city,
        state=payload.state,
        country=payload.country or "México",
        postal_code=payload.postal_code,
        description=payload.description,
        payment_methods=payload.payment_methods,
    )

    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    token = create_access_token({"sub": str(vendor.id), "email": vendor.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "vendor": vendor,
    }


def login_vendor(db: Session, payload: LoginRequest) -> dict:
    vendor = db.query(Vendor).filter(Vendor.email == payload.email).first()
    if not vendor:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    if not verify_password(payload.password, vendor.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    if not vendor.is_active:
        raise HTTPException(status_code=403, detail="La empresa está inactiva.")

    token = create_access_token({"sub": str(vendor.id), "email": vendor.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "vendor": vendor,
    }


def get_vendor_by_id(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()
