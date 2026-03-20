from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db
from app.schemas.catalog_upload_schema import CatalogUploadResponse
from app.schemas.catalog_normalization_schema import CatalogNormalizationResponse
from app.schemas.product_response_schema import ProductListResponse
from app.schemas.knowledge_base_schema import KnowledgeBaseBuildResponse
from app.services.catalog_service import (
    process_catalog_upload,
    normalize_catalog_for_vendor,
    save_normalized_catalog_to_db,
    list_products_by_vendor,
    build_knowledge_base_for_vendor,
    get_knowledge_base_info,
)

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


@router.post("/catalog/save")
def save_catalog(
    vendor_name: str = Form(...),
    db: Session = Depends(get_db)
):
    return save_normalized_catalog_to_db(db=db, vendor_name=vendor_name)


@router.get("/catalog/products", response_model=ProductListResponse)
def get_vendor_products(
    vendor_name: str,
    db: Session = Depends(get_db)
):
    return list_products_by_vendor(db=db, vendor_name=vendor_name)


@router.post("/catalog/build-knowledge-base", response_model=KnowledgeBaseBuildResponse)
def build_knowledge_base(
    vendor_name: str = Form(...),
    db: Session = Depends(get_db)
):
    return build_knowledge_base_for_vendor(db=db, vendor_name=vendor_name)


@router.get("/catalog/knowledge-base")
def knowledge_base_info(vendor_name: str):
    return get_knowledge_base_info(vendor_name=vendor_name)