from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import unicodedata


# Mapeo de columnas en español/inglés a columnas estandarizadas
COLUMN_MAPPING = {
    # product_id
    "sku": "product_id",
    "producto_id": "product_id",
    "product_id": "product_id",
    "codigo": "product_id",
    "code": "product_id",
    
    # name
    "nombre": "name",
    "product_name": "name",
    "nombre_producto": "name",
    "name": "name",
    
    # category
    "categoria": "category",
    "category": "category",
    "tipo": "category",
    "type": "category",
    
    # price
    "precio": "price",
    "price": "price",
    "costo": "price",
    "cost": "price",
    
    # currency
    "moneda": "currency",
    "currency": "currency",
    "divisa": "currency",
    
    # stock
    "stock": "stock_status",
    "stock_status": "stock_status",
    "inventario": "stock_status",
    "cantidad": "stock_status",
    "cantidad_disponible": "stock_status",
    
    # description
    "descripcion": "description",
    "description": "description",
    "detalle": "description",
    "details": "description",
    
    # image
    "imagen_url": "image_url",
    "image_url": "image_url",
    "imagen": "image_url",
    "image": "image_url",
}

# Columnas obligatorias (sin valores por defecto)
REQUIRED_COLUMNS = ["product_id", "name", "category", "price", "currency"]

# Columnas opcionales con valores por defecto
OPTIONAL_COLUMNS = {
    "stock_status": "disponible",  # Estado por defecto para dropshipping
    "min_shipping_days": 1,
    "max_shipping_days": 7,
    "description": "",
    "image_url": "",
}


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Lee un archivo Excel y retorna un DataFrame.
    """
    return pd.read_excel(file_path)


def normalize_column_names(columns: List[str]) -> List[str]:
    """
    Normaliza y mapea los nombres de las columnas:
    - minúsculas
    - sin espacios al inicio/final
    - REMOVER ACENTOS (categoría -> categoria)
    - mapea nombres en español/inglés a inglés estándar
    - espacios reemplazados por _
    """
    def remove_accents(text):
        """Remueve acentos de texto Unicode"""
        nfkd = unicodedata.normalize('NFKD', text)
        return ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    normalized = []
    for col in columns:
        col = str(col).strip().lower()
        # REMOVER ACENTOS PRIMERO
        col = remove_accents(col)
        # Reemplazar espacios
        col = col.replace(" ", "_")
        # Usar mapeo si existe
        col = COLUMN_MAPPING.get(col, col)
        normalized.append(col)
    return normalized


def validate_required_columns(columns: List[str]) -> Dict[str, Any]:
    """
    Valida columnas requeridas y devuelve información detallada.
    Retorna:
    {
        'missing': ['col1', 'col2'],  # Columnas faltantes
        'is_valid': True/False,       # Si es válido
        'message': 'descripción'
    }
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in columns]
    
    return {
        "missing": missing,
        "is_valid": len(missing) == 0,
        "required_columns": REQUIRED_COLUMNS,
        "message": f"Faltan columnas: {', '.join(missing)}" if missing else "Todas las columnas requeridas están presentes"
    }


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