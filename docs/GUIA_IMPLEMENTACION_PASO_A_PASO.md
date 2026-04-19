# 🛠️ GUÍA DE IMPLEMENTACIÓN PASO A PASO - WHATSAPP INTEGRATION

**Objetivo**: Verificar e implementar la integración WhatsApp Multi-Tenant  
**Duración Estimada**: 30-45 minutos  
**Requisitos Previos**:
- ✅ Backend running en http://localhost:8000
- ✅ Frontend running en http://localhost:5173
- ✅ PostgreSQL/Supabase accesible
- ✅ Credenciales Meta for Developers disponibles

---

## FASE 1: VERIFICACIÓN DE BD (5 minutos)

### Paso 1.1: Conectar a Base de Datos

```bash
# Opción 1: PostgreSQL Local
psql -U postgres -h localhost

# Opción 2: Supabase
psql "postgresql://user:password@db.supabase.co:5432/postgres"

# Opción 3: Mediante aplicación Python
python
>>> from backend.app.core.config import settings
>>> print(settings.DATABASE_URL)
```

**✅ Verificar**: Conexión exitosa y comando `\d` funciona

---

### Paso 1.2: Verificar Tabla Existe

```sql
-- Ver la estructura
\d whatsapp_connections

-- Debe mostrar:
-- Column           │         Type          │                     Modifiers
-- ────────────────┼───────────────────────┼─────────────────────────────────
-- id              │ integer               │ not null default ...
-- vendor_id       │ integer               │ not null unique
-- phone_number    │ character varying(20) │
-- phone_number_id │ character varying(150)│
-- access_token    │ text                  │
-- verify_token    │ character varying(255)│
-- is_connected    │ boolean               │ default false
```

**❌ Si falta?** Ejecutar migración (Paso 1.3)  
**✅ Si existe?** Continuar

---

### Paso 1.3: Ejecutar Migración (Si es necesario)

```bash
# Ir a directorio backend
cd backed

# Ejecutar migración
python migrate_whatsapp_phone_number.py

# Esperado output:
# 🚀 Starting database migration...
# ✅ Columna 'phone_number' agregada exitosamente
# ✅ Migration completed successfully!
```

**✅ Verificar**: Script completa sin errores

---

### Paso 1.4: Crear Índices (Opcional pero recomendado)

```sql
-- Crear índice en phone_number_id para webhooks rápidos
CREATE INDEX IF NOT EXISTS idx_whatsapp_phone_number_id 
ON whatsapp_connections(phone_number_id);

-- Crear índice en vendor_id para queries por empresa
CREATE INDEX IF NOT EXISTS idx_whatsapp_vendor_id 
ON whatsapp_connections(vendor_id);

-- Verificar índices creados
\d whatsapp_connections
```

**✅ Verificar**: Índices aparecen en output

---

## FASE 2: VERIFICACIÓN DE CÓDIGO (10 minutos)

### Paso 2.1: Verificar Modelado ORM

```bash
# Abrir archivo
code backed/app/models/whatsapp_connection.py

# Debe contener:
# - phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
# - phone_number_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
# - business_account_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
# - access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
# - verify_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
# - vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), unique=True)
```

**✅ Verificar**: Todos los campos están presentes

---

### Paso 2.2: Verificar Pydantic Schemas

```bash
# Abrir archivo
code backed/app/schemas/whatsapp_schema.py

# Debe tener dos clases:
# 1. WhatsAppConnectionRequest
#    - phone_number: Optional[str] = None
#    - phone_number_id: str (required)
#    - access_token: str (required)
#    - verify_token: str (required)

# 2. WhatsAppConnectionResponse
#    - phone_number: Optional[str]
#    - phone_number_id: Optional[str]
#    - access_token: NOT incluido (secreto)
#    - verify_token: Optional[str]
```

**✅ Verificar**: Ambas clases presentes con campos correctos

---

### Paso 2.3: Verificar Servicio de Lógica

```bash
# Abrir archivo
code backed/app/services/whatsapp_service.py

# Buscar función: upsert_whatsapp_connection
# Debe contener:
#   - connection.phone_number = payload.phone_number
#   - connection.phone_number_id = payload.phone_number_id
#   - connection.business_account_id = payload.business_account_id
#   - connection.access_token = payload.access_token
#   - connection.verify_token = payload.verify_token
#   - connection.is_connected = True
#   - db.commit()

# Buscar función: get_whatsapp_connection_by_phone_number_id
# Debe contener:
#   - Query filtrando por phone_number_id
#   - Return WhatsAppConnection o None
```

**✅ Verificar**: Ambas funciones presentes y correctas

---

### Paso 2.4: Verificar Rutas API

```bash
# Abrir archivo
code backed/app/api/routes/whatsapp_routes.py

# Debe contener 4 endpoints:
# 1. PUT /whatsapp/me
#    - Requiere: Authorization header (JWT)
#    - Recibe: WhatsAppConnectionRequest
#    - Retorna: WhatsAppConnectionResponse
#    - Guarda en BD

# 2. GET /whatsapp/me
#    - Requiere: Authorization header
#    - Retorna: WhatsAppConnectionResponse (sin access_token)

# 3. GET /whatsapp/webhook
#    - Hub verification para Meta
#    - No requiere auth
#    - Retorna: hub.challenge si token válido

# 4. POST /whatsapp/webhook
#    - Recibe webhook de Meta
#    - Procesa mensaje
#    - Genera respuesta
#    - Envía respuesta
```

**✅ Verificar**: Todos 4 endpoints presentes

---

### Paso 2.5: Verificar Frontend Component

```bash
# Abrir archivo
code frontend/src/app/pages/WhatsAppPage.tsx

# Debe contener:
# 1. useState para: phoneNumber, phoneNumberId, businessAccountId, accessToken, webhookToken
# 2. useState para: loading, error, success, connected
# 3. useEffect que:
#    - Ejecuta en mount []
#    - Llama GET /whatsapp/me
#    - Prelleña formulario si hay datos
# 4. handleConnect que:
#    - Valida campos requeridos
#    - Llama PUT /whatsapp/me
#    - Muestra success/error
# 5. handleDisconnect que:
#    - Limpia estado
#    - Actualiza is_connected = false
# 6. JSX que:
#    - Muestra 5 inputs
#    - Muestra botones Connect/Disconnect
#    - Muestra mensaje error/success/loading
```

**✅ Verificar**: Component tiene toda la lógica necesaria

---

## FASE 3: TESTS DE API (10 minutos)

### Paso 3.1: Test de Registro

```bash
# 1. Registrarse como empresa nueva
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Corp WhatsApp",
    "email": "test.whatsapp@corp.com",
    "password": "Test123456!",
    "country": "Colombia"
  }'

# Guardar JWT_TOKEN del response
# Esperado: Status 200 + access_token en response
```

**✅ Verificar**: Registro exitoso y token obtenido

---

### Paso 3.2: Test de Guardar Credenciales

```bash
# Reemplazar JWT_TOKEN con el obtenido en paso anterior
JWT_TOKEN="eyJhbGc..."

curl -X PUT "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+57 1 2345 6789",
    "phone_number_id": "1234567890",
    "business_account_id": "0987654321",
    "access_token": "EAABxxxxxxxxxxxxxxxxxxxx",
    "verify_token": "mi_token_secreto_123"
  }'

# Esperado: Status 200 + response con is_connected: true
```

**✅ Verificar**: Status 200 y credenciales guardadas

---

### Paso 3.3: Test de Recuperar Credenciales

```bash
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Esperado: Status 200 + todos los campos EXCEPTO access_token
# {
#   "vendor_id": 1,
#   "phone_number": "+57 1 2345 6789",
#   "phone_number_id": "1234567890",
#   "business_account_id": "0987654321",
#   "verify_token": "mi_token_secreto_123",
#   "is_connected": true
# }
```

**✅ Verificar**: 
- Status 200
- access_token NO aparece en response
- Otros campos correctos

---

### Paso 3.4: Test de Webhook Verification

```bash
curl -X GET "http://localhost:8000/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=mi_token_secreto_123&hub.challenge=CHALLENGE_123"

# Esperado: Status 200 + body = "CHALLENGE_123"
```

**✅ Verificar**: Token validado correctamente

---

### Paso 3.5: Test de Recepción de Mensaje

```bash
curl -X POST "http://localhost:8000/whatsapp/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "metadata": {
            "phone_number_id": "1234567890",
            "display_phone_number": "5712345678"
          },
          "contacts": [{
            "profile": {
              "name": "Cliente Test"
            },
            "wa_id": "5712345678"
          }],
          "messages": [{
            "from": "5712345678",
            "id": "wamid.test123",
            "timestamp": "1234567890",
            "type": "text",
            "text": {
              "body": "¿Tienen camisetas negras?"
            }
          }]
        }
      }]
    }]
  }'

# Esperado: Status 200 + {"status": "processed"}
# En logs del backend: "Message processed | vendor_id=1 | ..."
```

**✅ Verificar**: Webhook procesado exitosamente

---

## FASE 4: TESTS EN FRONTEND (10 minutos)

### Paso 4.1: Abrir Página WhatsApp

```bash
# En browser ir a:
http://localhost:5173/whatsapp

# Esperado:
# - Página carga sin errores
# - 5 campos de input visible
# - Botón "Guardar y verificar conexión"
# - Si hay credenciales guardadas, están prellenadas
```

**✅ Verificar**: UI carga correctamente

---

### Paso 4.2: Rellenar Formulario

```bash
# Llenar cada campo:
- Número de teléfono: +57 1 2345 6789
- Phone Number ID: 1234567890
- Business Account ID: 0987654321
- Access Token: EAABxxxx...
- Webhook Verify Token: mi_token_secreto_123

# NO limpiar los campos
```

**✅ Verificar**: Todos campos aceptan input

---

### Paso 4.3: Click en "Guardar y verificar"

```bash
# Presionar botón "Guardar y verificar conexión"

# Esperado:
# 1. Botón muestra "Guardando..." con spinner
# 2. Después 2-3 segundos:
#    - Desaparece spinner
#    - Muestra mensaje verde: "✅ Conexión guardada exitosamente"
#    - access_token se limpia (por seguridad)
#    - Botón cambia a "Desconectar" (rojo)
```

**✅ Verificar**: Todo funciona sin errores

---

### Paso 4.4: Refresh de Página

```bash
# Presionar F5 para refrescar la página

# Esperado:
# - Página carga
# - useEffect ejecuta GET /whatsapp/me
# - Formulario se prelleña con los valores guardados
# - Botón dice "Desconectar"
# - Estado muestra "Conectado"
```

**✅ Verificar**: Credenciales persisten en base de datos

---

### Paso 4.5: Test de Desconexión

```bash
# Presionar botón "Desconectar"

# Esperado:
# 1. Botón muestra "Desconectando..." con spinner
# 2. Después de 2 segundos:
#    - Formulario se limpia (campos vacíos)
#    - Mensaje: "Desconectado"
#    - Botón cambia a "Guardar y verificar conexión" (verde)
#    - is_connected = false en BD
```

**✅ Verificar**: Desconexión funciona correctamente

---

## FASE 5: TEST MULTI-TENANT (10 minutos)

### Paso 5.1: Crear Segunda Empresa

```bash
# Registrar otra empresa
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Otra Tienda SA",
    "email": "otra.tienda@sa.com",
    "password": "Test123456!",
    "country": "Colombia"
  }'

# Guardar JWT_TOKEN_2
JWT_TOKEN_2="eyJhbGc..."
```

**✅ Verificar**: Segunda empresa registrada

---

### Paso 5.2: Guardar Credenciales Diferentes en Empresa 2

```bash
curl -X PUT "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN_2" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+57 3 9000 0000",
    "phone_number_id": "9999999999",
    "business_account_id": "5555555555",
    "access_token": "EAAByyyyyyyyyyyyyyyyyyyyy",
    "verify_token": "otro_token_secreto_456"
  }'

# Esperado: Status 200
```

**✅ Verificar**: Empresa 2 tiene sus credenciales

---

### Paso 5.3: Verificar Aislamiento en BD

```sql
-- Conectar a BD

-- Ver todas las conexiones
SELECT vendor_id, phone_number, phone_number_id, business_account_id 
FROM whatsapp_connections;

-- Esperado output:
-- vendor_id | phone_number      | phone_number_id | business_account_id
-- 1         | +57 1 2345 6789   | 1234567890      | 0987654321
-- 2         | +57 3 9000 0000   | 9999999999      | 5555555555

-- Verificar access_tokens diferentes
SELECT vendor_id, access_token FROM whatsapp_connections;
-- Deben ser distintos: TOKEN_1 ≠ TOKEN_2
```

**✅ Verificar**: Dos registros completamente separados

---

### Paso 5.4: Verificar Empresa 1 No Ve Datos de Empresa 2

```bash
# GET con token de Empresa 1
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Esperado: Retorna SOLO datos de Empresa 1
# {
#   "phone_number_id": "1234567890",
#   ...
# }
# NO retorna phone_number_id de Empresa 2

# GET con token de Empresa 2
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN_2"

# Esperado: Retorna SOLO datos de Empresa 2
# {
#   "phone_number_id": "9999999999",
#   ...
# }
```

**✅ Verificar**: Cada empresa solo ve sus datos

---

### Paso 5.5: Test de Webhook Multi-Empresa

```bash
# Webhook con phone_number_id de Empresa 1
curl -X POST "http://localhost:8000/whatsapp/webhook" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "metadata": {
            "phone_number_id": "1234567890"
          },
          "messages": [{
            "from": "5712345678",
            "text": { "body": "Mensaje para Empresa 1" }
          }]
        }
      }]
    }]
  }'

# Backend identifica: vendor_id = 1 (Empresa 1)
# Usa token de Empresa 1

# Webhook con phone_number_id de Empresa 2  
curl -X POST "http://localhost:8000/whatsapp/webhook" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "metadata": {
            "phone_number_id": "9999999999"
          },
          "messages": [{
            "from": "5712345679",
            "text": { "body": "Mensaje para Empresa 2" }
          }]
        }
      }]
    }]
  }'

# Backend identifica: vendor_id = 2 (Empresa 2)
# Usa token de Empresa 2
```

**✅ Verificar**: Cada webhook va a la empresa correcta

---

## FASE 6: VERIFICACIÓN FINAL (5 minutos)

### Checklist de Implementación

- [ ] BD: Tabla `whatsapp_connections` existe con todos los campos
- [ ] BD: Indices creados para búsquedas rápidas
- [ ] Backend: `whatsapp_connection.py` tiene campo `phone_number`
- [ ] Backend: `whatsapp_schema.py` valida credenciales correctamente
- [ ] Backend: `whatsapp_service.py` guarda datos por vendor
- [ ] Backend: `whatsapp_routes.py` maneja PUT, GET, webhooks
- [ ] Frontend: Component carga y prelleña credenciales
- [ ] Frontend: Botón guardaguarda datos correctamente
- [ ] Frontend: Desconexión limpia campos
- [ ] API Test 1: Registro exitoso
- [ ] API Test 2: PUT /whatsapp/me guarda credenciales
- [ ] API Test 3: GET /whatsapp/me retorna sin `access_token`
- [ ] API Test 4: GET webhook verifica token
- [ ] API Test 5: POST webhook procesa mensajes
- [ ] UI Test 1: Página carga sin errores
- [ ] UI Test 2: Formulario aceptavalores
- [ ] UI Test 3: Botón guardar funciona
- [ ] UI Test 4: Reload mantiene datos
- [ ] Multi-tenant 1: Empresa 2 crea credenciales
- [ ] Multi-tenant 2: BD tiene 2 registros separados
- [ ] Multi-tenant 3: Empresa 1 solo ve sus tokens
- [ ] Multi-tenant 4: Webhooks routean correctamente

---

## 📊 RESULTADO ESPERADO

Si todas las fases completaron exitosamente:

✅ **Status**: LISTO PARA PRODUCCIÓN

**Confirmaciones:**
- [x] Base de datos actualizada
- [x] Código backend verificado
- [x] Código frontend verificado  
- [x] Endpoints API funcionales
- [x] Multi-tenancy implementado
- [x] Seguridad verificada
- [x] Webhooks bidireccionales funcionando

---

## 🚑 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| Error: "phone_number column not found" | Ejecutar migración (Paso 1.3) |
| 401 Unauthorized en PUT /whatsapp/me | Verificar JWT token válido |
| 422 Validation Error | Verificar campos requeridos presentes |
| Webhook no procesa | Verificar phone_number_id coincide |
| Credentials no se cargan en refresh | Verificar GET /whatsapp/me retorna datos |
| Error de conexión a BD | Verificar DATABASE_URL en .env |
| Frontend no conecta a API | Verificar VITE_API_URL en .env |

---

**Implementación Completada ✅**  
**Listo para Testing 🧪**  
**Listo para Producción 🚀**

