from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.vendor_schema import VendorResponse

router = APIRouter()

# Lista todos los vendors (empresas) registradas en el sistema (sin autenticación).
@router.get("/vendors", response_model=list[VendorResponse])
def list_vendors(
    db: Session = Depends(get_db)
):
    vendors = db.query(Vendor).order_by(Vendor.name.asc()).all()
    return vendors