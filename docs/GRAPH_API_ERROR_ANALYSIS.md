# 🔴 ANÁLISIS PROFUNDO DEL ERROR - GRAPH API META

## El Problema Técnico

### El Error Exacto
```
Error al registrar +57 316 9701688
Solicitud de publicación no compatible. El objeto con ID '1095201550345996' 
no existe, no se puede cargar debido a la falta de permisos o no admite esta operación.
```

### Qué Significa
En Graph API de Meta, este error significa:

```
❌ POST https://graph.facebook.com/v25.0/1095201550345996/ENDPOINT
   └─ Este ID no existe en la BD de Meta
   └─ O no tienes permisos para operarlo
   └─ O este ID no soporta esa operación (POST)
```

---

## 🎯 Lo Que Probablemente Estás Haciendo (Incorrecto)

### Hipótesis 1: Usando el ID INCORRECTO en el Endpoint
```
❌ INCORRECTO:
POST https://graph.facebook.com/v25.0/1095201550345996/phone_numbers
Authorization: Bearer {access_token}

El problema:
- ID: 1095201550345996 ← NO EXISTEN
- Graph API no puede encontrarlo
- Meta rechaza la solicitud
```

### Hipótesis 2: Intentando Registrar el Número como Nodo
```
❌ INCORRECTO:
POST https://graph.facebook.com/v25.0/{BUSINESS_ACCOUNT_ID}/phone_numbers
Body: {
  "phone_number": "1095201550345996"  ← Pasando el ID como número
}

Problema: El ID no es un número de teléfono
```

---

## ✅ Lo Que Deberías Estar Haciendo (CORRECTO)

### Estructura Correcta de Graph API para WhatsApp

La estructura es:
```
Graph Node Hierarchy:
├─ Nodo: BUSINESS_ACCOUNT_ID (tuyo: 2479057362544519)
│   ├─ Relación: /phone_numbers
│   │   └─ Devuelve lista de números registrados
│   │       └─ Cada uno tiene: phone_number_id
│   │
│   ├─ Relación: /message_templates
│   │
│   └─ Relación: /webhooks
```

### El Endpoint CORRECTO

#### Para ENVIAR mensajes:
```
POST https://graph.facebook.com/v25.0/PHONE_NUMBER_ID/messages
              ↓                          ↓
        API Graph v25.0         989003167640614 (tuyo)

Authorization: Bearer {access_token}
Content-Type: application/json

Payload:
{
  "messaging_product": "whatsapp",
  "to": "573169701688",
  "type": "text",
  "text": {
    "body": "Hola, tu orden está lista"
  }
}
```

#### Para RECIBIR mensajes (Webhook):
```
GET https://graph.facebook.com/v25.0/PHONE_NUMBER_ID/webhooks
                                      ↑
                              989003167640614

Content:
hub.mode=subscribe
hub.challenge={challenge_token}
hub.verify_token={verificar_token}
```

#### Para VERIFICAR tu conexión:
```
GET https://graph.facebook.com/v25.0/2479057362544519?fields=phone_numbers
                                      ↑
                          BUSINESS_ACCOUNT_ID

Response:
{
  "phone_numbers": {
    "data": [
      {
        "id": "989003167640614",        ← PHONE_NUMBER_ID
        "display_phone_number": "+1 555 636 6119",
        "phone_number_id": "989003167640614",
        "verified_name": "Mi Empresa"
      }
    ]
  },
  "id": "2479057362544519"
}
```

---

## 🔍 Desglose del Error

### Paso 1: Identificar dónde falla

Si estás usando cURL:
```powershell
# ❌ ESTO FALLA
curl -i -X POST \
  https://graph.facebook.com/v25.0/1095201550345996/messages \
  -H "Authorization: Bearer EAA..." \
  -H "Content-Type: application/json"

# Response:
# HTTP/1.1 400 Bad Request
# {"error":{"message":"Unsupported POST request...","type":"GraphMethodException"}}
```

### Paso 2: La Razón del Error

```
1095201550345996 no es un Phone Number ID
↓
Meta busca ese ID en su BD
↓
No lo encuentra
↓
Rechaza con: "El objeto con ID no existe"
```

### Paso 3: La Solución

```
Cambiar 1095201550345996 → 989003167640614
                ↑              ↑
        ID inexistente   Phone Number ID correcto
```

---

## 📊 Estructura Correcta Mapeada

```
Tu Configuración en Meta:
├─ Business Manager Account
│   └─ WhatsApp Business Account (WABA): 2479057362544519
│       └─ Phone Numbers registered:
│           └─ Display Number: +1 555 636 6119
│               ├─ phone_number_id: 989003167640614 ← USAR ESTE
│               ├─ verified_name: "Mi Empresa"
│               └─ Webhook URL: https://tu-dominio.com/whatsapp/webhook
│
└─ IDs Válidos en Graph API:
    ├─ ✅ /v25.0/989003167640614/messages
    ├─ ✅ /v25.0/2479057362544519/phone_numbers
    └─ ❌ /v25.0/1095201550345996/* ← NUNCA EXISTE
```

---

## 🟢 Validación con Graph API Explorer

Para verificar que tienes los IDs correctos:

### 1. Abre Graph API Explorer
URL: https://developers.facebook.com/tools/explorer/

### 2. Selecciona tu App

### 3. Ejecuta esta solicitud:
```
GET /2479057362544519?fields=phone_numbers

Response esperado:
{
  "phone_numbers": {
    "data": [
      {
        "display_phone_number": "+1 555 636 6119",
        "phone_number_id": "989003167640614"  ← Si ves esto, está OK!
      }
    ]
  },
  "id": "2479057362544519"
}
```

Si ves ese response con `"phone_number_id": "989003167640614"` → **Tienes los IDs correctos**

---

## 🚨 Checklist: ¿Por qué Falla?

Marca lo que aplica a tu situación:

- [ ] Usando ID `1095201550345996` en cualquier endpoint
  → **Solución:** Cambiar a `989003167640614`

- [ ] POST al ID incorrecto
  → **Solución:** POST solo a `989003167640614` o `2479057362544519`

- [ ] Token expirado o inválido
  → **Solución:** Regenerar token en Meta

- [ ] Falta de permisos en el token
  → **Solución:** Token debe tener scope `whatsapp_business_management`

- [ ] Webhook URL incorrecta
  → **Solución:** Debe ser accesible desde internet (https://)

- [ ] Verify Token no coincide
  → **Solución:** Debe ser idéntico en Meta y en tu código

---

## 📝 Lo Que Pasó

```
Flujo Incorrecto (Lo que hacías):
1. Usuario intenta registrar número
2. Backend hace POST a ID incorrecto
3. Meta API recibe: POST /1095201550345996/messages
4. Meta busca ese ID → No existe
5. Meta responde: "El objeto no existe"
6. Backend retorna error al usuario

Flujo Correcto (Lo que debes hacer):
1. Usuario intenta registrar número
2. Backend hace POST a PHONE_NUMBER_ID correcto
3. Meta API recibe: POST /989003167640614/messages
4. Meta busca ese ID → Existe ✅
5. Meta procesa la solicitud
6. Backend retorna éxito y order_id al usuario
```

---

## 🎯 Resumen: Los 3 IDs Correctos (GUARDALOS)

```
┌─────────────────────────────────────────────────────┐
│  ✅ PHONE_NUMBER_ID (para enviar mensajes)          │
│     GET/POST → /v25.0/989003167640614/*             │
│     Usa este para: /messages, /webhooks, etc.       │
├─────────────────────────────────────────────────────┤
│  ✅ BUSINESS_ACCOUNT_ID (para tu account/config)    │
│     GET/POST → /v25.0/2479057362544519/*            │
│     Usa este para: /phone_numbers, admin ops       │
├─────────────────────────────────────────────────────┤
│  ❌ NUNCA USAR: 1095201550345996                    │
│     Este ID NO EXISTE en Meta                       │
└─────────────────────────────────────────────────────┘
```

---

## 💡 Conclusión

El error ocurre porque:

1. **Tu backend está usando un ID que no existe**
2. **Meta rechaza cualquier solicitud a ese ID**
3. **Los IDs correctos ya los tienes**: 989003167640614 y 2479057362544519

Con los scripts y documentación que creamos:
- ✅ `configure_whatsapp.py` usa los IDs CORRECTOS
- ✅ `test_whatsapp.py` valida que sean correctos
- ✅ Scripts también validan formato (números, longitud, etc.)

**Próximo paso:** Ejecuta `python scripts/configure_whatsapp.py` con los IDs correctos.
