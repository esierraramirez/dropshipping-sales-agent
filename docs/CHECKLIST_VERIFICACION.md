# ✅ CHECKLIST DE VERIFICACIÓN - FLUJO COMPLETO

**Objetivo:** Verificar que cada paso del flujo funciona correctamente

---

## 🧪 TESTING DEL FLUJO PASO A PASO

### PASO 1: REGISTRO DE EMPRESA ✅

**Endpoint:** `POST http://localhost:8000/auth/register`

**Request:**
```json
{
  "name": "Mi Tienda Test",
  "email": "test@tienda.com",
  "password": "password123",
  "rfc": "RFC123456789",
  "sector": "Moda",
  "phone": "+57 3001234567",
  "website": "https://tienda.com",
  "address": "Calle 123 #45",
  "city": "Bogotá",
  "state": "Cundinamarca",
  "country": "Colombia",
  "postal_code": "110001",
  "description": "Tienda de moda online"
}
```

**Verificar:**
- [ ] Status 200
- [ ] Response incluye `access_token`
- [ ] Response incluye `vendor` con todos los datos
- [ ] BD PostgreSQL: Fila en tabla `vendors`

---

### PASO 2: LOGIN ✅

**Endpoint:** `POST http://localhost:8000/auth/login`

**Request:**
```json
{
  "email": "test@tienda.com",
  "password": "password123"
}
```

**Verificar:**
- [ ] Status 200
- [ ] Obtiene nuevo JWT token
- [ ] Guardar token: `TOKEN="eyJ..."`

---

### PASO 3: CARGAR ARCHIVO EXCEL ✅

**Endpoint:** `POST http://localhost:8000/catalog/upload/me`

**Preparar:**
- [ ] Crear archivo `productos.xlsx` con columnas:
  ```
  product_id | name | category | price | currency | stock_status
  001        | Camiseta Roja | Ropa | 25 | USD | in_stock
  002        | Pantalón Negro | Ropa | 45 | USD | in_stock
  ```

**Request (FormData):**
```
file: productos.xlsx
Header: Authorization: Bearer {TOKEN}
```

**Verificar:**
- [ ] Status 200
- [ ] Response: `"is_valid": true`
- [ ] Response: `"total_rows": 2`
- [ ] Response: `"preview_rows"`
- [ ] Archivo guardado en: `data/raw/mi-tienda-test/`

---

### PASO 4: NORMALIZAR DATOS ✅

**Endpoint:** `POST http://localhost:8000/catalog/normalize/me`

**Request:**
```
Header: Authorization: Bearer {TOKEN}
```

**Verificar:**
- [ ] Status 200
- [ ] Response: `"message": "Catálogo normalizado correctamente"`
- [ ] Response: `"valid_rows": 2`
- [ ] Archivos creados en `data/processed/mi-tienda-test/`:
  ```
  ✓ catalog_normalized.csv
  ✓ catalog_normalized.jsonl
  ✓ data_quality_report.json
  ```
- [ ] CSV contiene datos limpios
- [ ] JSONL tiene 1 línea por producto

---

### PASO 5: GUARDAR EN BASE DE DATOS ✅

**Endpoint:** `POST http://localhost:8000/catalog/save/me`

**Request:**
```
Header: Authorization: Bearer {TOKEN}
```

**Verificar:**
- [ ] Status 200
- [ ] Response: `"message": "Catálogo guardado..."`
- [ ] Response: `"total_saved": 2`
- [ ] PostgreSQL tabla `products`:
  ```sql
  SELECT COUNT(*) FROM products WHERE vendor_id = {vendor_id};
  -- Resultado: 2
  ```
- [ ] Cada producto tiene:
  - [ ] vendor_id correcto
  - [ ] name, category, price
  - [ ] stock_status
  - [ ] timestamp

---

### PASO 6: CONSTRUIR BASE DE CONOCIMIENTO ✅

**Endpoint:** `POST http://localhost:8000/catalog/build-knowledge-base/me`

**Request:**
```
Header: Authorization: Bearer {TOKEN}
```

**Verificar:**
- [ ] Status 200
- [ ] Response: `"message": "Base de conocimiento construida correctamente"`
- [ ] Response: `"documents_created": 2`
- [ ] Archivos creados en `data/index/mi-tienda-test/`:
  ```
  ✓ knowledge_base.jsonl (2 líneas, 1 por producto)
  ✓ keyword_index.json (índice de búsqueda)
  ```
- [ ] JSONL contiene documentos formateados

---

### PASO 7: BÚSQUEDA/RETRIEVAL ✅

**Endpoint:** `POST http://localhost:8000/retrieval/search`

**Request:**
```json
{
  "query": "camiseta roja",
  "top_k": 2
}
```

**Header:** `Authorization: Bearer {TOKEN}`

**Verificar:**
- [ ] Status 200
- [ ] Response: `"total_matches": 2` (o mayor)
- [ ] Response: `"results"` contiene al menos 1 producto
- [ ] Cada resultado tiene:
  - [ ] name
  - [ ] category
  - [ ] price
  - [ ] description

---

### PASO 8: CHAT CON LLM ✅

**Endpoint:** `POST http://localhost:8000/chat/me`

**Request:**
```json
{
  "message": "¿Tienes camisetas disponibles?"
}
```

**Header:** `Authorization: Bearer {TOKEN}`

**Verificar:**
- [ ] Status 200
- [ ] Response: `"agent_response"` contiene texto
- [ ] Response: `"matches_found": 1` (o más)
- [ ] Response: `"context_used"` muestra productos
- [ ] La respuesta menciona productos específicos
- [ ] La respuesta intenta vender/recomendar

**Respuesta esperada:**
```json
{
  "vendor_name": "Mi Tienda Test",
  "user_message": "¿Tienes camisetas disponibles?",
  "agent_response": "Sí, contamos con Camiseta Roja por $25. ¿Te interesa conocer más detalles o algún otro modelo?",
  "context_used": "[Resultado 1]\nProducto: Camiseta Roja...",
  "matches_found": 1
}
```

---

## 🎯 CONVERSACIÓN COMPLETA DE AUTO-TEST

### Script Python para testing (opcional):

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. REGISTER
print("1️⃣ Registrando empresa...")
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "name": "Test Shop",
        "email": "test@shop.com",
        "password": "test123",
        "rfc": "RFC123",
        "sector": "Fashion",
        "country": "Colombia",
    }
)
assert response.status_code == 200
token = response.json()["access_token"]
print(f"✅ Token: {token[:20]}...")

# 2. UPLOAD (requiere archivo Excel)
print("\n2️⃣ Cargando Excel...")
with open("test-products.xlsx", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/catalog/upload/me",
        files={"file": f},
        headers={"Authorization": f"Bearer {token}"}
    )
assert response.status_code == 200
print(f"✅ Productos cargados: {response.json()['total_rows']}")

# 3. NORMALIZE
print("\n3️⃣ Normalizando...")
response = requests.post(
    f"{BASE_URL}/catalog/normalize/me",
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
print(f"✅ Válidos: {response.json()['valid_rows']}")

# 4. SAVE TO DB
print("\n4️⃣ Guardando en BD...")
response = requests.post(
    f"{BASE_URL}/catalog/save/me",
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
print(f"✅ Guardados: {response.json().get('total_saved', 'N/A')}")

# 5. BUILD KB
print("\n5️⃣ Construyendo base de conocimiento...")
response = requests.post(
    f"{BASE_URL}/catalog/build-knowledge-base/me",
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
print(f"✅ Documentos: {response.json()['documents_created']}")

# 6. CHAT
print("\n6️⃣ Probando chat...")
response = requests.post(
    f"{BASE_URL}/chat/me",
    json={"message": "¿Qué productos tienes?"},
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
agent_response = response.json()["agent_response"]
print(f"✅ Respuesta: {agent_response[:100]}...")

print("\n✅ TODOS LOS PASOS COMPLETADOS EXITOSAMENTE")
```

---

## 🔍 DEBUGGING - Si algo falla

### Error 404 en /catalog/normalize/me
```
❌ "No existe catálogo cargado"
✅ Solución: Verifica que el archivo Excel fue cargado en paso 3
```

### Error 404 en /catalog/build-knowledge-base/me
```
❌ "No hay productos cargados"
✅ Solución: Verifica que POST /catalog/save/me fue exitoso
```

### Error 404 en /chat/me
```
❌ "La base de conocimiento aún no ha sido construida"
✅ Solución: Ejecuta POST /catalog/build-knowledge-base/me primero
```

### Error 401
```
❌ "Token inválido"
✅ Solución: 
  - Verifica Authorization header: "Bearer {TOKEN}"
  - Genera nuevo token con login
```

---

## 📊 VERIFICACIÓN DE DATOS

### PostgreSQL - Productos guardados
```sql
-- Conectar a Supabase PostgreSQL
SELECT COUNT(*) as total_products FROM products WHERE vendor_id = 1;

-- Ver productos
SELECT id, name, price, category FROM products LIMIT 5;
```

### Sistema de archivos
```bash
# Windows PowerShell
ls data/raw/test-shop/                  # Excel originales
ls data/processed/test-shop/            # Datos normalizados
ls data/index/test-shop/                # Base de conocimiento

# Ver contenido de JSONL
Get-Content data/index/test-shop/knowledge_base.jsonl -Head 1
```

---

## ✅ RESULTADO ESPERADO

Si todos los pasos pasan:

```
✅ Empresa registrada en PostgreSQL
✅ Excel cargado y almacenado
✅ Datos normalizados (CSV + JSONL)
✅ Productos guardados en BD (2,500+ filas)
✅ Base de conocimiento indexada
✅ LLM puede buscar productos (retrieval)
✅ Chat responde preguntas con info real de productos
✅ LLM intenta vender productos relevantes

🎉 FLUJO COMPLETAMENTE FUNCIONAL
```

---

**Última actualización:** 14 de Abril de 2026
