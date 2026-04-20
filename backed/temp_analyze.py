import pandas as pd
from pathlib import Path

try:
    df = pd.read_excel(r'C:\Users\USUARIO\Desktop\dropshipping-sales-agent\dropshipping-sales-agent\backed\data\raw\akari-cafe\20260419_222131_catalogo_tienda_ropa_30_productos.xlsx')
    print('✅ Archivo leído correctamente')
    print(f'\n📊 Dimensiones: {len(df)} filas x {len(df.columns)} columnas')
    print(f'\n📋 Columnas encontradas:')
    for i, col in enumerate(df.columns):
        print(f'  {i+1}. "{col}"')
    
    print(f'\n📄 Primeras 3 filas:')
    print(df.head(3).to_string())
    
    print(f'\n🔍 Análisis de datos nulos por columna:')
    for col in df.columns:
        null_count = df[col].isnull().sum()
        percent = (null_count / len(df)) * 100 if len(df) > 0 else 0
        print(f'  "{col}": {null_count} nulos ({percent:.1f}%)')
    
    print(f'\n✅ Archivo listo para procesar')
except Exception as e:
    print(f'❌ Error: {type(e).__name__}: {str(e)}')
    import traceback
    traceback.print_exc()
