from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple, List

import pandas as pd


CATEGORY_MAP = {
    # Electronics & Technology
    "electronics": "Electronics",
    "electronica": "Electronics",
    "tecnologia": "Electronics",
    "tech": "Electronics",
    "computadores": "Electronics",
    "computers": "Electronics",
    "smartphones": "Electronics",
    "telefonos": "Electronics",
    "accesorios tecnologia": "Electronics",
    "gadgets": "Electronics",
    "audio": "Electronics",
    "camara": "Electronics",
    "cameras": "Electronics",
    
    # Fashion & Clothing
    "fashion": "Fashion",
    "moda": "Fashion",
    "ropa": "Fashion",
    "clothing": "Fashion",
    "zapatos": "Fashion",
    "shoes": "Fashion",
    "bolsas": "Fashion",
    "bags": "Fashion",
    "accesorios moda": "Fashion",
    "joyas": "Fashion",
    "jewelry": "Fashion",
    
    # Home & Kitchen
    "hogar": "Home",
    "home": "Home",
    "cocina": "Home",
    "kitchen": "Home",
    "muebles": "Home",
    "furniture": "Home",
    "decoracion": "Home",
    "decoration": "Home",
    "bedding": "Home",
    "ropa cama": "Home",
    
    # Sports & Outdoor
    "sports": "Sports",
    "deportes": "Sports",
    "outdoor": "Sports",
    "exterior": "Sports",
    "gym": "Sports",
    "fitness": "Sports",
    "camping": "Sports",
    "bicicleta": "Sports",
    "bicycles": "Sports",
    
    # Beauty & Personal Care
    "belleza": "Beauty",
    "beauty": "Beauty",
    "cosmeticos": "Beauty",
    "cosmetics": "Beauty",
    "skincare": "Beauty",
    "cuidado piel": "Beauty",
    "perfume": "Beauty",
    "fragrances": "Beauty",
    "hair": "Beauty",
    "cabello": "Beauty",
    
    # Health & Wellness
    "health": "Health",
    "salud": "Health",
    "wellness": "Health",
    "bienestar": "Health",
    "suplementos": "Health",
    "supplements": "Health",
    "vitaminas": "Health",
    "vitamins": "Health",
    
    # Books & Education
    "libros": "Books",
    "books": "Books",
    "educacion": "Books",
    "education": "Books",
    "ebooks": "Books",
    "cursos": "Books",
    "courses": "Books",
    
    # Toys & Games
    "juguetes": "Toys",
    "toys": "Toys",
    "juegos": "Toys",
    "games": "Toys",
    "puzzles": "Toys",
    "lego": "Toys",
    
    # Pet Supplies
    "mascotas": "Pets",
    "pets": "Pets",
    "perros": "Pets",
    "gatos": "Pets",
    "accesorios mascotas": "Pets",
    "alimento mascota": "Pets",
    
    # Garden & Outdoor
    "jardin": "Garden",
    "garden": "Garden",
    "plantas": "Garden",
    "herramientas": "Garden",
    "tools": "Garden",
    
    # Office & Stationery
    "oficina": "Office",
    "office": "Office",
    "papeleria": "Office",
    "stationery": "Office",
    "escritorio": "Office",
    
    # Travel & Luggage
    "viajes": "Travel",
    "travel": "Travel",
    "maletas": "Travel",
    "luggage": "Travel",
    "mochilas": "Travel",
    "backpacks": "Travel",
    
    # Automotive
    "auto": "Automotive",
    "automotive": "Automotive",
    "carro": "Automotive",
    "accesorios carro": "Automotive",
    "car accessories": "Automotive",
    
    # Handmade & Crafts
    "artesania": "Handmade",
    "handmade": "Handmade",
    "manualidades": "Handmade",
    "crafts": "Handmade",
    
    # Default
    "general": "General",
    "otro": "General",
    "other": "General",
}


STOCK_STATUS_MAP = {
    "in_stock": "in_stock",
    "disponible": "in_stock",
    "available": "in_stock",
    "agotado": "out_of_stock",
    "out_of_stock": "out_of_stock",
    "sin stock": "out_of_stock",
    "limited": "limited",
    "limitado": "limited",
    "preorder": "preorder",
    "preventa": "preorder",
}


CURRENCY_ALLOWED = {"COP", "USD", "EUR"}


def normalize_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_category(value: Any) -> str:
    text = normalize_text(value).lower()
    return CATEGORY_MAP.get(text, normalize_text(value).title())


def normalize_currency(value: Any) -> str:
    text = normalize_text(value).upper()
    if text in CURRENCY_ALLOWED:
        return text
    return "COP"


def normalize_stock_status(value: Any) -> str:
    text = normalize_text(value).lower()
    return STOCK_STATUS_MAP.get(text, "out_of_stock")


def normalize_price(value: Any) -> float:
    if pd.isna(value):
        return 0.0

    text = str(value).strip()

    # Eliminar símbolos de moneda y espacios
    text = re.sub(r"[^\d,.\-]", "", text)

    # Casos:
    # 129900
    # 129,900
    # 129.900
    # 129,900.50
    # 129.900,50
    if "," in text and "." in text:
        # Si el último separador es coma, asumimos formato europeo
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    else:
        # Si solo hay comas y parece separador de miles
        if text.count(",") == 1 and len(text.split(",")[-1]) == 3:
            text = text.replace(",", "")
        # Si solo hay puntos y parece separador de miles
        elif text.count(".") == 1 and len(text.split(".")[-1]) == 3:
            text = text.replace(".", "")
        else:
            text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return 0.0


def normalize_int(value: Any) -> int:
    if pd.isna(value):
        return 0
    text = re.sub(r"[^\d\-]", "", str(value))
    try:
        return max(0, int(text))
    except ValueError:
        return 0


def normalize_optional_text(value: Any) -> str | None:
    text = normalize_text(value)
    return text if text else None


def normalize_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Normaliza el DataFrame del catálogo y retorna:
    - DataFrame normalizado
    - quality_report
    """
    normalized_rows: List[Dict[str, Any]] = []
    invalid_rows = 0
    errors: List[Dict[str, Any]] = []

    for index, row in df.iterrows():
        try:
            normalized_row = {
                "product_id": normalize_text(row.get("product_id")),
                "name": normalize_text(row.get("name")),
                "category": normalize_category(row.get("category")),
                "price": normalize_price(row.get("price")),
                "currency": normalize_currency(row.get("currency")),
                "stock_status": normalize_stock_status(row.get("stock_status")),
                "min_shipping_days": normalize_int(row.get("min_shipping_days")),
                "max_shipping_days": normalize_int(row.get("max_shipping_days")),
                "short_description": normalize_optional_text(row.get("short_description")),
                "full_description": normalize_optional_text(row.get("full_description")),
                "brand": normalize_optional_text(row.get("brand")),
                "size": normalize_optional_text(row.get("size")),
                "colors": normalize_optional_text(row.get("colors")),
                "launch_year": normalize_int(row.get("launch_year")) if not pd.isna(row.get("launch_year")) else None,
                "sku": normalize_optional_text(row.get("sku")),
                "shipping_cost": normalize_price(row.get("shipping_cost")) if not pd.isna(row.get("shipping_cost")) else None,
                "shipping_regions": normalize_optional_text(row.get("shipping_regions")),
                "returns_policy": normalize_optional_text(row.get("returns_policy")),
                "warranty_policy": normalize_optional_text(row.get("warranty_policy")),
                "specs": normalize_optional_text(row.get("specs")),
                "variants": normalize_optional_text(row.get("variants")),
                "source": normalize_optional_text(row.get("source")),
            }

            # Validaciones mínimas de fila
            if not normalized_row["product_id"]:
                raise ValueError("product_id vacío")
            if len(normalized_row["name"]) < 3:
                raise ValueError("name demasiado corto")
            if normalized_row["max_shipping_days"] < normalized_row["min_shipping_days"]:
                raise ValueError("max_shipping_days menor que min_shipping_days")

            normalized_rows.append(normalized_row)

        except Exception as e:
            invalid_rows += 1
            errors.append({
                "row_index": int(index),
                "error": str(e)
            })

    normalized_df = pd.DataFrame(normalized_rows)

    quality_report = {
        "total_rows_input": int(len(df)),
        "valid_rows": int(len(normalized_df)),
        "invalid_rows": int(invalid_rows),
        "errors": errors
    }

    return normalized_df, quality_report


def ensure_processed_vendor_directory(base_path: str, vendor_slug: str) -> Path:
    vendor_dir = Path(base_path) / vendor_slug
    vendor_dir.mkdir(parents=True, exist_ok=True)
    return vendor_dir


def save_processed_outputs(
    normalized_df: pd.DataFrame,
    quality_report: Dict[str, Any],
    base_path: str,
    vendor_slug: str
) -> Tuple[str, str, str]:
    vendor_dir = ensure_processed_vendor_directory(base_path, vendor_slug)

    csv_path = vendor_dir / "catalog_normalized.csv"
    jsonl_path = vendor_dir / "catalog_normalized.jsonl"
    report_path = vendor_dir / "data_quality_report.json"

    normalized_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for record in normalized_df.to_dict(orient="records"):
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(quality_report, f, ensure_ascii=False, indent=2)

    return str(csv_path), str(jsonl_path), str(report_path)