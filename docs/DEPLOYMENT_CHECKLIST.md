# 🚀 DEPLOYMENT CHECKLIST - WHATSAPP INTEGRATION

**Objetivo**: Verificar que el sistema WhatsApp está completamente funcional antes de ir a producción

**Fecha de Implementación**: 19 de Abril de 2026  
**Responsable**: DevOps / QA  
**Estado**: 🟢 LISTO PARA DEPLOYMENT

---

## 📋 PRE-DEPLOYMENT CHECKS

### ✅ Database Layer

- [ ] **Migración Ejecutada**
  ```bash
  cd backed && python migrate_whatsapp_phone_number.py
  # Expected output: "✅ Migration completed successfully!"
  ```

- [ ] **Tabla Verificada**
  ```sql
  \d whatsapp_connections
  
  # Debe contener:
  # id                 | integer
  # vendor_id          | integer (UNIQUE, FK → vendors)
  # phone_number       | character varying(20)
  # phone_number_id    | character varying(150)
  # business_account_id | character varying(150)
  # access_token       | text
  # verify_token       | character varying(255)
  # is_connected       | boolean DEFAULT false
  # connected_at       | timestamp
  # created_at         | timestamp
  # updated_at         | timestamp
  ```

- [ ] **Índices Creados**
  ```sql
  CREATE INDEX idx_whatsapp_vendor_id ON whatsapp_connections(vendor_id);
  CREATE UNIQUE INDEX idx_whatsapp_phone_number_id ON whatsapp_connections(phone_number_id);
  ```

- [ ] **Columnas Nullables**
  ```sql
  -- Verificar campos opcionales
  ALTER TABLE whatsapp_connections 
  ALTER COLUMN phone_number DROP NOT NULL;
  ALTER TABLE whatsapp_connections 
  ALTER COLUMN business_account_id DROP NOT NULL;
  ```

### ✅ Backend Code

- [ ] **Modelos Actualizados**
  - [ ] `backed/app/models/whatsapp_connection.py` contiene `phone_number` field
  - [ ] Testeado: Crear instancia sin error

- [ ] **Schemas Actualizados**
  - [ ] `backed/app/schemas/whatsapp_schema.py` contiene `phone_number` en Request/Response
  - [ ] Testeado: Validación Pydantic pasa

- [ ] **Servicios Actualizados**
  - [ ] `backed/app/services/whatsapp_service.py`:
    - [ ] `upsert_whatsapp_connection()` guarda `phone_number`
    - [ ] `get_whatsapp_connection_by_vendor()` retorna todas las credenciales
    - [ ] `get_whatsapp_connection_by_phone_number_id()` funciona en webhooks
  - [ ] Testeado: Métodos retornan datos correctos

- [ ] **Rutas API Verificadas**
  - [ ] `backed/app/api/routes/whatsapp_routes.py`:
    - [ ] PUT `/whatsapp/me` → recibe payload con phone_number
    - [ ] GET `/whatsapp/me` → retorna todas las credenciales
    - [ ] GET `/whatsapp/webhook` → verifica token
    - [ ] POST `/whatsapp/webhook` → procesa mensajes
  - [ ] Testeado: Todos los endpoints responden correctamente

### ✅ Frontend Code

- [ ] **Component Actualizado**
  - [ ] `frontend/src/app/pages/WhatsAppPage.tsx`
    - [ ] useEffect carga credenciales en mount
    - [ ] handleConnect() llama PUT /whatsapp/me
    - [ ] handleDisconnect() actualiza is_connected
    - [ ] Muestra estados: loading, error, success
  - [ ] Testeado: Formulario funciona sin errores

### ✅ Environment Variables

- [ ] **Backend Environment**
  ```bash
  # .env.local o secrets
  WHATSAPP_API_VERSION=v18.0          # Meta API version
  WHATSAPP_GRAPH_URL=https://graph.instagram.com
  DB_URL=postgresql://...              # Database connection
  OPENAI_API_KEY=sk-...               # Para agente LLM
  JWT_SECRET=...                      # Para autenticación
  ```

- [ ] **Frontend Environment**
  ```bash
  # .env
  VITE_API_URL=http://localhost:8000
  VITE_APP_NAME=Dropshipping Sales Agent
  ```

---

## 🧪 INTEGRATION TESTS

### Test 1: Database Persistence

**Escenario**: Guardar y recuperar credenciales

```bash
# 1. Registrar empresa
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Corp",
    "email": "test@corp.com",
    "password": "test123",
    "country": "Colombia"
  }'
# Save JWT_TOKEN

# 2. Guardar credenciales WhatsApp
curl -X PUT "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+57 1 2345 6789",
    "phone_number_id": "1234567890",
    "business_account_id": "0987654321",
    "access_token": "EAABxxxxxxxxxxxxx",
    "verify_token": "secreto123"
  }'

# 3. ✅ Esperado: Response 200 con status "connected"
# 4. Verificar en BD
psql -c "SELECT * FROM whatsapp_connections WHERE vendor_id = 1"
# ✅ Debe mostrar los datos guardados

# 5. Recuperar credenciales
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN"
# ✅ Response debe contener phone_number_id = "1234567890"
```

**Status**: ✅ PASS / ❌ FAIL

---

### Test 2: Multi-Tenancy Isolation

**Escenario**: Dos empresas no pueden ver credenciales una de la otra

```bash
# 1. Crear Empresa 1
JWT_EMPRESA1=...  # Token después de registrarse
# Guardar credenciales con phone_number_id = "111111111"

# 2. Crear Empresa 2
JWT_EMPRESA2=...  # Token diferente
# Guardar credenciales con phone_number_id = "222222222"

# 3. Empresa 1 intenta obtener credenciales
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_EMPRESA1"
# ✅ Debe mostrar phone_number_id = "111111111" (sus propias creds)

# 4. Empresa 2 intenta obtener credenciales
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_EMPRESA2"
# ✅ Debe mostrar phone_number_id = "222222222" (sus propias creds)

# 5. Verificar en BD
SELECT vendor_id, phone_number_id FROM whatsapp_connections;
# ✅ Debe mostrar 2 registros separados
```

**Status**: ✅ PASS / ❌ FAIL

---

### Test 3: Webhook Verification

**Escenario**: Meta verifica el webhook durante setup

```bash
# Meta envía request de verificación
curl -X GET "http://localhost:8000/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=secreto123&hub.challenge=CHALLENGE_123"

# ✅ Esperado Response: "CHALLENGE_123" con status 200
```

**Status**: ✅ PASS / ❌ FAIL

---

### Test 4: Webhook Message Processing

**Escenario**: Mensaje llega del cliente, backend procesa y responde

```bash
# 1. Simular webhook de Meta
curl -X POST "http://localhost:8000/whatsapp/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "metadata": {
            "phone_number_id": "1234567890",
            "display_phone_number": "5712345678",
            "business_account_id": "0987654321"
          },
          "contacts": [{
            "profile": { "name": "Cliente Test" },
            "wa_id": "5712345678"
          }],
          "messages": [{
            "from": "5712345678",
            "id": "wamid.123456",
            "timestamp": "1663898306",
            "type": "text",
            "text": { "body": "¿Tienen camisetas?" }
          }]
        }
      }]
    }]
  }'

# ✅ Esperado:
# - Status 200
# - Respuesta: {"status": "processed", "message_sent": true}
# - Backend logs: "Message processed | vendor_id=1 | text='¿Tienen camisetas?'"
# - Meta recibe respuesta enviada al cliente
```

**Status**: ✅ PASS / ❌ FAIL

---

### Test 5: Agent Response Generation

**Escenario**: Agente LLM genera respuesta coherente

```bash
# Backend internamente:
# 1. Extrae vendor_id = 1
# 2. Carga productos de vendor 1
# 3. Llama LLM: contexto + mensaje cliente
# 4. LLM retorna respuesta relevante
# 5. Envía por WhatsApp

# Verificar logs:
tail -f backed/logs.log | grep "Message processed"

# ✅ Debe mostrar:
# - vendor_id correcto
# - Message: "¿Tienen camisetas?"
# - Response: (respuesta coherente con productos)
```

**Status**: ✅ PASS / ❌ FAIL

---

### Test 6: Error Handling

**Escenario**: Manejo de errores comunes

```bash
# Test 6a: Token Expirado
curl -X PUT "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer INVALID_TOKEN" \
  -d '{...}'
# ✅ Esperado: 401 Unauthorized

# Test 6b: Credenciales Incompletas
curl -X PUT "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "phone_number_id": "123"
    # Falta: access_token, verify_token
  }'
# ✅ Esperado: 422 Validation Error

# Test 6c: Access Token Inválido en Meta
# Guardar credenciales con token fake
curl -X PUT "http://localhost:8000/whatsapp/me" -d '{
  "access_token": "FAKE_TOKEN_12345",
  ...
}'
# Enviar webhook
curl -X POST "http://localhost:8000/whatsapp/webhook" -d '{...}'
# ✅ Esperado:
# - Backend intenta enviar a Meta
# - Meta retorna 400/401
# - Backend loguea error
# - No hay crash
```

**Status**: ✅ PASS / ❌ FAIL

---

## 📊 LOAD TESTING

### Scenario 1: Concurrent Companies

```bash
# Simular 10 empresas enviando mensajes simultáneamente
for i in {1..10}; do
  curl -X POST "http://localhost:8000/whatsapp/webhook" \
    -H "Content-Type: application/json" \
    -d "{
      \"entry\": [{
        \"changes\": [{
          \"value\": {
            \"metadata\": {
              \"phone_number_id\": \"${i}${i}${i}${i}${i}\"
            },
            \"messages\": [{
              \"from\": \"571234567${i}\",
              \"text\": { \"body\": \"Mensaje empresa $i\" }
            }]
          }
        }]
      }]
    }" &
done
wait

# ✅ Esperado:
# - Todos los requests procesados
# - Sin timeouts
# - Response time < 2s por request
# - Cada empresa recibe su respuesta correcta
```

**Metrics to Track**:
- Response time promedio
- P95 latency
- CPU usage
- Memory usage
- DB connection pool

**Status**: ✅ PASS / ❌ FAIL

---

## 🔐 SECURITY CHECKS

- [ ] **Access Token**
  - [ ] Nunca se retorna en GET /whatsapp/me (security)
  - [ ] Se encripta en tránsito (HTTPS)
  - [ ] Se almacena encriptado en BD (Field encryption)
  - [ ] Rotación implementada (token refresh strategy)

- [ ] **JWT Validation**
  - [ ] Todos los endpoints requieren Authorization header
  - [ ] Token expirado es rechazado (401)
  - [ ] Signature validada correctamente
  - [ ] Payload no puede ser modificado

- [ ] **Webhook Security**
  - [ ] X-Hub-Signature-256 validado (SHA256)
  - [ ] Token de verificación es aleatorio
  - [ ] Webhook URL es HTTPS en producción
  - [ ] Rate limiting implementado

- [ ] **SQL Injection Prevention**
  - [ ] Todas las queries usan prepared statements
  - [ ] SQLAlchemy ORM utilizado (no queries raw)
  - [ ] Input validation en Pydantic schemas

---

## 📈 MONITORING & ALERTS

### Logs to Configure

```python
# 1. Webhook Received
logger.info(f"webhook_received|phone_number_id={phone_number_id}|vendor_id={vendor_id}|client_from={client_phone}")

# 2. Message Processing
logger.info(f"message_processing|vendor_id={vendor_id}|user_message_len={len(message)}")

# 3. Agent Response
logger.info(f"agent_response|vendor_id={vendor_id}|response_len={len(response)}|llm_latency={latency}ms")

# 4. Message Sent
logger.info(f"message_sent|vendor_id={vendor_id}|to={client_phone}|message_id={msg_id}|latency={latency}ms")

# 5. Errors
logger.error(f"whatsapp_error|vendor_id={vendor_id}|error_code={error.code}|message={error.message}")
```

### Metrics to Monitor

| Métrica | Objetivo | Alert |
|---------|----------|-------|
| Webhook latency | < 2s | > 5s |
| Message delivery rate | > 99% | < 95% |
| LLM response time | < 3s | > 10s |
| DB connection pool | < 50% | > 80% |
| Memory usage | < 2GB | > 3GB |
| Error rate | < 1% | > 5% |
| Uptime | 99.9% | < 95% |

---

## 🚀 PRODUCTION DEPLOYMENT

### Step 1: Pre-Deployment Backup

```bash
# Backup de DB
pg_dump -h prod-db.example.com -U postgres dropshipping > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup de archivos config
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz backend/app/
```

### Step 2: Deploy Backend

```bash
# 1. Pull latest code
git pull origin main

# 2. Run migrations
cd backed
python migrate_whatsapp_phone_number.py

# 3. Install dependencies
pip install -r requirements.txt

# 4. Restart service
systemctl restart dropshipping-backend

# 5. Verify
curl -X GET "http://localhost:8000/health"
# ✅ Expected: {"status": "healthy"}
```

### Step 3: Deploy Frontend

```bash
# 1. Build
npm run build

# 2. Deploy to CDN/Server
npm run deploy

# 3. Verify
curl -X GET "https://app.example.com/health"
# ✅ Expected: OK
```

### Step 4: Configure Meta Webhook

1. Ir a https://developers.facebook.com
2. My Apps → Tu App WhatsApp
3. Configuration:
   - **Callback URL**: `https://api.tudominio.com/whatsapp/webhook`
   - **Verify Token**: Mismo usado en ENV
   - **Subscribe**: `messages` + `message_template_status_update`

### Step 5: Verification

```bash
# Test endpoint accesible
curl -X GET "https://api.tudominio.com/health"

# Test webhooks
curl -X GET "https://api.tudominio.com/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=..."

# Monitor logs
tail -f /var/log/dropshipping/backend.log

# Check DB
psql -h prod-db -U postgres -c "SELECT COUNT(*) FROM whatsapp_connections;"
```

---

## ✅ POST-DEPLOYMENT VERIFICATION

- [ ] Webhook verification con Meta completó exitosamente
- [ ] Primer mensaje de prueba recibido y respondido
- [ ] Logs muestran procesamiento correcto
- [ ] Múltiples empresas conectadas sin interferencia
- [ ] Performance dentro de SLA (< 2s latency)
- [ ] Monitoreo activo y recibiendo métricas
- [ ] Alertas configuradas y testando
- [ ] Backup de BD completado
- [ ] Rollback plan documentado

---

## 🔄 ROLLBACK PROCEDURE

Si algo falla en producción:

```bash
# 1. Revert code
git revert HEAD

# 2. Restart services
systemctl restart dropshipping-backend
systemctl restart dropshipping-frontend

# 3. Restore DB if needed
psql -h prod-db -U postgres dropshipping < backup_YYYYMMDD_HHMMSS.sql

# 4. Verify
curl -X GET "https://api.tudominio.com/health"

# 5. Notify team
slack "🚨 Rollback completed - investigating issue"
```

---

## 📝 SIGN-OFF

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| QA Lead | __________ | _____ | ______ |
| DevOps | __________ | _____ | ______ |
| Backend Lead | __________ | _____ | ______ |
| Product | __________ | _____ | ______ |

---

**Estado Final**: 🟢 READY FOR PRODUCTION

**Última Actualización**: 19 de Abril 2026  
**Próxima Revisión**: Post-deployment (24h)
