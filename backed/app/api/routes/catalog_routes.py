from fastapi import APIRouter, UploadFile, File, Form

from app.schemas.catalog_upload_schema import CatalogUploadResponse
from app.services.catalog_service import process_catalog_upload

router = APIRouter()


@router.post("/catalog/upload", response_model=CatalogUploadResponse)
def upload_catalog(
    vendor_name: str = Form(...),
    file: UploadFile = File(...)
):
    return process_catalog_upload(file=file, vendor_name=vendor_name)