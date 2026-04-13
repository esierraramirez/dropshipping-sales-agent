from fastapi import APIRouter, Depends, Header, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.db.session import get_db
from app.schemas.settings_schema import (
    VendorSettingsUpsertRequest,
    VendorSettingsResponse,
)
from app.services.auth_service import get_vendor_by_id
from app.services.settings_service import (
    get_settings_by_vendor_id,
    upsert_vendor_settings,
)

router = APIRouter()


def get_current_vendor_id(authorization: str) -> int:
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
        return vendor_id
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="No fue posible validar el token.")


@router.get("/settings/me", response_model=VendorSettingsResponse)
def get_my_settings(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    vendor_id = get_current_vendor_id(authorization)
    settings_obj = get_settings_by_vendor_id(db=db, vendor_id=vendor_id)
    return settings_obj


@router.put("/settings/me", response_model=VendorSettingsResponse)
def update_my_settings(
    payload: VendorSettingsUpsertRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    vendor_id = get_current_vendor_id(authorization)

    vendor = get_vendor_by_id(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")

    settings_obj = upsert_vendor_settings(
        db=db,
        vendor_id=vendor_id,
        payload=payload,
    )
    return settings_obj
