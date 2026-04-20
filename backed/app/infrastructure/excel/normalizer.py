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
    # Manejo especial para Series (cuando viene de iterrows)
    if isinstance(value, pd.Series):
        # Si es una Series, toma el primer valor
        value = value.iloc[0] if len(value) > 0 else ""
    
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
    Normaliza el DataFrame del catálogo de forma EXTREMADAMENTE tolerante.
    Casi nunca rechaza una fila - intenta rescatar cualquier dato posible.
    """
    normalized_rows: List[Dict[str, Any]] = []
    invalid_rows = 0
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    for index, row in df.iterrows():
        try:
            # Convertir row a diccionario para asegurar acceso a valores escalares
            row_dict = row.to_dict() if hasattr(row, 'to_dict') else dict(row)
            
            product_id = normalize_text(row_dict.get("product_id", ""))
            name = normalize_text(row_dict.get("name", ""))
            
            # ESTRATEGIA DE RESCATE #1: Generar product_id si falta
            if not product_id:
                # Intenta usar nombre como base
                if name:
                    product_id = name.replace(" ", "_")[:30]
                else:
                    # Última opción: usar índice
                    product_id = f"PROD_{index+1:05d}"
                
                warnings.append({
                    "row_index": int(index),
                    "warning": "product_id generado automáticamente",
                    "generated_id": product_id
                })
            
            # ESTRATEGIA DE RESCATE #2: Generar nombre si falta
            if not name or len(name) < 2:
                name = f"Producto {product_id}"
                warnings.append({
                    "row_index": int(index),
                    "warning": "nombre generado automáticamente"
                })
            
            # ESTRATEGIA DE RESCATE #3: Manejar shipping days
            min_shipping = normalize_int(row_dict.get("min_shipping_days", 1))
            max_shipping = normalize_int(row_dict.get("max_shipping_days", 7))
            
            # Si ambos son 0, usar valores por defecto
            if min_shipping == 0 and max_shipping == 0:
                min_shipping, max_shipping = 1, 7
            # Si solo max es 0, usar min
            elif max_shipping == 0:
                max_shipping = min_shipping if min_shipping > 0 else 7
            # Si solo min es 0, dejar max
            elif min_shipping == 0:
                min_shipping = max_shipping if max_shipping > 0 else 1
            
            # Si max < min, intercambiar
            if max_shipping < min_shipping:
                min_shipping, max_shipping = max_shipping, min_shipping
            
            normalized_row = {
                "product_id": product_id,
                "name": name,
                "category": normalize_category(row_dict.get("category", "General")),
                "price": normalize_price(row_dict.get("price", 0)),
                "currency": normalize_currency(row_dict.get("currency", "COP")),
                "stock_status": normalize_stock_status(row_dict.get("stock_status", "disponible")),
                "min_shipping_days": min_shipping,
                "max_shipping_days": max_shipping,
                "short_description": normalize_optional_text(row_dict.get("short_description", "")),
                "full_description": normalize_optional_text(row_dict.get("full_description", "")),
                "brand": normalize_optional_text(row_dict.get("brand", "")),
                "size": normalize_optional_text(row_dict.get("size", "")),
                "colors": normalize_optional_text(row_dict.get("colors", "")),
                "launch_year": normalize_int(row_dict.get("launch_year")) if not pd.isna(row_dict.get("launch_year")) else None,
                "sku": normalize_optional_text(row_dict.get("sku", "")),
                "shipping_cost": normalize_price(row_dict.get("shipping_cost", 0)) if not pd.isna(row_dict.get("shipping_cost")) else None,
                "shipping_regions": normalize_optional_text(row_dict.get("shipping_regions", "")),
                "returns_policy": normalize_optional_text(row_dict.get("returns_policy", "")),
                "warranty_policy": normalize_optional_text(row_dict.get("warranty_policy", "")),
                "specs": normalize_optional_text(row_dict.get("specs", "")),
                "variants": normalize_optional_text(row_dict.get("variants", "")),
                "source": normalize_optional_text(row_dict.get("source", "")),
            }

            normalized_rows.append(normalized_row)

        except Exception as e:
            invalid_rows += 1
            errors.append({
                "row_index": int(index),
                "error": str(e),
                "row_data": str(row.to_dict())
            })
            # Loguear pero continuar - no queremos perder el proceso
            import traceback
            print(f"⚠️ Error procesando fila {index}: {str(e)}")
            traceback.print_exc()
            continue

    # SI NO HAY FILAS VÁLIDAS, crear DataFrame con estructura correcta pero VACÍO
    # Esto evita el error de "No columns to parse"
    if not normalized_rows:
        print(f"⚠️ ADVERTENCIA: Todas las {len(df)} filas fueron rechazadas!")
        print(f"Errores encontrados: {errors}")
        normalized_df = pd.DataFrame(columns=[
            "product_id", "name", "category", "price", "currency", "stock_status",
            "min_shipping_days", "max_shipping_days", "short_description", "full_description",
            "brand", "size", "colors", "launch_year", "sku", "shipping_cost",
            "shipping_regions", "returns_policy", "warranty_policy", "specs", "variants", "source"
        ])
    else:
        normalized_df = pd.DataFrame(normalized_rows)

    quality_report = {
        "total_rows_input": int(len(df)),
        "valid_rows": int(len(normalized_df)),
        "invalid_rows": int(invalid_rows),
        "warnings": warnings,
        "errors": errors
    }

    print(f"✅ Normalización completada: {len(normalized_df)} filas válidas de {len(df)} totales")
    
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