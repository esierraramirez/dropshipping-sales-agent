#!/usr/bin/env python3
"""
Script de diagnóstico para validar archivos Excel antes de subirlos.
Uso: python validate_excel.py /ruta/al/archivo.xlsx
"""
import sys
import pandas as pd
from pathlib import Path


def validate_excel(file_path):
    """Valida un archivo Excel y reporta problemas."""
    
    print("=" * 60)
    print(f"🔍 Diagnosticando: {file_path}")
    print("=" * 60)
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"❌ ERROR: No se pudo leer el archivo")
        print(f"Detalles: {str(e)}")
        return False
    
    print(f"\n📊 Estructura del Excel:")
    print(f"  - Total de filas: {len(df)}")
    print(f"  - Total de columnas: {len(df.columns)}")
    print(f"  - Columnas encontradas: {list(df.columns)}")
    
    if len(df) == 0:
        print(f"\n❌ ERROR: El Excel está vacío (sin filas)")
        return False
    
    print(f"\n📝 Analizando datos:")
    
    # Verificar columnas críticas
    critical_columns = {
        "product_id": ["sku", "producto_id", "product_id", "codigo", "code"],
        "name": ["nombre", "product_name", "nombre_producto", "name"],
        "price": ["precio", "price", "costo", "cost"],
        "category": ["categoria", "category", "tipo", "type"],
    }
    
    found_columns = {}
    for critical, variations in critical_columns.items():
        found = False
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if col_lower in variations or col_lower == critical:
                found_columns[critical] = col
                found = True
                break
        
        if found:
            print(f"  ✅ {critical}: ENCONTRADO como '{found_columns[critical]}'")
        else:
            print(f"  ⚠️  {critical}: NO ENCONTRADO")
    
    # Analizar datos en las primeras 5 filas
    print(f"\n📄 Primeras 3 filas:")
    print(df.head(3).to_string())
    
    # Revisar valores nulos
    print(f"\n🔍 Análisis de datos nulos:")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            percent = (null_count / len(df)) * 100
            print(f"  - {col}: {null_count} nulos ({percent:.1f}%)")
    
    # Revisar product_id y name específicamente
    print(f"\n🆔 Analizando identificadores:")
    
    # Buscar columna product_id
    product_id_col = found_columns.get("product_id")
    if product_id_col:
        product_id_values = df[product_id_col].astype(str).str.strip()
        empty_ids = (product_id_values == "") | (product_id_values == "nan")
        valid_ids = (~empty_ids).sum()
        print(f"  - Columna: {product_id_col}")
        print(f"  - Valores válidos: {valid_ids}/{len(df)}")
        print(f"  - Ejemplos: {product_id_values.head(3).tolist()}")
    else:
        print(f"  ⚠️  No se encontró columna de product_id - se generará automáticamente")
    
    # Buscar columna name
    name_col = found_columns.get("name")
    if name_col:
        name_values = df[name_col].astype(str).str.strip()
        empty_names = (name_values == "") | (name_values == "nan")
        valid_names = (~empty_names).sum()
        print(f"  - Columna: {name_col}")
        print(f"  - Valores válidos: {valid_names}/{len(df)}")
        print(f"  - Ejemplos: {name_values.head(3).tolist()}")
    else:
        print(f"  ⚠️  No se encontró columna de name - se generará automáticamente")
    
    # Revisar precios
    price_col = found_columns.get("price")
    if price_col:
        print(f"  - Precios encontrados: {price_col}")
        prices = pd.to_numeric(df[price_col], errors='coerce')
        valid_prices = prices.notna().sum()
        print(f"  - Precios válidos: {valid_prices}/{len(df)}")
        print(f"  - Rango: {prices.min():.2f} - {prices.max():.2f}")
    
    print(f"\n✅ Resumen final:")
    if len(df) > 0:
        print(f"  ✅ El Excel se puede procesar")
        print(f"  ✅ Sistema completará datos faltantes automáticamente")
        print(f"\n➡️  Próximo paso: Sube este archivo en http://localhost:5173/catalog")
        return True
    else:
        print(f"  ❌ Imposible procesar: sin filas de datos")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python validate_excel.py /ruta/al/archivo.xlsx")
        print(f"\nEjemplo:")
        print(f"  python validate_excel.py data/raw/tienda-demo.xlsx")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"❌ Archivo no encontrado: {file_path}")
        sys.exit(1)
    
    success = validate_excel(str(file_path))
    sys.exit(0 if success else 1)
