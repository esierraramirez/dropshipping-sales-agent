from fastapi import APIRouter, UploadFile, File, Form

from app.schemas.catalog_upload_schema import CatalogUploadResponse
from app.schemas.catalog_normalization_schema import CatalogNormalizationResponse
from app.services.catalog_service import process_catalog_upload, normalize_catalog_for_vendor

router = APIRouter()


@router.post("/catalog/upload", response_model=CatalogUploadResponse)
def upload_catalog(
    vendor_name: str = Form(...),
    file: UploadFile = File(...)
):
    return process_catalog_upload(file=file, vendor_name=vendor_name)


@router.post("/catalog/normalize", response_model=CatalogNormalizationResponse)
def normalize_catalog(
    vendor_name: str = Form(...)
):
    return normalize_catalog_for_vendor(vendor_name=vendor_name)