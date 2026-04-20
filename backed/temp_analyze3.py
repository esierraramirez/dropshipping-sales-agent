import pandas as pd
import sys
sys.path.insert(0, r'C:\Users\USUARIO\Desktop\dropshipping-sales-agent\dropshipping-sales-agent\backed')

from app.infrastructure.excel.normalizer import normalize_dataframe

# Leer archivo original
df = pd.read_excel(r'C:\Users\USUARIO\Desktop\dropshipping-sales-agent\dropshipping-sales-agent\backed\data\raw\akari-cafe\20260419_222131_catalogo_tienda_ropa_30_productos.xlsx')

print("📊 DATOS ORIGINALES:")
print(f"  Filas: {len(df)}")
print(f"  Primeras 3 filas:\n{df.head(3)}\n")

# Normalizar
print("🔄 NORMALIZANDO...")
normalized_df, quality_report = normalize_dataframe(df)

print(f"\n📈 RESULTADO:")
print(f"  Filas válidas: {len(normalized_df)}")
print(f"  Filas rechazadas: {quality_report['invalid_rows']}")
print(f"\nReporte de calidad:")
print(f"  Total entrada: {quality_report['total_rows_input']}")
print(f"  Válidas: {quality_report['valid_rows']}")
print(f"  Inválidas: {quality_report['invalid_rows']}")

if quality_report['warnings']:
    print(f"\n⚠️  Advertencias ({len(quality_report['warnings'])}):")
    for w in quality_report['warnings'][:5]:
        print(f"    Fila {w.get('row_index')}: {w.get('warning')}")

if quality_report['errors']:
    print(f"\n❌ Errores ({len(quality_report['errors'])}):")
    for e in quality_report['errors'][:5]:
        print(f"    Fila {e.get('row_index')}: {e.get('error')}")

if len(normalized_df) > 0:
    print(f"\n✅ Primeras 3 filas normalizadas:\n{normalized_df.head(3)}")
else:
    print(f"\n❌ NO hay filas normalizadas!")
