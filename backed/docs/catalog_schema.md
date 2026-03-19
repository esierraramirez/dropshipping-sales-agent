# Esquema del Catálogo de Productos

## Descripción
Este documento define la estructura oficial del catálogo de productos que será cargado por el vendedor dropshipping mediante un archivo Excel dentro de la plataforma.

## Objetivo
Estandarizar la información de productos para permitir:
- validación del catálogo
- normalización de datos
- almacenamiento estructurado
- asociación del catálogo al vendedor
- preparación de la base de conocimiento para el agente inteligente
- respuestas confiables del agente con base en información real

## Formato de entrada
El vendedor cargará su catálogo mediante un archivo Excel (`.xlsx`) siguiendo la plantilla definida por el sistema.

## Columnas obligatorias
- `product_id`: identificador único del producto
- `name`: nombre del producto
- `category`: categoría del producto
- `price`: precio numérico del producto
- `currency`: moneda del producto (`COP`, `USD`, `EUR`)
- `stock_status`: estado del inventario (`in_stock`, `out_of_stock`, `limited`, `preorder`)
- `min_shipping_days`: tiempo mínimo de envío
- `max_shipping_days`: tiempo máximo de envío

## Columnas opcionales
- `short_description`: descripción corta
- `full_description`: descripción completa
- `brand`: marca
- `shipping_cost`: costo de envío
- `shipping_regions`: regiones o ciudades donde aplica el envío
- `returns_policy`: política de devoluciones
- `warranty_policy`: política de garantía
- `specs`: especificaciones técnicas
- `variants`: variantes como color, talla o modelo
- `source`: origen o proveedor del producto

## Reglas de validación
- `price` debe ser mayor o igual a 0
- `min_shipping_days` y `max_shipping_days` deben ser enteros positivos
- `max_shipping_days` debe ser mayor o igual a `min_shipping_days`
- `stock_status` debe pertenecer al conjunto permitido:
  - `in_stock`
  - `out_of_stock`
  - `limited`
  - `preorder`
- `currency` debe pertenecer al conjunto permitido:
  - `COP`
  - `USD`
  - `EUR`

## Propósito dentro del sistema
La información estructurada del catálogo servirá como base para:
1. la carga del catálogo por parte del vendedor
2. la validación y normalización de los productos
3. el almacenamiento del catálogo por vendedor
4. la construcción posterior de la base de conocimiento del agente
5. la preparación del índice semántico para recuperación RAG

## Entregables asociados
- Documento técnico del esquema del catálogo
- Modelo Pydantic de validación del producto
- JSON Schema del producto
- Plantilla Excel para el vendedor
- Ejemplo de producto válido