# 🔧 DEBUG VISUAL - GRAPH API REQUESTS VS RESPONSES

## Guía Rápida: ¿Qué estás haciendo mal?

###

 Escenario 1: POST a ID Incorrecto

```
┌─────────────────────────────────────────────────────────────┐
│ ❌ REQUEST INCORRECTO (Probablemente lo que haces ahora)    │
└─────────────────────────────────────────────────────────────┘

POST https://graph.facebook.com/v25.0/1095201550345996/messages
Authorization: Bearer EAAMGYyYgJogBR...
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "573169701688",
  "type": "text",
  "text": { "body": "Hola" }
}

┌─────────────────────────────────────────────────────────────┐
│ ❌ RESPONSE DEL ERROR                                        │
└─────────────────────────────────────────────────────────────┘

HTTP/1.1 400 Bad Request

{
  "error": {
    "message": "Solicitud de publicación no compatible. El objeto con ID 
               '1095201550345996' no existe, no se puede cargar debido a 
               la falta de permisos o no admite esta operación.",
    "type": "GraphMethodException",
    "code": 3,
    "fbtrace_id": "Axxx..."
  }
}

┌─────────────────────────────────────────────────────────────┐
│ ✅ REQUEST CORRECTO                                          │
└─────────────────────────────────────────────────────────────┘

POST https://graph.facebook.com/v25.0/989003167640614/messages
                                    ↑
                         PHONE_NUMBER_ID correcto

Authorization: Bearer EAAMGYyYgJogBR...
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "573169701688",
  "type": "text",
  "text": { "body": "Hola" }
}

┌─────────────────────────────────────────────────────────────┐
│ ✅ RESPONSE EXITOSO                                          │
└─────────────────────────────────────────────────────────────┘

HTTP/1.1 200 OK

{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "573169701688",
      "wa_id": "573169701688"
    }
  ],
  "messages": [
    {
      "id": "wamid.xxx..."
    }
  ]
}
```

---

## Escenario 2: Headers Faltantes o Incorrectos

```
┌─────────────────────────────────────────────────────────────┐
│ ❌ INCORRECTO - Headers faltantes                            │
└─────────────────────────────────────────────────────────────┘

POST https://graph.facebook.com/v25.0/989003167640614/messages
# ❌ Falta: Authorization header
# ❌ Falta: Content-Type header

{
  "messaging_product": "whatsapp",
  "to": "573169701688",
  "type": "text",
  "text": { "body": "Hola" }
}

Response:
{
  "error": {
    "message": "An access token is required to request this resource.",
    "type": "OAuthException",
    "code": 104
  }
}

┌─────────────────────────────────────────────────────────────┐
│ ✅ CORRECTO - Headers completos                             │
└─────────────────────────────────────────────────────────────┘

POST https://graph.facebook.com/v25.0/989003167640614/messages
Authorization: Bearer EAAMGYyYgJogBRdcJDJvGchUBoej5m...  ← REQUERIDO
Content-Type: application/json                            ← REQUERIDO

{
  "messaging_product": "whatsapp",
  "to": "573169701688",
  "type": "text",
  "text": { "body": "Hola" }
}

Response: ✅ 200 OK
```

---

## Escenario 3: Token Expirado

```
┌─────────────────────────────────────────────────────────────┐
│ ❌ Token Expirado o Inválido                                 │
└─────────────────────────────────────────────────────────────┘

Authorization: Bearer invalid_or_expired_token

Response:
{
  "error": {
    "message": "Invalid OAuth access token.",
    "type": "OAuthException",
    "code": 190,
    "error_subcode": 1
  }
}

┌─────────────────────────────────────────────────────────────┐
│ ✅ Token Válido                                              │
└─────────────────────────────────────────────────────────────┘

Authorization: Bearer EAAXXX...  # Token que empieza con EAA y tiene >100 chars

Response: ✅ 200 OK (mensaje enviado exitosamente)
```

---

## Escenario 4: Body JSON Incorrecto

```
┌─────────────────────────────────────────────────────────────┐
│ ❌ JSON Inválido o Campos Faltantes                          │
└─────────────────────────────────────────────────────────────┘

{
  "to": "573169701688",
  "type": "text",
  "text": { "body": "Hola" }
  # ❌ Falta: "messaging_product": "whatsapp"
}

Response:
{
  "error": {
    "message": "INVALID_PARAM: Invalid parameter: messaging_product",
    "type": "OAuthException",
    "code": 100
  }
}

┌─────────────────────────────────────────────────────────────┐
│ ✅ JSON Correcto                                             │
└─────────────────────────────────────────────────────────────┘

{
  "messaging_product": "whatsapp",  ← REQUERIDO
  "to": "573169701688",              ← REQUERIDO
  "type": "text",                    ← REQUERIDO
  "text": {                          ← REQUERIDO
    "body": "Hola"                   ← REQUERIDO
  }
}

Response: ✅ 200 OK
```

---

## Escenario 5: Webhook Verification

```
┌─────────────────────────────────────────────────────────────┐
│ ❌ Verificación Falla - Verify Token Incorrecto             │
└─────────────────────────────────────────────────────────────┘

GET https://tu-dominio.com/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=wrong_token&hub.challenge=abc123

Backend busca en BD por verify_token
No coincide (guardaste "correct_token" pero Meta envía "wrong_token")

Response:
HTTP 403 Forbidden
"Invalid verification token"

Resultado:
❌ Meta NO verifica tu webhook
❌ Meta no puede enviar mensajes a tu dirección

┌─────────────────────────────────────────────────────────────┐
│ ✅ Verificación Exitosa - Token Correcto                    │
└─────────────────────────────────────────────────────────────┘

GET https://tu-dominio.com/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=correct_token&hub.challenge=abc123

Backend busca en BD por verify_token
✅ Encuentra: "correct_token" (coincide)

Response:
HTTP 200 OK
Content: abc123  ← Echo del challenge

Resultado:
✅ Meta VERIFICA tu webhook exitosamente ✅
✅ Meta puede enviar mensajes a tu dirección ✅
```

---

## Checklist: Debugging paso a paso

### Paso 1: Verifica los IDs
```powershell
# Abre Meta Developer Console
https://developers.facebook.com/tools/explorer/

# Ejecuta esta consulta:
GET /2479057362544519?fields=phone_numbers

# Resultado esperado:
{
  "phone_numbers": {
    "data": [
      {
        "id": "989003167640614",  ← Si ves esto: ID CORRECTO
        "display_phone_number": "+1 555 636 6119"
      }
    ]
  }
}

# Resultado incorrecto:
# Si aparece "error": {...} → Algo está mal con tu account
```

### Paso 2: Verifica el Token
```powershell
# Abre Meta Developer Console con el token
# Ejecuta:
GET /me

# Resultado esperado:
{
  "id": "TU_USER_ID",
  "name": "Tu Nombre",
  "email": "tu@email.com"
}

# Si ves error: Token inválido o expirado
```

### Paso 3: Prueba el Endpoint de Mensajes
```powershell
# En PowerShell:
$headers = @{
    "Authorization" = "Bearer EAA..."
    "Content-Type" = "application/json"
}

$body = @{
    "messaging_product" = "whatsapp"
    "to" = "573169701688"  # Cambia al número correcto
    "type" = "text"
    "text" = @{ "body" = "Test message" }
} | ConvertTo-Json

curl -i -X POST `
  https://graph.facebook.com/v25.0/989003167640614/messages `
  -H $headers `
  -d $body

# Response esperado:
# HTTP/1.1 200 OK
# {"messages": [{"id":"wamid.xxx"}]}
```

### Paso 4: Verifica Webhook
```powershell
# Abre tu navegador y accede a:
https://tu-dominio.com/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=my_token&hub.challenge=test123

# Resultado esperado en navegador:
test123

# Si ves error o página en blanco:
❌ Webhook endpoint incorrecto
❌ Verify token no coincide
❌ Backend no está corriendo
```

---

## Matriz de Solución de Problemas

| Error | Cause | Solución |
|-------|-------|----------|
| "El objeto no existe" | ID incorrecto | Uscar 989003167640614 |
| "Access token required" | Falta Authorization header | Agregar: Authorization: Bearer EAA... |
| "Invalid OAuth token" | Token expirado | Regenerar token en Meta |
| "Missing parameter" | Falta campo en JSON | Incluir todos los campos requeridos |
| "Webhook verification failed" | Verify token incorrecto | Verificar que coincida en Meta y BD |
| "Permission denied" | Permisos insuficientes | Token debe tener scope whatsapp* |
| "Rate limit exceeded" | Demasiadas solicitudes | Esperar o aumentar límite en Meta |

---

## Comandos de Debug Útiles

### Ver logs del backend
```powershell
# En tu terminal del backend:
# Los logs mostrarán errores exactos cuando falle una solicitud
```

### Monitorear webhooks
```powershell
# Usa Webhook.site para ver exactamente qué Meta te envía:
# 1. Abre https://webhook.site
# 2. Copia tu URL única
# 3. Usa esa URL en Meta → Configuration → Webhook URL
# 4. Envía un mensaje de prueba
# 5. Verás exactamente qué Meta envía
```

### Decodificar JWT Token (si es necesario)
```powershell
# En https://jwt.io:
# 1. Pega tu token
# 2. Verás payload, expiration, permisos
```

---

## 🎯 Conclusión

La mayoría de los errores se reducen a:

1. ✅ **ID correcto**: 989003167640614 (NO 1095201550345996)
2. ✅ **Headers completos**: Authorization + Content-Type
3. ✅ **JSON válido**: Todos los campos requeridos
4. ✅ **Token válido**: No expirado, con permisos
5. ✅ **Webhook verificado**: Verify token coincide

Si sigues nuestros scripts (`configure_whatsapp.py` y `test_whatsapp.py`), todo esto es validado automáticamente.
