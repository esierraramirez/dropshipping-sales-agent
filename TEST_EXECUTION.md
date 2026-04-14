# 🧪 GUÍA RÁPIDA DE VERIFICACIÓN

## Opción 1: Test Automatizado (RECOMENDADO) ⚡

### Pre-requisitos
```bash
# Instalar dependencias necesarias
pip install openpyxl requests

# Verificar que el backend esté corriendo
# Terminal 1: ir a backed/ y ejecutar
cd backed
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar test completo
```bash
# Terminal 2: ejecutar script de test
cd dropshipping-sales-agent
python test_complete_flow.py

# Con verbose (más detallado)
python test_complete_flow.py --verbose
# o
python test_complete_flow.py -v
```

### Resultado esperado
```
============================================================
🚀 VERIFICACIÓN COMPLETA DEL FLUJO DE VENTAS
============================================================

PASO 1: Registrar empresa
✅ Empresa registrada: Test Tienda 15:32:45
✅ Email: test-20260414153245@tienda.com
✅ Token obtenido: eyJ0eXAiOiJKV1QiLCJhbGc...

PASO 2: Cargar archivo Excel
✅ Excel cargado exitosamente
✅ Total de filas: 5
✅ Válidas: 5

PASO 3: Normalizar datos
✅ Datos normalizados
✅ Filas válidas: 5
✅ Filas inválidas: 0

PASO 4: Guardar en Base de Datos
✅ Productos guardados en BD
✅ Total: 5 productos

PASO 5: Construir Base de Conocimiento
✅ Base de conocimiento construida
✅ Documentos indexados: 5

PASO 6: Probar Chat con LLM
Query 1: ¿Qué camisetas tienes disponibles?
✅ Respuesta recibida
✅ Productos encontrados: 1
  Respuesta: Contamos con Camiseta Roja Premium por $25...

Query 2: Quiero zapatillas para correr, ¿cuál me recomiendas?
✅ Respuesta recibida
✅ Productos encontrados: 1
  Respuesta: Te recomiendo nuestras Zapatillas Running...

Query 3: ¿Cuál es el producto más barato que tienen?
✅ Respuesta recibida
✅ Productos encontrados: 1
  Respuesta: El producto más barato es el Gorro Deportivo...

============================================================
✅ RESUMEN DE VERIFICACIÓN
============================================================

✅ Todos los pasos completados exitosamente
✅ Tiempo total: 8.23 segundos
✅ Empresa creada: Test Tienda 15:32:45 (123)
✅ Productos: BD
✅ Base de conocimiento: INDEXADA
✅ Chat LLM: FUNCIONAL

🎉 FLUJO COMPLETAMENTE VERIFICADO Y FUNCIONAL 🎉
```

---

## Opción 2: Verificación Manual (Postman) 📮

Si prefieres probar paso a paso con Postman:

### 1️⃣ REGISTRO
```
POST http://localhost:8000/auth/register
Content-Type: application/json

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

✅ Guardar el `access_token` que retorna

---

### 2️⃣ CARGAR EXCEL
```
POST http://localhost:8000/catalog/upload/me
Authorization: Bearer {TOKEN}
Content-Type: multipart/form-data

file: [seleccionar archivo XLSX]
```

---

### 3️⃣ NORMALIZAR
```
POST http://localhost:8000/catalog/normalize/me
Authorization: Bearer {TOKEN}
```

---

### 4️⃣ GUARDAR EN BD
```
POST http://localhost:8000/catalog/save/me
Authorization: Bearer {TOKEN}
```

---

### 5️⃣ CONSTRUIR BASE DE CONOCIMIENTO
```
POST http://localhost:8000/catalog/build-knowledge-base/me
Authorization: Bearer {TOKEN}
```

---

### 6️⃣ CHAT CON LLM
```
POST http://localhost:8000/chat/me
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "message": "¿Qué productos tienes disponibles?"
}
```

---

## Opción 3: Verificación con cURL 💻

```bash
# 1. Registrar
TOKEN=$(curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@test.com",
    "password": "test123",
    "country": "Colombia"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"

# 2. Chat
curl -X POST http://localhost:8000/chat/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué tienes disponible?"}'
```

---

## ✅ Checklist Post-Verificación

Después de ejecutar el test:

- [ ] ✅ Script completó todos los 6 pasos sin errores
- [ ] ✅ Chat retornou respuestas que mencionan productos
- [ ] ✅ Las respuestas contienen información de precios
- [ ] ✅ Tiempo de respuesta < 10 segundos por query
- [ ] ✅ No hay errores 500 en el backend
- [ ] ✅ PostgreSQL contiene registros de productos

---

## 🔍 Debugging

### Error: "No se pudo conectar"
```
❌ Error: No se pudo conectar con el servidor
✅ Solución: 
   1. Verifica que backend esté corriendo en puerto 8000
   2. Ejecuta: uvicorn app.main:app --reload
   3. Confirma: http://localhost:8000/health retorna 200
```

### Error: "Token inválido"
```
❌ Error: 401 Unauthorized
✅ Solución:
   1. Usa el token exacto de la respuesta de registro
   2. Formato: "Authorization: Bearer {TOKEN}"
   3. Genera nuevo token si expiró
```

### Error: "Base de conocimiento no existe"
```
❌ Error: 404 Knowledge base not found
✅ Solución:
   1. Verifica que POST /catalog/save/me retornó 200
   2. Ejecuta POST /catalog/build-knowledge-base/me
   3. Espera 2-3 segundos antes de chatear
```

### Error: "Productos no encontrados en búsqueda"
```
❌ Matches found: 0
✅ Solución:
   1. Verifica que la query sea similar a productos reales
   2. Intenta: "¿Qué tienes?" en lugar de queries específicas
   3. Revisa que build-knowledge-base retornó documentos_created > 0
```

---

## 📊 Métricas Esperadas

| Métrica | Esperado | Actual |
|---------|----------|--------|
| **Tiempo registro** | < 2s | ✅ |
| **Tiempo carga Excel** | < 3s | ✅ |
| **Tiempo normalización** | < 5s | ✅ |
| **Tiempo guardar BD** | < 2s | ✅ |
| **Tiempo construir KB** | < 3s | ✅ |
| **Tiempo respuesta chat** | < 5s | ✅ |
| **Matches encontrados** | ≥ 1 | ✅ |
| **Token response** | < 600 | ✅ |

---

## 📝 Logs Importantes

### Ver logs del backend
```bash
# En terminal donde corre uvicorn
# Verás líneas como:
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started server process [PID]
INFO:     Waiting for application startup

# Durante test verás:
INFO:     POST /auth/register HTTP/1.1" 200
INFO:     POST /catalog/upload/me HTTP/1.1" 200
INFO:     POST /chat/me HTTP/1.1" 200
```

### Verificar PostgreSQL
```sql
-- Conectar a Supabase
SELECT COUNT(*) FROM vendors;           -- Debe > 0
SELECT COUNT(*) FROM products;          -- Debe = 5
SELECT COUNT(*) FROM chat_messages;     -- Debe > 0
```

---

## 🎯 Siguiente Paso

Una vez verificado el flujo completo:

1. **Generar datos reales**: Usa un Excel real de tu catálogo
2. **Prueba con usuarios reales**: Invita Beta users
3. **Monitorear costos**: Revisa OpenAI dashboard
4. **Optimizar prompts**: Ajusta el system_prompt para mejorar conversions

---

**Información de contacto para debugging:**
- Backend: http://localhost:8000/docs (Swagger)
- Health check: http://localhost:8000/health
- Logs: Terminal donde corre uvicorn

¡Listo para verificar tu sistema! 🚀
