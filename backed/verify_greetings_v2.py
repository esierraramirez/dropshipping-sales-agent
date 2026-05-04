#!/usr/bin/env python3
"""Verificar que los saludos se responden correctamente con saludo inicial."""

import pandas as pd

df = pd.read_excel('data/reports/objective4_kpi_results.xlsx', sheet_name='detalle_pruebas')

# Filtrar solo las pruebas de disponibilidad (saludos simples)
availability_tests = df[df['query_type'] == 'availability']

print('='*100)
print('VERIFICACION DE SALUDOS SIMPLES - availability')
print('='*100)
print(f'\nTotal pruebas: {len(availability_tests)}\n')

# Verificar si responde con saludo inicial
correct_greetings = 0

for idx, row in availability_tests.iterrows():
    message = row['message']
    response = row['assistant_response']
    
    # Verificar si es un saludo inicial, respuesta social, o identificacion
    is_correct = (
        'asistente' in response.lower() or 
        'soy' in response.lower() or 
        'gusto atenderte' in response.lower() or
        'claro' in response.lower() or
        'mucho gusto' in response.lower()
    )
    
    if is_correct:
        correct_greetings += 1
        status = "✓ CORRECTO"
    else:
        status = "✗ INCORRECTO"
    
    print(f'[{idx+1}] Mensaje: "{message[:50]}"')
    print(f'    Respuesta: "{response[:90]}..."')
    print(f'    {status}\n')

print('='*100)
print(f'RESULTADO: {correct_greetings}/{len(availability_tests)} respuestas fueron correctas')
print(f'Porcentaje: {correct_greetings/len(availability_tests)*100:.1f}%')

if correct_greetings == len(availability_tests):
    print('\n✅ TODAS LAS RESPUESTAS FUERON CORRECTAS')
else:
    print(f'\n⚠️  {len(availability_tests) - correct_greetings} RESPUESTAS NECESITABAN MEJORAR')
