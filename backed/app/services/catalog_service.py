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

    df.columns = normalize_column_names(list(df.columns))
    missing_columns = validate_required_columns(list(df.columns))

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"No es posible normalizar. Faltan columnas obligatorias: {missing_columns}"
        )

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