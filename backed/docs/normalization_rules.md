# Reglas de Normalización del Catálogo

## Objetivo
Estandarizar la información cargada por el vendedor desde Excel para convertirla en una base de conocimiento uniforme y utilizable por el agente inteligente.

## Reglas aplicadas

### Precio
- Se eliminan símbolos de moneda.
- Se convierten separadores de miles y decimales.
- El valor final se almacena como número decimal.

### Categoría
- Se homologan categorías similares a un conjunto estándar.
- Ejemplo:
  - electronica → Electronics
  - tecnologia → Electronics
  - hogar → Home

### Stock
- Se transforma a los estados permitidos:
  - in_stock
  - out_of_stock
  - limited
  - preorder

### Moneda
- Se convierte a mayúsculas.
- Si el valor es inválido, por defecto se asigna COP.

### Tiempos de envío
- Se convierten a enteros positivos.
- `max_shipping_days` debe ser mayor o igual a `min_shipping_days`.

### Campos opcionales
- Si vienen vacíos, se almacenan como null o se omiten según corresponda.

## Salidas del proceso
- `catalog_normalized.csv`
- `catalog_normalized.jsonl`
- `data_quality_report.json`