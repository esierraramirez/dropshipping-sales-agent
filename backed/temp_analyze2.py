import pandas as pd
import numpy as np
from pathlib import Path

df = pd.read_excel(r'C:\Users\USUARIO\Desktop\dropshipping-sales-agent\dropshipping-sales-agent\backed\data\raw\akari-cafe\20260419_222131_catalogo_tienda_ropa_30_productos.xlsx')

print("🔍 ANÁLISIS PROFUNDO DE DATOS PROBLEMÁTICOS\n")

# Analizar min_shipping_days y max_shipping_days específicamente
print("📊 min_shipping_days:")
for i, val in enumerate(df['min_shipping_days']):
    print(f"  Fila {i}: type={type(val).__name__}, value={repr(val)}, pd.isna={pd.isna(val)}")
    if i >= 5:
        print(f"  ... (y {len(df)-6} más)")
        break

print("\n📊 max_shipping_days:")
for i, val in enumerate(df['max_shipping_days']):
    print(f"  Fila {i}: type={type(val).__name__}, value={repr(val)}, pd.isna={pd.isna(val)}")
    if i >= 5:
        print(f"  ... (y {len(df)-6} más)")
        break

# Probar conversiones que hace el normalize
print("\n🔧 Simulando conversiones de normalize_int:")

def normalize_int(value):
    import re
    if pd.isna(value):
        return 0
    text = re.sub(r"[^\d\-]", "", str(value))
    try:
        return max(0, int(text))
    except ValueError:
        return 0

for i in range(min(3, len(df))):
    min_val = df['min_shipping_days'].iloc[i]
    max_val = df['max_shipping_days'].iloc[i]
    norm_min = normalize_int(min_val)
    norm_max = normalize_int(max_val)
    print(f"  Fila {i}: min({repr(min_val)})→{norm_min}, max({repr(max_val)})→{norm_max}")

print("\n✅ Análisis completado")
