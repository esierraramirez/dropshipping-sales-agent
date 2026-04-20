# 📱 Guía de Configuración WhatsApp Business API

## 🎯 Objetivo Final
Cuando un cliente escriba a tu número de WhatsApp (+57 316 9701688 o el de prueba), el agente responda automáticamente desde tu application.

---

## ⚠️ ERROR COMÚN - SOLUCIÓN INMEDIATA

### ❌ El Problema
**Error**: "Solicitud de publicación no compatible. El objeto con ID '1095201550345996' no existe"

### ✅ La Solución
Asegúrate de usar los IDs CORRECTOS que WhatsApp te proporciona:

| Parámetro | Tu Valor | Dónde Usarlo |
|-----------|----------|--------------|
| **Phone Number ID** | `989003167640614` | Enviar mensajes + Webhook |
| **Business Account ID** | `2479057362544519` | Configuración de webhooks |
| **Access Token** | El token largo que tienes | Headers de autorización |
| ❌ **NO usar** | `1095201550345996` | Este ID es incorrecto |

---

## 📋 Paso 1: Verifica tus Credenciales en Meta

**URL**: https://developers.facebook.com/apps

1. Selecciona tu app
2. Ve a **WhatsApp** → **API Setup**
3. En la sección "Seleccionar números de teléfono":
   - ✅ Copia **Identificador de número de teléfono**: `989003167640614`
   - ✅ Copia **Identificador de la cuenta de WhatsApp Business**: `2479057362544519`
   - ✅ Genera nuevo token si es necesario

**Resultado esperado**: Tienes 3 datos críticos

```
Phone Number ID:      989003167640614
Business Account ID:  2479057362544519
Access Token:         EAAMGYyYg... (token largo)
```

---

## 🔒 Paso 2: Configura el Punto Final de Webhook

Tu backend ya tiene listo:
- **Ruta de verificación**: `GET /whatsapp/webhook?hub.mode=subscribe&hub.verify_token=...`
- **Ruta de recepción**: `POST /whatsapp/webhook`

### Opción A: Desarrollo Local (NGROK)

```powershell
# 1. Descarga ngrok desde https://ngrok.com/download
# 2. En PowerShell, ve a la carpeta donde descargaste ngrok:

.\ngrok.exe http 8000

# Verás un output como:
# Forwarding     https://abc123def456.ngrok.io -> http://localhost:8000

# Copia la URL: https://abc123def456.ngrok.io
```

### Opción B: Producción (Tu Servidor)
- URL: `https://tu-dominio.com` (reemplaza con tu dominio)

---

## 🔐 Paso 3: Registra la Conexión en tu BD

Usa el **endpoint de tu backend** para guardar las credenciales de WhatsApp:

### Endpoint
```
PUT http://localhost:8000/whatsapp/me
```

### Headers
```
Authorization: Bearer {tu_jwt_token}
Content-Type: application/json
```

### Body (Reemplaza los valores)
```json
{
  "phone_number": "+1 555 636 6119",
  "phone_number_id": "989003167640614",
  "business_account_id": "2479057362544519",
  "access_token": "EAAMGYyYgJogBRdcJDJvGchUBoej5mDWAtHgt45mauftgwXRXX0RhTjj2ulWyDTQXwd3ZCmXZArCDmXwzlPtJQxWiEwo7EzzIk1aoxOMO4pDuyYNrYrjlHVZADaWr53CrXpiHXYGxJhWSuyXuekuUaKmRKW7bMUO4OTbZAX1u8N7te4sAnbRCTY18ApmYU7jS79CsawGwmazXDryo6lQnMPqBv9FLGjYZC5S8KkJfGpFnPQc0PfPqHOqMpJkJiOxMCCfXqIphZBfodLTrJodyqId0cf",
  "verify_token": "mi_super_clave_secreta_2024"
}
```

### Probar con CURL
```powershell
$headers = @{
    "Authorization" = "Bearer eyJhbGc..."  # Tu JWT token
    "Content-Type" = "application/json"
}

$body = @{
    phone_number = "+1 555 636 6119"
    phone_number_id = "989003167640614"
    business_account_id = "2479057362544519"
    access_token = "EAAMGYyYgJog..."
    verify_token = "mi_super_clave_secreta_2024"
} | ConvertTo-Json

Invoke-WebRequest `
    -Uri "http://localhost:8000/whatsapp/me" `
    -Method PUT `
    -Headers $headers `
    -Body $body
```

**Resultado esperado**: Code 200 con tu conexión guardada

---

## ⚙️ Paso 4: Configura el Webhook en Meta

1. Ve a: https://developers.facebook.com/apps → Tu app → **WhatsApp** → **Configuration**

2. **Webhook y suscripción a eventos**:

   | Campo | Valor |
   |-------|-------|
   | **Webhook URL** | `https://abc123def456.ngrok.io/whatsapp/webhook` (usa tu URL de ngrok o dominio) |
   | **Verify Token** | `mi_super_clave_secreta_2024` (el mismo que usaste en Paso 3) |

3. **Suscribirse a eventos de webhook**:
   - ✅ `messages`
   - ✅ `message_status`

4. Haz clic en **Guardar**

**Importante**: El `verify_token` que pongas aquí debe ser IDÉNTICO al que guardaste en Paso 3.

---

## 🧪 Paso 5: Prueba tu Configuración

### 5a. Verifica el Webhook
Meta enviará automáticamente un `GET` para verificar tu webhook:

```
GET https://tu-url-ngrok.com/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=mi_super_clave_secreta_2024&hub.challenge=abc123xyz
```

Tu backend debe responder con el `challenge` (esto ya está programado).

### 5b. Envía un Mensaje de Prueba desde WhatsApp

En la página de **API Setup** de Meta, está la sección "Enviar y recibir mensajes":

1. Selecciona el número **de prueba** como destinatario
2. Haz clic en **"Enviar mensaje de prueba"**
3. Ingresa un teléfono (puede ser el tuyo +57 3169701688)
4. Envía el mensaje

**Lo que debería ocurrir**:
- El cliente recibe un mensaje de prueba en WhatsApp ✅
- Tu servidor recibe un `POST /whatsapp/webhook` ✅
- El agente genera una respuesta ✅
- Se envía un mensaje de vuelta por WhatsApp ✅

---

## 🔄 Flujo Completo Una Vez Configurado

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE EN WHATSAPP                   │
│              "Hola, quiero saber sobre productos"            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
          ┌─────────────────────────────────────┐
          │      META WHATSAPP CLOUD API         │
          │  Envía POST a tu webhook URL         │
          └────────────────┬────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │    TU BACKEND: POST /whatsapp/webhook     │
        │  (whatsapp_routes.py)                    │
        └────────────────┬─────────────────────────┘
                         │
                         ▼
    ┌────────────────────────────────────────────────────┐
    │  1. Extrae mensaje: "Hola, quiero saber sobre..." │
    │  2. Busca empresa por phone_number_id             │
    │  3. Llama al agente: generate_agent_reply()       │
    │  4. Agente busca productos en BD                  │
    │  5. LLM genera respuesta natural                  │
    │  6. Intenta crear orden si es confirmación        │
    └────────────────┬─────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────────────────┐
    │  Respuesta del agente:                             │
    │  "¡Hola! Soy el asistente de [Tu Empresa]...     │
    │   Tenemos 5 productos disponibles..."              │
    └────────────────┬─────────────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────────────────────┐
        │  POST a META para enviar respuesta        │
        │  graph.facebook.com/v25.0/               │
        │  {phone_number_id}/messages              │
        └────────────────┬─────────────────────────┘
                         │
                         ▼
          ┌─────────────────────────────────────┐
          │      META WHATSAPP CLOUD API         │
          │   Distribuye mensaje a cliente       │
          └─────────────────┬───────────────────┘
                            │
                            ▼
   ┌──────────────────────────────────────────────┐
   │         CLIENTE RECIBE EN WHATSAPP            │
   │  "¡Hola! Soy el asistente de [Tu Empresa]   │
   │   Tenemos estos productos disponibles:..."   │
   └──────────────────────────────────────────────┘
```

---

## 🆘 Solución de Problemas

### Error: "Token ID '1095201550345996' no existe"
**Causa**: Estás usando un ID incorrecto
**Solución**: Verifica que uses `989003167640614` (el phone_number_id correcto)

### Error: "Webhook verification failed"
**Causa**: El `verify_token` no coincide
**Solución**: 
1. Verifica que sea exactamente igual en Meta y en tu BD
2. Reinicia el backend
3. Intenta verificar de nuevo en Meta

### No llega ningún mensaje
**Causa**: El webhook URL es incorrecto o ngrok se desconectó
**Solución**:
1. Verifica que la URL en Meta sea correcta
2. Si usas ngrok, reinicia y copia la nueva URL
3. Prueba con: `curl https://tu-url/whatsapp/webhook` desde terminal

### El agente no responde
**Causa**: Backend no está configurado correctamente
**Solución**:
1. Verifica que backend esté corriendo en puerto 8000
2. Revisa los logs: `tail -f /ruta/a/logs/backend.log`
3. Asegúrate que las credenciales están guardadas en BD usando PUT /whatsapp/me

---

## 📝 Checklist Final

- [ ] Tengo los 3 IDs correctos de Meta (Phone ID, Business ID, Access Token)
- [ ] Ejecuté PUT /whatsapp/me con mis credenciales
- [ ] Tengo ngrok corriendo o un dominio público para webhook
- [ ] Configuré el webhook URL en Meta
- [ ] El verify_token en Meta coincide con el de mi BD
- [ ] Suscribí a eventos: messages y message_status
- [ ] El backend está corriendo en puerto 8000
- [ ] Probé enviando un mensaje de prueba desde Meta
- [ ] Recibí el POST en /whatsapp/webhook
- [ ] El agente respondió automáticamente

---

## 🚀 Próximos Pasos

Una vez funcionando:

1. **Agregar tu número real** (+57 316 9701688):
   - En Meta, ve a **Administrador de WhatsApp**
   - Agrega y verifica tu número real
   - Obtén el nuevo phone_number_id
   - Actualiza con PUT /whatsapp/me

2. **Configurar el método de pago** en Meta para enviar mensajes ilimitados

3. **Probar conversación completa**:
   - Cliente: "Hola, quiero este producto"
   - Agente: Presenta opciones
   - Cliente: "Confirmo mi compra"
   - Backend: Crea orden automáticamente
   - Agente: "✅ Tu orden quedó registrada"

---

## 📞 Contacto / Soporte

Si algo falla:
1. Revisa los logs del backend: `app.log`
2. Verifica en Meta que el webhook URL sea accesible
3. Confirma que todos los IDs sean correctos
4. Intenta de nuevo desde cero con ngrok fresco
