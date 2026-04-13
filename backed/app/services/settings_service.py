from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.schemas.settings_schema import VendorSettingsUpsertRequest


def get_or_create_vendor_settings(db: Session, vendor: Vendor) -> VendorSettings:
    settings = db.query(VendorSettings).filter(VendorSettings.vendor_id == vendor.id).first()

    if settings:
        return settings

    settings = VendorSettings(
        vendor_id=vendor.id,
        business_start_hour=None,
        business_end_hour=None,
        off_hours_message="Hola, en este momento nos encontramos fuera de horario de atención. Déjanos tu mensaje y te responderemos pronto.",
        agent_enabled=True,
        tone="friendly",
    )

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


def get_settings_by_vendor_id(db: Session, vendor_id: int) -> VendorSettings:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")

    return get_or_create_vendor_settings(db=db, vendor=vendor)


def upsert_vendor_settings(
    db: Session,
    vendor_id: int,
    payload: VendorSettingsUpsertRequest,
) -> VendorSettings:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")

    settings = get_or_create_vendor_settings(db=db, vendor=vendor)

    settings.business_start_hour = payload.business_start_hour
    settings.business_end_hour = payload.business_end_hour
    settings.off_hours_message = payload.off_hours_message
    settings.agent_enabled = payload.agent_enabled
    settings.tone = payload.tone

    db.commit()
    db.refresh(settings)

    return settings
