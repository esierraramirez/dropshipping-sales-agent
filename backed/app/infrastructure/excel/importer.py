from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


REQUIRED_COLUMNS = [
    "product_id",
    "name",
    "category",
    "price",
    "currency",
    "stock_status",
    "min_shipping_days",
    "max_shipping_days",
]


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Lee un archivo Excel y retorna un DataFrame.
    """
    return pd.read_excel(file_path)


def normalize_column_names(columns: List[str]) -> List[str]:
    """
    Normaliza los nombres de las columnas:
    - minúsculas
    - sin espacios al inicio/final
    - espacios reemplazados por _
    """
    normalized = []
    for col in columns:
        col = str(col).strip().lower().replace(" ", "_")
        normalized.append(col)
    return normalized


def validate_required_columns(columns: List[str]) -> List[str]:
    """
    Retorna las columnas obligatorias faltantes.
    """
    return [col for col in REQUIRED_COLUMNS if col not in columns]


def dataframe_preview(df: pd.DataFrame, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retorna las primeras filas como lista de diccionarios.
    """
    preview_df = df.head(limit).fillna("")
    return preview_df.to_dict(orient="records")


def ensure_raw_vendor_directory(base_path: str, vendor_slug: str) -> Path:
    """
    Crea la carpeta raw del vendedor si no existe.
    """
    vendor_dir = Path(base_path) / vendor_slug
    vendor_dir.mkdir(parents=True, exist_ok=True)
    return vendor_dir