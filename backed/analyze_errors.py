#!/usr/bin/env python3
"""Analizar errores del Excel de pruebas KPI."""

import pandas as pd

df = pd.read_excel('data/reports/objective4_kpi_results.xlsx', sheet_name='detalle_pruebas')
errors = df[df['status'] == 'ERROR']

print('='*100)
print('ERRORES EN LAS PRUEBAS KPI OBJETIVO 4')
print('='*100)
print(f'\nTotal de errores: {len(errors)} de {len(df)} pruebas\n')

# Agrupar errores por tipo de query
error_by_type = errors.groupby('query_type').size()
print('Errores por tipo de query:')
for query_type, count in error_by_type.items():
    print(f'  - {query_type}: {count} errores')

# Mostrar detalles de algunos errores
print('\n' + '='*100)
print('DETALLE DE LOS ERRORES:')
print('='*100)

for idx, (i, row) in enumerate(errors.iterrows()):
    if idx >= 15:  # Mostrar máximo 15 errores para no saturar
        print(f'\n... y {len(errors) - idx} errores más')
        break
    
    print(f"\n[{idx+1}] Test #{row['case_id']} - {row['query_type']}")
    print(f"  Mensaje: {row['message'][:80]}")
    print(f"  Error: {row['error'][:150] if pd.notna(row['error']) else 'N/A'}")
    response = row['assistant_response']
    if pd.isna(response) or response == '':
        print(f"  ⚠️  Respuesta EN BLANCO")
    else:
        print(f"  Respuesta: {str(response)[:100]}")
    print(f"  Order Created: {row['order_created']}")

# Análisis de respuestas en blanco
print('\n' + '='*100)
print('ANÁLISIS DE RESPUESTAS EN BLANCO:')
print('='*100)
blank_responses = df[df['assistant_response'].isna() | (df['assistant_response'] == '')]
print(f'\nTotal de respuestas en blanco: {len(blank_responses)} de {len(df)} pruebas')
print(f'Porcentaje: {len(blank_responses) / len(df) * 100:.1f}%')

if len(blank_responses) > 0:
    print('\nRespuestas en blanco por tipo de query:')
    blank_by_type = blank_responses.groupby('query_type').size()
    for query_type, count in blank_by_type.items():
        print(f'  - {query_type}: {count} respuestas en blanco')
