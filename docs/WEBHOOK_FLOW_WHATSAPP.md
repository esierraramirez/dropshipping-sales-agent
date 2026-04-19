# 📨 WEBHOOK FLOW - WHATSAPP INCOMING MESSAGES

**Propósito**: Documentar flujo completo de recibimiento y procesamiento de mensajes de WhatsApp

---

## 1. 🔄 ARQUITECTURA DE WEBHOOK

### Diagrama de Flujo

```
┌─────────────────────────────────────┐
│ Cliente WhatsApp (ej: +57 300 123 4567)
│ Envía: "¿Tienen camisetas negras?"
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Meta Cloud API     │
        │ (WhatsApp Servers) │
        └────────┬───────────┘
                 │ Cloud API busca configuración
                 │ del número: phone_number_id=1234567890
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │ Backend: POST /whatsapp/webhook      │
        │ Recibe: webhook payload              │
        │ Extrae: metadata.phone_number_id     │
        └────────┬──────────────────────────────┘
                 │
                 ▼
        ┌──────────────────────────────────────┐
        │ Backend: process_incoming_whatsapp... │
        │ 1. Busca en BD:                       │
        │    SELECT vendor FROM whatsapp_...   │
        │    WHERE phone_number_id = 1234567890│
        │ 2. Obtiene: vendor_id = 123         │
        └────────┬───────────────────────────────┘
                 │
                 ▼
        ┌──────────────────────────────────────┐
        │ Agent: generate_agent_reply()        │
        │ 1. Carga inventario vendor 123      │
        │ 2. Procesa query: categorizar,       │
        │    buscar productos                  │
        │ 3. Genera respuesta LLM             │
        │ = "Sí, tenemos camisetas negras..." │
        └────────┬───────────────────────────────┘
                 │
                 ▼
        ┌──────────────────────────────────────┐
        │ Backend: send_whatsapp_text_message()│
        │ 1. Obtiene credentials:              │
        │    - access_token                    │
        │    - phone_number_id                 │
        │ 2. Llama Meta API con POST request   │
        │ 3. Envía respuesta al cliente        │
        └────────┬───────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Meta Cloud API     │
        │ Envía mensaje      │
        └────────┬───────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │ Cliente recibe: "Sí, tenemos..."    │
        │ WhatsApp de empresa +57 1 2345 6789 │
        └─────────────────────────────────────┘
```

---

## 2. 📥 WEBHOOK REQUEST - META TO BACKEND

### Formato de Mensajes Entrantes

```json
{
  "entry": [
    {
      "id": "123456789",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "5712345678",
              "phone_number_id": "1234567890",
              "business_account_id": "0987654321"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Juan Pérez"
                },
                "wa_id": "5712345678"
              }
            ],
            "messages": [
              {
                "from": "5712345678",
                "id": "wamid.xxxxx",
                "timestamp": "1663898306",
                "type": "text",
                "text": {
                  "body": "¿Tienen camisetas negras?"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Extracción de Datos Clave

| Campo | Tipo | Uso | Ejemplo |
|-------|------|-----|---------|
| `metadata.phone_number_id` | str | 🔑 Identificar empresa | "1234567890" |
| `metadata.display_phone_number` | str | Mostrar número | "57 1 2345 6789" |
| `messages[0].from` | str | ID cliente | "5712345678" |
| `messages[0].text.body` | str | Mensaje del cliente | "¿Tienen camisetas?" |
| `messages[0].timestamp` | str | Hora (Unix) | "1663898306" |
| `contacts[0].profile.name` | str | Nombre cliente | "Juan Pérez" |

---

## 3. 🔐 BACKEND WEBHOOK VERIFICATION

### Endpoint: GET /whatsapp/webhook

**Propósito**: Meta envía request de verificación al configurar webhook

**Request (Meta → Backend):**
```
GET /whatsapp/webhook?hub.mode=subscribe&hub.verify_token=MI_TOKEN_SECRETO&hub.challenge=CHALLENGE_STRING_123
```

**Código Backend:**
```python
@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None),
    hub_verify_token: str = Query(None),
    hub_challenge: str = Query(None)
):
    # 1. Obtener verify_token guardado en BD del vendor
    # 2. Comparar con hub_verify_token de Meta
    
    if hub_verify_token == SAVED_VERIFY_TOKEN:
        # ✅ Token válido
        return hub_challenge  # Meta valida que somos nosotros
    else:
        # ❌ Token inválido
        return {"error": "Unauthorized"}, 403
```

**Response (200 OK):**
```
CHALLENGE_STRING_123
```

---

## 4. 📨 BACKEND WEBHOOK HANDLER

### Endpoint: POST /whatsapp/webhook

**Request (Meta → Backend):**
```json
POST http://api.tudominio.com/whatsapp/webhook
Content-Type: application/json

{
  "entry": [{
    "changes": [{
      "value": {
        "metadata": {
          "phone_number_id": "1234567890"
        },
        "messages": [{
          "from": "5712345678",
          "text": { "body": "¿Tienen camisetas?" }
        }]
      }
    }]
  }]
}
```

**Procesamiento Backend (sequence):**

```python
@router.post("/webhook")
async def receive_webhook(
    body: dict,
    db: Session = Depends(get_db)
):
    # 1️⃣ EXTRAER phone_number_id del webhook
    phone_number_id = body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
    # Result: "1234567890"
    
    # 2️⃣ BUSCAR QUE EMPRESA TIENE ESTE NÚMERO
    connection = db.query(WhatsAppConnection).filter(
        WhatsAppConnection.phone_number_id == phone_number_id
    ).first()
    # Result: WhatsAppConnection(vendor_id=123, access_token=..., is_connected=True)
    
    if not connection:
        return {"error": "Phone number not configured"}, 404
    
    # 3️⃣ OBTENER INFORMACIÓN DEL CLIENTE
    vendor_id = connection.vendor_id
    client_phone = body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    message_text = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
    # Results: 
    # vendor_id = 123
    # client_phone = "5712345678"
    # message_text = "¿Tienen camisetas?"
    
    # 4️⃣ LLAMAR AL AGENTE LLM
    response_text = await generate_agent_reply(
        vendor_id=vendor_id,
        user_message=message_text,
        user_phone=client_phone,
        db=db
    )
    # Result: "Sí, tenemos camisetas en negro, azul y blanco..."
    
    # 5️⃣ ENVIAR RESPUESTA POR WHATSAPP
    await send_whatsapp_text_message(
        vendor_id=vendor_id,
        recipient_phone=client_phone,
        message=response_text,
        db=db
    )
    # Usa connection.access_token y connection.phone_number_id
    
    # 6️⃣ RESPONDER A META CON 200
    return {"status": "processed"}, 200
```

**Response (200 OK):**
```json
{
  "status": "processed",
  "message_sent": true,
  "response": "Sí, tenemos camisetas negras..."
}
```

---

## 5. 📤 RESPUESTA A CLIENTE - SEND MESSAGE

### Service: send_whatsapp_text_message()

**InputParameters:**
```python
vendor_id = 123
recipient_phone = "5712345678"  # Sin + ni espacios
message = "Sí, tenemos camisetas negras en stock..."
db = Session
```

**Lectura de Credentials:**
```python
# Leer credenciales guardadas por empresa
connection = db.query(WhatsAppConnection).filter(
    WhatsAppConnection.vendor_id == vendor_id
).first()

# connection.access_token = "EAABxxxxxxxxxxxxx"
# connection.phone_number_id = "1234567890"
```

**Call to Meta API:**
```python
url = f"https://graph.instagram.com/v18.0/{connection.phone_number_id}/messages"

headers = {
    "Authorization": f"Bearer {connection.access_token}",
    "Content-Type": "application/json"
}

payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": recipient_phone,  # "5712345678"
    "type": "text",
    "text": {
        "body": message
    }
}

# POST request
response = requests.post(url, json=payload, headers=headers)
```

**Success Response (200 OK):**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [{
    "input": "5712345678",
    "wa_id": "5712345678"
  }],
  "messages": [{
    "id": "wamid.xxxxx"
  }]
}
```

**Error Response (Ejemplos):**

```json
{
  "error": {
    "message": "Invalid access token",
    "type": "OAuthException",
    "code": 190
  }
}
```

---

## 6. 🧠 AGENT REPLY GENERATION

### Service: generate_agent_reply()

**Parameters:**
```python
vendor_id = 123
user_message = "¿Tienen camisetas negras?"
user_phone = "5712345678"
db = Session
```

**Internal Process:**

```
1. LOAD VENDOR INFO
   - vendor = db.query(Vendor).filter(Vendor.id == 123).first()
   - Result: Vendor(name="Mi Tienda", email="...", country="Colombia")

2. LOAD PRODUCTS (RAG - Retrieval)
   - retriever = get_retriever(vendor_id=123)
   - similar_products = retriever.retrieve(query="camisetas negras")
   - Result: [{name: "Camiseta Negra M", price: 25.99}, ...]

3. CRAFT CONTEXT
   context = f"""
   Eres agente de ventas de {vendor.name}.
   Productos disponibles: {similar_products}
   Mensaje del cliente: {user_message}
   """

4. CALL LLM (OpenAI)
   response = openai.ChatCompletion.create(
       model="gpt-4",
       messages=[{
           "role": "system",
           "content": "Eres agente amable de ventas..."
       }, {
           "role": "user",
           "content": context
       }],
       max_tokens=500
   )
   
   Result: "Sí, tenemos camisetas negras disponibles..."

5. SAVE CONVERSATION (Optional)
   - Guardar en chat_history (vendor_id, user_phone, message, response)

6. RETURN RESPONSE
   return response
```

---

## 7. 🔒 MULTI-TENANCY SECURITY

### Verificación de Aislamiento

```python
# ✅ EMPRESA 1 CONECTA
company1_credentials = {
    "vendor_id": 1,
    "phone_number_id": "111111111",
    "access_token": "TOKEN_EMPRESA_1",
    "business_account_id": "BAA_1"
}
# Guardadas en BD con vendor_id = 1

# ✅ EMPRESA 2 CONECTA
company2_credentials = {
    "vendor_id": 2,
    "phone_number_id": "222222222",
    "access_token": "TOKEN_EMPRESA_2",
    "business_account_id": "BAA_2"
}
# Guardadas en BD con vendor_id = 2

# ❌ WEBHOOK LLEGA CON phone_number_id = "111111111"
webhook_payload = {..., "phone_number_id": "111111111"}

# ✅ BACKEND BUSCA
connection = db.query(WhatsAppConnection).filter(
    WhatsAppConnection.phone_number_id == "111111111"
).first()
# Resultado: vendor_id = 1 (EMPRESA 1)
# access_token = "TOKEN_EMPRESA_1"

# ✅ RESPUESTA ENVIADA CON TOKEN_EMPRESA_1
# → Mensaje sale desde WhatsApp de EMPRESA 1 solo
# → Respuesta generada con productos de EMPRESA 1 solo

# ✅ EMPRESA 2 NUNCA VE DATOS DE EMPRESA 1
```

---

## 8. 📊 LOGGING & MONITORING

### Events a Registrar

```python
# Cada webhook que llega:
logger.info(f"Webhook received | phone_number_id={phone_number_id} | vendor_id={vendor_id} | from={client_phone}")

# Mensaje procesado:
logger.info(f"Message processed | vendor_id={vendor_id} | user_message={message_text} | response_len={len(response)}")

# Mensaje enviado:
logger.info(f"Message sent | vendor_id={vendor_id} | to={client_phone} | status=success")

# Errores:
logger.error(f"Failed to send | vendor_id={vendor_id} | error={error}")
```

---

## 9. ✅ VERIFICATION CHECKLIST

### Frontend → Backend

- [ ] Frontend: FormularioBienUX en http://localhost:5173/whatsapp
- [ ] Frontend: Campos se cargan con GET /whatsapp/me
- [ ] Frontend: POST guardar credenciales con PUT /whatsapp/me
- [ ] Backend: PUT /whatsapp/me recibe y guarda en BD

### Backend → Database

- [ ] whatsapp_connections tabla existe con todos los campos
- [ ] vendor_id foreign key apunta a vendors table
- [ ] phone_number_id indexado para búsquedas rápidas
- [ ] access_token encriptado en tránsito

### Database → Meta API (Webhook Incoming)

- [ ] Meta Cloud API está configurado con webhook URL
- [ ] Webhook token coincide en Meta + BD
- [ ] Backend recibe POST en /whatsapp/webhook
- [ ] phone_number_id extraído correctamente

### Agent Processing

- [ ] Agent LLM accesa productos de vendor correcto
- [ ] Respuesta se genera en idioma correcto
- [ ] Respuesta es coherente con el inventario

### Backend → Meta API (Webhook Outgoing)

- [ ] send_whatsapp_text_message() usa credentials correctas
- [ ] access_token no expirado
- [ ] phone_number_id válido
- [ ] Mensaje enviado exitosamente a cliente

---

## 10. 🧪 TEST SCRIPT

```bash
#!/bin/bash

# Test 1: Verify webhook endpoint
echo "1️⃣ Testing GET /whatsapp/webhook..."
curl -X GET "http://localhost:8000/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=secreto123&hub.challenge=TEST_CHALLENGE"

# Test 2: Save credentials
echo "\n2️⃣ Testing PUT /whatsapp/me..."
curl -X PUT "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+57 1 2345 6789",
    "phone_number_id": "1234567890",
    "business_account_id": "0987654321",
    "access_token": "EAABxxxxx",
    "verify_token": "secreto123"
  }'

# Test 3: Get credentials
echo "\n3️⃣ Testing GET /whatsapp/me..."
curl -X GET "http://localhost:8000/whatsapp/me" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"

# Test 4: Simulate incoming webhook
echo "\n4️⃣ Testing POST /whatsapp/webhook..."
curl -X POST "http://localhost:8000/whatsapp/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "metadata": {
            "phone_number_id": "1234567890"
          },
          "contacts": [{
            "profile": { "name": "Juan Test" },
            "wa_id": "5712345678"
          }],
          "messages": [{
            "from": "5712345678",
            "text": { "body": "¿Tienen camisetas?" }
          }]
        }
      }]
    }]
  }'
```

---

**Referencia**: Este documento describe el flujo de webhooks bidireccional WhatsApp ↔ Backend
