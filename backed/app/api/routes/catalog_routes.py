from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.api.deps import get_current_vendor
from app.models.vendor import Vendor

from app.schemas.catalog_upload_schema import CatalogUploadResponse
from app.schemas.catalog_normalization_schema import CatalogNormalizationResponse
from app.schemas.product_response_schema import ProductListResponse
from app.schemas.knowledge_base_schema import KnowledgeBaseBuildResponse

from app.services.catalog_service import (
    process_catalog_upload_for_vendor,
    normalize_catalog_for_authenticated_vendor,
    save_authenticated_vendor_catalog_to_db,
    list_authenticated_vendor_products,
    build_authenticated_vendor_knowledge_base,
    get_authenticated_vendor_knowledge_base_info,
)

router = APIRouter()


@router.post("/catalog/upload/me", response_model=CatalogUploadResponse)
def upload_my_catalog(
    file: UploadFile = File(...),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return process_catalog_upload_for_vendor(file=file, vendor=current_vendor)


@router.post("/catalog/normalize/me", response_model=CatalogNormalizationResponse)
def normalize_my_catalog(
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return normalize_catalog_for_authenticated_vendor(vendor=current_vendor)


@router.post("/catalog/save/me")
def save_my_catalog(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return save_authenticated_vendor_catalog_to_db(db=db, vendor=current_vendor)


@router.get("/catalog/products/me", response_model=ProductListResponse)
def get_my_products(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return list_authenticated_vendor_products(db=db, vendor=current_vendor)


@router.post("/catalog/build-knowledge-base/me", response_model=KnowledgeBaseBuildResponse)
def build_my_knowledge_base(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return build_authenticated_vendor_knowledge_base(db=db, vendor=current_vendor)


@router.get("/catalog/knowledge-base/me")
def get_my_knowledge_base(
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return get_authenticated_vendor_knowledge_base_info(vendor=current_vendor)