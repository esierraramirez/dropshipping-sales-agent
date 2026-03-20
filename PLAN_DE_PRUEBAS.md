# 🧪 Plan de Pruebas - 5 Funcionalidades Principales

## 📋 Resumen de Funcionalidades

| # | Funcionalidad | Endpoint | Método | Entrada | Salida |
|---|---|---|---|---|---|
| 1 | Esquema del catálogo | `/catalog/upload` | POST | Excel + vendor_name | Validación de columnas |
| 2 | Carga y validación | `/catalog/upload` | POST | File .xlsx | Archivo guardado + preview |
| 3 | Normalización | `/catalog/normalize` | POST | vendor_name | Datos limpios y categorizados |
| 4 | Almacenamiento en BD | `/catalog/save` | POST | vendor_name | Productos en DB |
| 5 | Base de conocimiento | `/catalog/build-knowledge-base` | POST | vendor_name | Índice y documentos |

---

## 🔧 Columnas Requeridas

El sistema requiere estos campos en el Excel:

```
product_id       (identificador único)
name             (nombre del producto)
category         (categoría estandarizada)
price            (precio en formato numérico)
currency         (moneda: USD, COP, etc.)
stock_status     (disponibilidad)
min_shipping_days (días mínimos de envío)
max_shipping_days (días máximos de envío)
```

---

## 🧪 FUNCIONALIDAD 1: Esquema del Catálogo

### ✅ Prueba 1.1: Archivo con estructura correcta

**Pasos:**
1. Usar archivo: `tests/test_data/valid_catalog.xlsx`
2. Ejecutar:
   ```bash
   curl -X POST "http://localhost:8000/catalog/upload" \
     -F "vendor_name=TestVendor" \
     -F "file=@tests/test_data/valid_catalog.xlsx"
   ```

**Resultado esperado:**
```json
{
  "message": "Catálogo cargado y analizado correctamente.",
  "vendor_name": "TestVendor",
  "detected_columns": [
    "product_id", "name", "category", "price", "currency", 
    "stock_status", "min_shipping_days", "max_shipping_days"
  ],
  "missing_required_columns": [],
  "total_rows": 5,
  "is_valid": true,
  "preview_rows": [...]
}
```

### ❌ Prueba 1.2: Archivo con columnas faltantes

**Pasos:**
1. Usar archivo: `tests/test_data/invalid_missing_columns.xlsx`
2. Ejecutar:
   ```bash
   curl -X POST "http://localhost:8000/catalog/upload" \
     -F "vendor_name=TestVendor" \
     -F "file=@tests/test_data/invalid_missing_columns.xlsx"
   ```

**Resultado esperado:**
```json
{
  "message": "Catálogo cargado y analizado correctamente.",
  "is_valid": false,
  "missing_required_columns": ["price", "currency"],
  "total_rows": 5
}
```

### 📝 Verificaciones
- [ ] Columnas detectadas correctamente
- [ ] Identificadas columnas faltantes
- [ ] No hay errores de crash
- [ ] Se muestra preview de datos

---

## 🧪 FUNCIONALIDAD 2: Carga y Validación

### ✅ Prueba 2.1: Archivo válido procesado correctamente

**Pasos:**
1. Subir archivo válido
2. Verificar que se guarde en `data/raw/{vendor_slug}/{timestamp}_{nombre}.xlsx`
3. Revisar respuesta

**Verificaciones:**
```bash
# Verificar que el archivo se guardó
ls -la data/raw/testvend/

# Debería haber un archivo como:
# data/raw/testvend/20260320_123456_valid_catalog.xlsx
```

### ❌ Prueba 2.2: Archivo inválido (datos corruptos)

**Pasos:**
1. Usar archivo: `tests/test_data/corrupted_file.xlsx` (con datos inválidos)
2. Ejecutar upload
3. Verificar que el sistema detecte errores

**Resultado esperado:**
```json
{
  "detail": "No fue posible leer el archivo Excel: ..."
}
```

### 🚫 Prueba 2.3: Archivo formatos incorrectos

**Pasos:**
1. Intentar subir: `tests/test_data/invalid_format.csv`
2. Ejecutar:
   ```bash
   curl -X POST "http://localhost:8000/catalog/upload" \
     -F "vendor_name=TestVendor" \
     -F "file=@tests/test_data/invalid_format.csv"
   ```

**Resultado esperado:**
```json
{
  "detail": "Solo se permiten archivos .xlsx"
}
```

### 📝 Verificaciones
- [ ] Archivos válidos se guardan correctamente
- [ ] Se genera timestamp en el nombre
- [ ] Sistema detecta errores en archivos inválidos
- [ ] Mensajes de error son claros
- [ ] No hay crash del sistema

---

## 🧪 FUNCIONALIDAD 3: Normalización y Categorización

### ✅ Prueba 3.1: Normalizar datos "sucios"

**Pasos:**
1. Usar archivo: `tests/test_data/dirty_data.xlsx` (con datos inconsistentes)
2. Ejecutar:
   ```bash
   curl -X POST "http://localhost:8000/catalog/normalize" \
     -F "vendor_name=TestVendor"
   ```

**El archivo contiene:**
- Precios como texto: `"$20.000"`, `"USD 100,50"`
- Categorías inconsistentes: `"ropa"`, `"ROPA"`, `"Ropas"`
- Textos con espacios extras

**Resultado esperado:**
```json
{
  "message": "Catálogo normalizado correctamente.",
  "vendor_name": "TestVendor",
  "total_rows": 5,
  "valid_rows": 5,
  "invalid_rows": 0,
  "preview_rows": [
    {
      "product_id": "001",
      "name": "Camiseta Azul",
      "category": "ropa",
      "price": 20000.0,
      "currency": "COP",
      "stock_status": "en_stock",
      "min_shipping_days": 2,
      "max_shipping_days": 5
    }
  ],
  "processed_csv_path": "data/processed/testvend/catalog_normalized.csv",
  "processed_jsonl_path": "data/processed/testvend/catalog_normalized.jsonl",
  "quality_report_path": "data/processed/testvend/quality_report.json"
}
```

### ✅ Prueba 3.2: Detectar filas inválidas

**Pasos:**
1. Usar archivo: `tests/test_data/partial_errors.xlsx` (3 filas válidas, 2 inválidas)
2. Normalizar
3. Verificar report_path

**Resultado esperado:**
```json
{
  "valid_rows": 3,
  "invalid_rows": 2,
  "quality_report_path": "data/processed/testvend/quality_report.json"
}
```

**El reporte debe mostrar:**
```json
{
  "total_rows_input": 5,
  "valid_rows": 3,
  "invalid_rows": 2,
  "errors": [
    {
      "row": 2,
      "issues": ["price es inválido", "category no encontrada"]
    },
    {
      "row": 4,
      "issues": ["stock_status inválido"]
    }
  ]
}
```

### 📝 Verificaciones
- [ ] Precios convertidos a numéricos
- [ ] Categorías estandarizadas
- [ ] Espacios en blanco removidos
- [ ] Errores identificados correctamente
- [ ] Filas inválidas separadas
- [ ] Archivos generados en `data/processed/`

---

## 🧪 FUNCIONALIDAD 4: Almacenamiento en Base de Datos

### ✅ Prueba 4.1: Guardar productos en BD

**Pasos:**
1. Después de normalizar, ejecutar:
   ```bash
   curl -X POST "http://localhost:8000/catalog/save" \
     -F "vendor_name=TestVendor"
   ```

**Resultado esperado:**
```json
{
  "message": "Productos guardados exitosamente en la base de datos.",
  "vendor_name": "TestVendor",
  "products_saved": 5,
  "products_failed": 0,
  "vendor_id": 1,
  "created_at": "2026-03-20T12:34:56"
}
```

### ✅ Prueba 4.2: Consultar productos por vendedor

**Pasos:**
1. Ejecutar:
   ```bash
   curl -X GET "http://localhost:8000/catalog/products?vendor_name=TestVendor"
   ```

**Resultado esperado:**
```json
{
  "vendor_name": "TestVendor",
  "total_products": 5,
  "products": [
    {
      "id": 1,
      "product_id": "001",
      "name": "Camiseta Azul",
      "category": "ropa",
      "price": 20000.0,
      "currency": "COP",
      "stock_status": "en_stock",
      "vendor_id": 1,
      "created_at": "2026-03-20T12:34:56"
    }
  ]
}
```

### ✅ Prueba 4.3: Verificar sin pérdida de datos

**Pasos:**
1. Contar filas en CSV normalizado
2. Contar registros en BD
3. Comparar

**Verificaciones:**
```bash
# Contar líneas en CSV
wc -l data/processed/testvend/catalog_normalized.csv
# Resultado: 6 (5 productos + header)

# Consultar BD
curl -X GET "http://localhost:8000/catalog/products?vendor_name=TestVendor"
# total_products debe ser 5
```

### 📝 Verificaciones
- [ ] Todos los productos se guardan
- [ ] Se crea vendor_id correctamente
- [ ] No hay pérdida de datos
- [ ] Relación vendor-product es correcta
- [ ] Campos se guardan sin modificación

---

## 🧪 FUNCIONALIDAD 5: Base de Conocimiento del Agente

### ✅ Prueba 5.1: Construir base de conocimiento

**Pasos:**
1. Después de guardar en BD, ejecutar:
   ```bash
   curl -X POST "http://localhost:8000/catalog/build-knowledge-base" \
     -F "vendor_name=TestVendor"
   ```

**Resultado esperado:**
```json
{
  "message": "Base de conocimiento construida exitosamente.",
  "vendor_name": "TestVendor",
  "documents_created": 5,
  "index_built": true,
  "knowledge_base_path": "data/processed/testvend/knowledge_base.jsonl",
  "index_path": "data/processed/testvend/knowledge_base_index.json",
  "indexed_keywords": 142,
  "indexed_categories": ["ropa", "electrónica", "hogar"]
}
```

### ✅ Prueba 5.2: Consultar información de base de conocimiento

**Pasos:**
1. Ejecutar:
   ```bash
   curl -X GET "http://localhost:8000/catalog/knowledge-base?vendor_name=TestVendor"
   ```

**Resultado esperado:**
```json
{
  "vendor_name": "TestVendor",
  "status": "available",
  "total_documents": 5,
  "index_info": {
    "keywords_indexed": 142,
    "categories": ["ropa", "electrónica", "hogar"],
    "most_common_keywords": ["camiseta", "azul", "algodón", "precio", "envío"]
  },
  "index_file_size": 2048,
  "knowledge_base_file_size": 4096
}
```

### ✅ Prueba 5.3: Verificar contenido de documento

**Pasos:**
1. Leer archivo: `data/processed/testvend/knowledge_base.jsonl`
2. Verificar estructura de documento

**Cada línea debe ser:**
```json
{
  "id": "prod_001",
  "content": "Camiseta Azul de algodón. Categoría: ropa. Precio: 20000 COP. Disponible. Envío: 2-5 días.",
  "metadata": {
    "product_id": "001",
    "name": "Camiseta Azul",
    "category": "ropa",
    "price": 20000.0,
    "currency": "COP",
    "stock_status": "en_stock",
    "vendor_name": "TestVendor"
  },
  "keywords": ["camiseta", "azul", "algodón", "ropa", "20000", "cop"]
}
```

### 📝 Verificaciones
- [ ] Se crean documentos para cada producto
- [ ] Índice de palabras clave se construye
- [ ] Categorías se indexan correctamente
- [ ] Archivos se guardan en ubicación correcta
- [ ] Estructura de documento es consistente
- [ ] LLM puede acceder a la información

---

## 🎯 Flujo Completo de Pruebas

```
┌─────────────────────────────────────────────────────────────┐
│ 1. UPLOAD CATALOG                                           │
│ POST /catalog/upload (vendor_name, file)                    │
│ └─ Validar columnas ✓                                       │
│ └─ Generar preview ✓                                        │
└────────────┬────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. NORMALIZE CATALOG                                        │
│ POST /catalog/normalize (vendor_name)                       │
│ └─ Limpiar datos ✓                                          │
│ └─ Estandarizar categorías ✓                                │
│ └─ Generar reporte de calidad ✓                             │
└────────────┬────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. SAVE TO DATABASE                                         │
│ POST /catalog/save (vendor_name, db)                        │
│ └─ Crear vendor si no existe ✓                              │
│ └─ Guardar productos ✓                                      │
└────────────┬────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. BUILD KNOWLEDGE BASE                                     │
│ POST /catalog/build-knowledge-base (vendor_name, db)        │
│ └─ Convertir productos a documentos ✓                       │
│ └─ Crear índice de palabras clave ✓                         │
│ └─ Guardar en JSONL ✓                                       │
└────────────┬────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. QUERY                                                    │
│ GET /catalog/products (vendor_name)                         │
│ GET /catalog/knowledge-base (vendor_name)                   │
│ └─ Verificar que todo está accesible ✓                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Matriz de Casos de Prueba

### Casos Positivos (Happy Path)
| Test | Endpoint | Parámetro | Esperado | Estado |
|------|----------|-----------|----------|--------|
| 1.1 | POST /upload | Archivo válido | is_valid=true | ⚪ |
| 2.1 | POST /upload | Columnas correctas | missing_columns=[] | ⚪ |
| 3.1 | POST /normalize | Datos "sucios" | valid_rows>0 | ⚪ |
| 4.1 | POST /save | vendor_name | products_saved>0 | ⚪ |
| 4.2 | GET /products | vendor_name | products lista | ⚪ |
| 5.1 | POST /build-kb | vendor_name | documents_created>0 | ⚪ |
| 5.2 | GET /knowledge-base | vendor_name | index_info | ⚪ |

### Casos Negativos (Error Handling)
| Test | Endpoint | Parámetro | Esperado | Estado |
|------|----------|-----------|----------|--------|
| 1.2 | POST /upload | Columnas faltantes | is_valid=false | ⚪ |
| 2.2 | POST /upload | Archivo corruptor | 400 Bad Request | ⚪ |
| 2.3 | POST /upload | Formato .csv | 400 Bad Request | ⚪ |
| 3.2 | POST /normalize | Datos parciales | invalid_rows>0 | ⚪ |
| 4.X | GET /products | vendor no existe | 404 Not Found | ⚪ |
| 5.X | GET /kb | vendor no existe | 404 Not Found | ⚪ |

---

## 🛠️ Herramientas de Prueba

### 1. Usando cURL
```bash
# Upload
curl -X POST "http://localhost:8000/catalog/upload" \
  -F "vendor_name=MiVendedor" \
  -F "file=@tests/test_data/valid_catalog.xlsx"

# Normalize
curl -X POST "http://localhost:8000/catalog/normalize" \
  -F "vendor_name=MiVendedor"

# Save
curl -X POST "http://localhost:8000/catalog/save" \
  -F "vendor_name=MiVendedor"

# Get Products
curl -X GET "http://localhost:8000/catalog/products?vendor_name=MiVendedor"

# Build Knowledge Base
curl -X POST "http://localhost:8000/catalog/build-knowledge-base" \
  -F "vendor_name=MiVendedor"

# Get Knowledge Base
curl -X GET "http://localhost:8000/catalog/knowledge-base?vendor_name=MiVendedor"
```

### 2. Usando Postman
- Importar colección: `tests/postman/catalog_collection.json`
- Configurar variables: `{{base_url}}`, `{{vendor_name}}`
- Ejecutar suite de pruebas

### 3. Usando Python (requests)
```python
# Ver: tests/test_catalog_api.py
python tests/test_catalog_api.py
```

---

## ✅ Checklist de Verificación Final

### Antes de Iniciar Pruebas
- [ ] Base de datos inicializada
- [ ] Servidor FastAPI ejecutando en puerto 8000
- [ ] Directorios `data/raw/` y `data/processed/` creados
- [ ] Archivos de prueba en `tests/test_data/`

### Después de Cada Funcionalidad
- [ ] Respuesta HTTP correcta (status code)
- [ ] Estructura JSON válida
- [ ] Datos en archivos generados
- [ ] No hay excepciones no capturadas
- [ ] Logs en consola son claros

### Después de Todas las Pruebas
- [ ] Ejecutar script de limpieza: `scripts/cleanup_test_data.sh`
- [ ] Verificar BD limpia
- [ ] Generar reporte: `tests/generate_test_report.py`

---

## 📚 Archivos de Referencia

```
tests/
├── test_data/
│   ├── valid_catalog.xlsx                 ✅ Archivo válido
│   ├── invalid_missing_columns.xlsx       ❌ Faltan columnas
│   ├── invalid_format.csv                 ❌ Formato incorrecto
│   ├── corrupted_file.xlsx                ❌ Datos corruptos
│   ├── dirty_data.xlsx                    🔄 Datos sin limpiar
│   └── partial_errors.xlsx                ⚠️ Mezcla válido/inválido
├── postman/
│   └── catalog_collection.json            API tests
├── test_catalog_api.py                    Script Python
└── curl_commands.sh                       Comandos bash
```

---

## 🔗 Endpoints a Probar

| # | Método | Endpoint | Descripción |
|---|--------|----------|-------------|
| 1 | POST | `/catalog/upload` | Cargar archivo Excel |
| 2 | POST | `/catalog/normalize` | Normalizar datos |
| 3 | POST | `/catalog/save` | Guardar en BD |
| 4 | GET | `/catalog/products` | Listar productos |
| 5 | POST | `/catalog/build-knowledge-base` | Construir KB |
| 6 | GET | `/catalog/knowledge-base` | Info de KB |

---

## 📝 Notas Importantes

1. **Orden de ejecución**: Debe ser upload → normalize → save → build-kb
2. **vendor_name**: Mismo vendedor debe usarse en toda la cadena
3. **Timestamps**: Cada upload genera nuevo timestamp
4. **Limpieza**: Usar scripts de limpieza entre pruebas
5. **Logs**: Revisar logs en `logs/` para diagnóstico

---

**Última actualización**: 2026-03-20  
**Versión**: 1.0
