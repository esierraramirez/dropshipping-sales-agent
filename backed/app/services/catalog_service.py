from pathlib import Path
from datetime import datetime
import shutil
import re

from fastapi import UploadFile, HTTPException

from app.infrastructure.excel.importer import (
    read_excel_file,
    normalize_column_names,
    validate_required_columns,
    dataframe_preview,
    ensure_raw_vendor_directory,
)


RAW_DATA_PATH = "data/raw"


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

    df.columns = normalize_column_names(list(df.columns))
    detected_columns = list(df.columns)

    missing_columns = validate_required_columns(detected_columns)
    preview_rows = dataframe_preview(df, limit=10)

    return {
        "message": "Catálogo cargado y analizado correctamente.",
        "vendor_name": vendor_name,
        "original_filename": file.filename,
        "saved_path": saved_path,
        "detected_columns": detected_columns,
        "missing_required_columns": missing_columns,
        "preview_rows": preview_rows,
        "total_rows": len(df),
        "is_valid": len(missing_columns) == 0,
    }