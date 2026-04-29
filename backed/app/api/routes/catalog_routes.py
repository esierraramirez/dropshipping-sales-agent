from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
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
from app.models.product import Product

router = APIRouter()

# Carga un archivo Excel/CSV con el catálogo de productos del vendor.
@router.post("/catalog/upload/me", response_model=CatalogUploadResponse)
def upload_my_catalog(
    file: UploadFile = File(...),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return process_catalog_upload_for_vendor(file=file, vendor=current_vendor)

# Normaliza y valida el catálogo subido (valida campos, formatos, precios).
@router.post("/catalog/normalize/me", response_model=CatalogNormalizationResponse)
def normalize_my_catalog(
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return normalize_catalog_for_authenticated_vendor(vendor=current_vendor)

# Guarda el catálogo normalizado en la base de datos.
@router.post("/catalog/save/me")
def save_my_catalog(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return save_authenticated_vendor_catalog_to_db(db=db, vendor=current_vendor)

# Lista todos los productos del vendor autenticado.
@router.get("/catalog/products/me", response_model=ProductListResponse)
def get_my_products(
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    return list_authenticated_vendor_products(db=db, vendor=current_vendor)


# Lista productos filtrando explicitamente por atributos de negocio.
@router.get("/catalog/products/me/filter", response_model=ProductListResponse)
def filter_my_products(
    category: str | None = Query(default=None, min_length=1),
    stock_status: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    query = db.query(Product).filter(
        Product.vendor_id == current_vendor.id,
        Product.is_deleted == False,
    )

    if category:
        query = query.filter(Product.category.ilike(f"%{category.strip()}%"))

    if stock_status:
        query = query.filter(Product.stock_status == stock_status.strip())

    products = query.order_by(Product.name.asc()).all()

    return {
        "vendor_name": current_vendor.name,
        "total_products": len(products),
        "products": products,
    }

# Obtiene los detalles completos de un producto específico.
@router.get("/catalog/products/{product_id}")
def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.vendor_id == current_vendor.id,
        Product.is_deleted == False
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {
        "id": product.id,
        "vendor_id": product.vendor_id,
        "product_id": product.product_id,
        "name": product.name,
        "category": product.category,
        "price": float(product.price),
        "currency": product.currency,
        "stock_status": product.stock_status,
    }

# Actualiza campos de un producto (nombre, precio, stock, categoría).
@router.patch("/catalog/products/{product_id}")
def update_product(
    product_id: int,
    updates: dict,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.vendor_id == current_vendor.id,
        Product.is_deleted == False
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Actualizar solo los campos permitidos
    allowed_fields = {"name", "price", "stock_status", "category"}
    for field, value in updates.items():
        if field in allowed_fields and value is not None:
            setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return {
        "message": "Producto actualizado correctamente",
        "product": {
            "id": product.id,
            "product_id": product.product_id,
            "name": product.name,
            "price": float(product.price),
            "stock_status": product.stock_status,
        }
    }

# Elimina un producto del catálogo del vendor.
@router.delete("/catalog/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_vendor: Vendor = Depends(get_current_vendor),
):
    from app.services.audit_service import log_delete
    from datetime import datetime
    
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.vendor_id == current_vendor.id,
        Product.is_deleted == False
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product_name = product.name
    
    # Registrar en auditoría ANTES de eliminar
    log_delete(
        db=db,
        entity_type="Product",
        entity_id=product_id,
        entity_object=product,
        vendor=current_vendor,
        description=f"Producto eliminado: {product_name} (SKU: {product.product_id})"
    )
    
    # Soft delete: marcar como eliminado sin borrar datos
    product.is_deleted = True
    product.deleted_at = datetime.utcnow()
    db.commit()
    
    return {
        "message": f"Producto '{product_name}' eliminado correctamente (datos archivados para auditoría)",
        "product_id": product_id,
        "archived_at": product.deleted_at.isoformat()
    }

# Construye los embeddings semánticos del catálogo para búsqueda RAG (crítico para el agente).
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