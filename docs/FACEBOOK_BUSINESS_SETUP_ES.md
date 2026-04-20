# 🔧 CORRECCIÓN PASO A PASO - FACEBOOK BUSINESS → WHATSAPP AGENT

## 🚨 El Problema
Estás usando el ID INCORRECTO: `1095201550345996`

**El ID CORRECTO es: `989003167640614`**

---

## ✅ Solución: 3 Pasos en Facebook Business

### Paso 1: Acceder a Facebook Business
1. Ve a: https://business.facebook.com
2. Inicia sesión con tu cuenta
3. Click en el icono de **menú** (arriba izquierda)

---

### Paso 2: Encontrar tu Número de WhatsApp Business
1. En el menú izquierdo → **Herramientas**
2. Busca: **Administrador de WhatsApp** (o "WhatsApp Manager")
3. Click en él

**Verás algo como esto:**
```
┌─────────────────────────────────────────┐
│  Administrador de WhatsApp              │
├─────────────────────────────────────────┤
│  Tu Cuenta de Negocio: XYZ              │
│  ├─ Números de teléfono:                │
│  │  └─ +1 555 636 6119 ← Este es el tuyo │
│  │     ID: 989003167640614 ← COPIA ESTE │
│  │                                      │
│  │  └─ +57 316 9701688 (si existe)      │
│  │     ID: ???????????? ← O copia este   │
│  └─ Webhooks:                           │
│     URL: ...                            │
└─────────────────────────────────────────┘
```

**👉 IMPORTANTE:** El ID que ves al lado del número es el `phone_number_id`

---

### Paso 3: Verificar que tu Número esté Registrado
En el **Administrador de WhatsApp**:

1. **Sección "Números"**:
   - Verifica que veas al menos un número
   - Si NO ves ninguno → debes **agregar tu número**

2. **Para AGREGAR tu número (+57 316 9701688)**:
   - Click en: **"Agregar número de teléfono"** o **"Add phone number"**
   - Selecciona **Colombia** (+57)
   - Ingresa: **316 9701688** (sin +57 ni espacios)
   - Click: **Verificar**
   - Meta te enviará un **código de 6 dígitos** por SMS o llamada
   - Ingresa el código
   - ✅ Número registrado

3. **Una vez registrado**:
   - Verás el `phone_number_id` asignado por Meta
   - Cópialo exactamente como aparece

---

## 🔑 Los IDs Que Necesitas (GUÁRDALOS)

### Opción A: Si usas el número de PRUEBA (+1 555 636 6119)
```
Phone Number ID:      989003167640614
Business Account ID:  2479057362544519
```

### Opción B: Si registras tu número (+57 316 9701688)
```
Phone Number ID:      [Será diferente - cópialo de Facebook Business]
Business Account ID:  2479057362544519  [Este es el mismo]
```

---

## 🔧 Cómo Usar los IDs en tu Backend

### En Facebook Business Dashboard:

1. Ve a: **Configuración** (Settings/Configuration)
2. Busca: **"Credenciales de API de WhatsApp"** o **"WhatsApp API Credentials"**
3. **Copiar:**
   - ✅ **Phone Number ID**: `989003167640614` (o el nuevo si registraste otro)
   - ✅ **Business Account ID**: `2479057362544519`
   - ✅ **Access Token**: El token largo que empieza con `EAA`
   - ✅ **Verify Token**: Cualquier string que tú generes (ej: `my_secret_token_2024`)

---

## ⚡ Ejecutar en tu Backend

Una vez tengas los IDs correctos, en terminal:

```powershell
# Terminal 1: Backend corriendo en puerto 8000
cd .\backed
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Ejecutar configuración
python scripts/configure_whatsapp.py

# El script te pedirá interactivamente:
# 1. Número: +1 555 636 6119 (o tu número +57 316 9701688)
# 2. Phone Number ID: 989003167640614 (o el tuyo si es diferente)
# 3. Business Account: 2479057362544519
# 4. Access Token: Tu token de Meta
# 5. Verify Token: Token secreto que generates
```

---

## ✅ Verificar que Funciona

```powershell
# Terminal 3: Testing
python scripts/test_whatsapp.py

# Resultado esperado:
# ✅ Backend is running
# ✅ Webhook verification works
# ✅ Incoming message simulation works
# ✅ All tests passed!
```

---

## 📱 Configurar Webhook en Facebook Business

Una vez que el backend esté corriendo:

1. Abre: **https://developers.facebook.com/apps**
2. Selecciona tu App
3. Ve a: **WhatsApp** → **Configuration**
4. En **"Webhook Configuration"**:

   | Campo | Valor |
   |-------|-------|
   | **Webhook URL** | `https://tu-dominio.com/whatsapp/webhook` |
   | **Verify Token** | El token que generaste en configure_whatsapp.py |

5. En **"Webhook Fields"**:
   - ✅ Marcar: `messages`
   - ✅ Marcar: `message_status`

6. Click: **Save**

---

## 🟢 ¿Cómo Sé que Funciona?

Cuando todo esté correcto:

1. **En Facebook Business:**
   - ✅ El número aparece como "Activo" o "Verified"
   - ✅ El webhook status dice "Configured"

2. **En tu Backend:**
   - ✅ Puedes ejecutar `test_whatsapp.py` sin errores
   - ✅ Los logs muestran: "Webhook verified successfully"

3. **En WhatsApp:**
   - Envías un mensaje a tu número desde WhatsApp
   - ✅ Tu agente responde automáticamente

---

## 🆘 Si Sigue Fallando

### Error: "ID no existe"
→ Verificar que usas el `phone_number_id` correcto (989003167640614 o el tuyo)
→ NO usar 1095201550345996

### Error: "Verify Token incorrecto"
→ El token en Facebook Business debe ser EXACTO al que usaste en configure_whatsapp.py

### Error: "Webhook URL no accesible"
→ Usar ngrok para exponer localhost: `ngrok http 8000`
→ Usar esa URL en Facebook Business

### Error: "Permission denied"
→ El Access Token necesita estos permisos:
  - whatsapp_business_management
  - whatsapp_business_messaging

---

## 📋 Checklist Final (Antes de Probar)

Verifica en Facebook Business:

- [ ] Al menos un número de WhatsApp registrado
- [ ] `phone_number_id` visible al lado del número
- [ ] `business_account_id` disponible
- [ ] Access Token generado y válido
- [ ] Verify Token anotado
- [ ] Webhook URL configurada
- [ ] Webhook Fields (messages, message_status) marcadas

Verifica en tu Backend:

- [ ] Backend corriendo en puerto 8000
- [ ] Script `configure_whatsapp.py` ejecutado sin errores
- [ ] Conexión guardada en BD
- [ ] Script `test_whatsapp.py` pasando todos los tests

---

## 🚀 Resultado Final

Una vez todo configurado:

```
Cliente escribe a +57 316 9701688 en WhatsApp
         ↓
Meta envía mensaje a tu webhook
         ↓
Tu backend recibe la solicitud
         ↓
Agente genera respuesta IA
         ↓
Respuesta se envía automáticamente a cliente
         ↓
✅ CLIENTE RECIBE RESPUESTA DEL AGENTE
```

---

## 💡 Pro Tips

1. **Para Testing Rápido:** Usa el número de prueba (+1 555 636 6119) primero
2. **Para Producción:** Luego registra tu número real (+57 316 9701688)
3. **No Confundas IDs:** 
   - Phone ID = Para enviar mensajes
   - Business ID = Para administración
   - NO usar: 1095201550345996
4. **Token Válido:** Regenera en Meta si duda

---

## 📞 Links Útiles

- Facebook Business: https://business.facebook.com
- Developer Apps: https://developers.facebook.com/apps
- Graph API Docs: https://developers.facebook.com/docs/graph-api
- WhatsApp API Docs: https://developers.facebook.com/docs/whatsapp

---

## ✨ ¿Necesitas Ayuda?

Si aún tienes error después de esto:

1. Abre: `docs/GRAPH_API_ERROR_ANALYSIS.md` (análisis técnico)
2. Abre: `docs/GRAPH_API_DEBUG_VISUAL.md` (debugging visual)
3. Ejecuta: `python scripts/test_whatsapp.py` (test automático)

¡El agente en WhatsApp te funcionará! 🎉
