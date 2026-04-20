from pathlib import Path
from datetime import datetime
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.vendor import Vendor
from app.models.product import Product
from app.rag.documents import product_to_document
from app.rag.inderex import save_knowledge_base_jsonl, build_basic_keyword_index
import shutil
import json
import re

from app.infrastructure.excel.importer import (
    read_excel_file,
    normalize_column_names,
    validate_required_columns,
    dataframe_preview,
    ensure_raw_vendor_directory,
)
from app.infrastructure.excel.normalizer import (
    normalize_dataframe,
    save_processed_outputs,
)


RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def save_uploaded_excel(file: UploadFile, vendor_name: str) -> str:
    if not file.filename:
        raise HTTPException(status_code=400, detail="El archivo no tiene nombre.")

    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos .xlsx")

    vendor_slug = slugify(vendor_name)
    vendor_dir = ensure_raw_vendor_directory(RAW_DATA_PATH, vendor_slug)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    saved_path = vendor_dir / safe_filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(saved_path)


def process_catalog_upload(file: UploadFile, vendor_name: str) -> dict:
    saved_path = save_uploaded_excel(file, vendor_name)

    try:
        df = read_excel_file(saved_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No fue posible leer el archivo Excel: {str(e)}")

    # Normalizar nombres de columnas
    original_columns = list(df.columns)
    df.columns = normalize_column_names(original_columns)
    detected_columns = list(df.columns)

    # Validar columnas requeridas
    validation = validate_required_columns(detected_columns)
    
    # Agregar columnas faltantes con valores por defecto
    from app.infrastructure.excel.importer import OPTIONAL_COLUMNS
    for col, default_val in OPTIONAL_COLUMNS.items():
        if col not in df.columns:
            df[col] = default_val
    
    preview_rows = dataframe_preview(df, limit=10)

    return {
        "message": "Catálogo cargado y analizado correctamente." if validation["is_valid"] else validation["message"],
        "vendor_name": vendor_name,
        "original_filename": file.filename,
        "saved_path": saved_path,
        "detected_columns": detected_columns,
        "original_columns": original_columns,
        "missing_required_columns": validation["missing"],
        "validation_details": validation,
        "preview_rows": preview_rows,
        "total_rows": len(df),
        "is_valid": validation["is_valid"],
    }


def get_latest_raw_catalog_path(vendor_name: str) -> str:
    vendor_slug = slugify(vendor_name)
    vendor_dir = Path(RAW_DATA_PATH) / vendor_slug

    if not vendor_dir.exists():
        raise HTTPException(status_code=404, detail="No existe catálogo cargado para este vendedor.")

    files = sorted(vendor_dir.glob("*.xlsx"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not files:
        raise HTTPException(status_code=404, detail="No se encontraron archivos Excel para este vendedor.")

    return str(files[0])


def normalize_catalog_for_vendor(vendor_name: str) -> dict:
    source_file = get_latest_raw_catalog_path(vendor_name)

    try:
        df = read_excel_file(source_file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No fue posible leer el archivo Excel: {str(e)}")

    # Normalizar nombres de columnas y mapear español/inglés
    df.columns = normalize_column_names(list(df.columns))
    validation = validate_required_columns(list(df.columns))

    if not validation["is_valid"]:
        raise HTTPException(
            status_code=400,
            detail=f"No es posible normalizar. Faltan columnas obligatorias: {validation['missing']}"
        )

    # Agregar columnas opcionales con valores por defecto si no existen
    from app.infrastructure.excel.importer import OPTIONAL_COLUMNS
    for col, default_val in OPTIONAL_COLUMNS.items():
        if col not in df.columns:
            df[col] = default_val

    normalized_df, quality_report = normalize_dataframe(df)

    vendor_slug = slugify(vendor_name)
    csv_path, jsonl_path, report_path = save_processed_outputs(
        normalized_df=normalized_df,
        quality_report=quality_report,
        base_path=PROCESSED_DATA_PATH,
        vendor_slug=vendor_slug
    )

    preview_rows = dataframe_preview(normalized_df, limit=10)

    return {
        "message": "Catálogo normalizado correctamente.",
        "vendor_name": vendor_name,
        "source_file": source_file,
        "processed_csv_path": csv_path,
        "processed_jsonl_path": jsonl_path,
        "quality_report_path": report_path,
        "total_rows": int(quality_report["total_rows_input"]),
        "valid_rows": int(quality_report["valid_rows"]),
        "invalid_rows": int(quality_report["invalid_rows"]),
        "preview_rows": preview_rows,
    }
    
def get_or_create_vendor(db: Session, vendor_name: str) -> Vendor:
    vendor_slug = slugify(vendor_name)

    vendor = db.query(Vendor).filter(Vendor.slug == vendor_slug).first()
    if vendor:
        return vendor

    vendor = Vendor(name=vendor_name, slug=vendor_slug)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


def save_normalized_catalog_to_db(db: Session, vendor_name: str) -> dict:
    vendor = get_or_create_vendor(db, vendor_name)

    vendor_slug = slugify(vendor_name)
    processed_file = Path(PROCESSED_DATA_PATH) / vendor_slug / "catalog_normalized.csv"
    report_file = Path(PROCESSED_DATA_PATH) / vendor_slug / "data_quality_report.json"

    if not processed_file.exists():
        raise HTTPException(
            status_code=404,
            detail="No existe catálogo normalizado para este vendedor. Primero debes ejecutar /catalog/normalize"
        )

    df = read_excel_file(str(processed_file)) if processed_file.suffix == ".xlsx" else None
    if df is None:
        import pandas as pd
        try:
            df = pd.read_csv(processed_file)
        except pd.errors.EmptyDataError:
            # Leer reporte de calidad para dar más contexto
            quality_report = {}
            if report_file.exists():
                with open(report_file, "r") as f:
                    quality_report = json.load(f)
            
            error_detail = "El archivo CSV normalizado está vacío."
            if quality_report:
                warnings = quality_report.get("warnings", [])
                errors = quality_report.get("errors", [])
                if warnings:
                    error_detail += f"\nAdvertencias durante normalización: {len(warnings)}"
                if errors:
                    error_detail += f"\nErrores: {len(errors)} - {errors[:2]}"  # Mostrar primeros 2
            
            raise HTTPException(
                status_code=400,
                detail=error_detail + "\nVerifica que tu Excel tenga al menos una fila de datos válida con product_id y name."
            )
    
    # Validar que hay al menos una fila
    if len(df) == 0:
        # Leer reporte de calidad
        quality_report = {}
        if report_file.exists():
            with open(report_file, "r") as f:
                quality_report = json.load(f)
        
        error_message = "No hay productos válidos en el catálogo normalizado."
        if quality_report:
            total_input = quality_report.get("total_rows_input", 0)
            invalid = quality_report.get("invalid_rows", 0)
            warnings = quality_report.get("warnings", [])
            errors = quality_report.get("errors", [])
            
            error_message += f"\n\nReporte de Normalización:"
            error_message += f"\n- Filas en Excel: {total_input}"
            error_message += f"\n- Filas rechazadas: {invalid}"
            error_message += f"\n- Advertencias: {len(warnings)}"
            
            if errors:
                error_message += f"\n- Errores encontrados:"
                for err in errors[:3]:  # Mostrar primeros 3 errores
                    error_message += f"\n  Fila {err.get('row_index')}: {err.get('error')}"
        
        raise HTTPException(
            status_code=400,
            detail=error_message
        )

    # Limpiar productos previos del vendedor para reemplazar el catálogo actual
    db.query(Product).filter(Product.vendor_id == vendor.id).delete()
    db.commit()

    inserted = 0

    for idx, (_, row) in enumerate(df.iterrows()):
        try:
            # Helper functions para manejar conversiones con valores inválidos/NaN
            def safe_float(value, default=0.0):
                if value is None or value == "" or (isinstance(value, float) and pd.isna(value)):
                    return default
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default
            
            def safe_int(value, default=0):
                if value is None or value == "":
                    return default
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return default
            
            product = Product(
                vendor_id=vendor.id,
                product_id=str(row.get("product_id", "")).strip(),
                name=str(row.get("name", "")).strip(),
                category=str(row.get("category", "")).strip(),
                price=safe_float(row.get("price", 0), 0.0),  # Nunca None
                currency=str(row.get("currency", "COP")).strip(),
                stock_status=str(row.get("stock_status", "out_of_stock")).strip(),
                min_shipping_days=safe_int(row.get("min_shipping_days", 0), 0),  # Nunca None
                max_shipping_days=safe_int(row.get("max_shipping_days", 0), 0),  # Nunca None
                short_description=row.get("short_description") if row.get("short_description") else None,
                full_description=row.get("full_description") if row.get("full_description") else None,
                brand=row.get("brand") if row.get("brand") else None,
                shipping_cost=safe_float(row.get("shipping_cost"), None),  # Puede ser None (opcional)
                shipping_regions=row.get("shipping_regions") if row.get("shipping_regions") else None,
                returns_policy=row.get("returns_policy") if row.get("returns_policy") else None,
                warranty_policy=row.get("warranty_policy") if row.get("warranty_policy") else None,
                specs=row.get("specs") if row.get("specs") else None,
                variants=row.get("variants") if row.get("variants") else None,
                source=row.get("source") if row.get("source") else None,
            )
            db.add(product)
            inserted += 1
            print(f"[Row {idx+1}] Producto insertado: {product.product_id}")
        except Exception as e:
            # Log error pero continúa con siguiente producto
            import traceback
            print(f"[Row {idx+1}] Error procesando producto {row.get('product_id', 'UNKNOWN')}: {str(e)}")
            traceback.print_exc()
            continue
    
    print(f"Total a insertar: {inserted}")
    db.commit()
    print(f"Base de datos actualizada con {inserted} productos")

    return {
        "message": "Catálogo almacenado en base de datos correctamente.",
        "vendor_id": vendor.id,
        "vendor_name": vendor.name,
        "inserted_products": inserted
    }


def list_products_by_vendor(db: Session, vendor_name: str) -> dict:
    vendor_slug = slugify(vendor_name)

    vendor = db.query(Vendor).filter(Vendor.slug == vendor_slug).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado.")

    products = db.query(Product).filter(Product.vendor_id == vendor.id).order_by(Product.name.asc()).all()

    return {
        "vendor_name": vendor.name,
        "total_products": len(products),
        "products": products
    }

def build_knowledge_base_for_vendor(db: Session, vendor_name: str) -> dict:
    vendor_slug = slugify(vendor_name)

    vendor = db.query(Vendor).filter(Vendor.slug == vendor_slug).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado.")

    products = db.query(Product).filter(Product.vendor_id == vendor.id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No hay productos cargados para este vendedor.")

    documents = []
    for product in products:
        product_dict = {
            "vendor_id": product.vendor_id,
            "product_id": product.product_id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "currency": product.currency,
            "stock_status": product.stock_status,
            "min_shipping_days": product.min_shipping_days,
            "max_shipping_days": product.max_shipping_days,
            "short_description": product.short_description,
            "full_description": product.full_description,
            "brand": product.brand,
            "shipping_cost": product.shipping_cost,
            "shipping_regions": product.shipping_regions,
            "returns_policy": product.returns_policy,
            "warranty_policy": product.warranty_policy,
            "specs": product.specs,
            "variants": product.variants,
            "source": product.source,
        }
        documents.append(product_to_document(product_dict))

    kb_dir = Path("data/index") / vendor_slug
    knowledge_base_path = kb_dir / "knowledge_base.jsonl"
    index_path = kb_dir / "keyword_index.json"

    save_knowledge_base_jsonl(documents, str(knowledge_base_path))
    build_basic_keyword_index(documents, str(index_path))

    return {
        "message": "Base de conocimiento construida correctamente.",
        "vendor_name": vendor.name,
        "total_products": len(products),
        "documents_created": len(documents),
        "knowledge_base_path": str(knowledge_base_path),
        "index_path": str(index_path),
        "preview_documents": documents[:3]
    }


def get_knowledge_base_info(vendor_name: str) -> dict:
    vendor_slug = slugify(vendor_name)
    kb_dir = Path("data/index") / vendor_slug

    knowledge_base_path = kb_dir / "knowledge_base.jsonl"
    index_path = kb_dir / "keyword_index.json"

    if not knowledge_base_path.exists() or not index_path.exists():
        raise HTTPException(
            status_code=404,
            detail="La base de conocimiento aún no ha sido construida para este vendedor."
        )

    preview_documents = []
    with knowledge_base_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 3:
                break
            preview_documents.append(json.loads(line))

    return {
        "message": "Base de conocimiento encontrada.",
        "vendor_name": vendor_name,
        "knowledge_base_path": str(knowledge_base_path),
        "index_path": str(index_path),
        "preview_documents": preview_documents
    }


# Nuevas funciones para trabajar con Vendor autenticado


def process_catalog_upload_for_vendor(file: UploadFile, vendor: Vendor) -> dict:
    return process_catalog_upload(file=file, vendor_name=vendor.name)


def normalize_catalog_for_authenticated_vendor(vendor: Vendor) -> dict:
    return normalize_catalog_for_vendor(vendor_name=vendor.name)


def save_authenticated_vendor_catalog_to_db(db: Session, vendor: Vendor) -> dict:
    """
    Guarda catálogo a la base de datos del vendor autenticado.
    Si no existe CSV normalizado, lo normaliza automáticamente.
    """
    vendor_slug = vendor.slug
    processed_file = Path(PROCESSED_DATA_PATH) / vendor_slug / "catalog_normalized.csv"
    
    # Si no existe CSV normalizado, normalizarlo primero
    if not processed_file.exists():
        try:
            # Intentar normalizar automáticamente desde el Excel más reciente
            normalize_result = normalize_catalog_for_vendor(vendor_name=vendor.name)
            print(f"📝 Catálogo normalizado automáticamente: {normalize_result}")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"No existe catálogo normalizado. Primero debes subir un Excel y normalizarlo. Error: {str(e)}"
            )
    
    # Verificar que el CSV existe y tiene contenido
    if not processed_file.exists():
        raise HTTPException(
            status_code=400,
            detail=f"El archivo normalizado no se creó correctamente. Verifica tu Excel."
        )
    
    return save_normalized_catalog_to_db(db=db, vendor_name=vendor.name)


def list_authenticated_vendor_products(db: Session, vendor: Vendor) -> dict:
    return list_products_by_vendor(db=db, vendor_name=vendor.name)


def build_authenticated_vendor_knowledge_base(db: Session, vendor: Vendor) -> dict:
    return build_knowledge_base_for_vendor(db=db, vendor_name=vendor.name)


def get_authenticated_vendor_knowledge_base_info(vendor: Vendor) -> dict:
    return get_knowledge_base_info(vendor_name=vendor.name)