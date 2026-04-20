# ⚡ GUÍA ULTRA RÁPIDA - Registrar Número en WhatsApp Business (10 minutos)

## 🎯 Objetivo
Tu número de WhatsApp (+57 316 9701688) reciba y responda automáticamente mediante tu agente IA

---

## 5 PASOS CRÍTICOS

### ✅ PASO 1: Acceder a Facebook Business (2 min)

```
https://business.facebook.com
└─ Inicia sesión con tu cuenta Meta/Facebook
└─ Verás el dashboard
```

---

### ✅ PASO 2: Ir a Administrador de WhatsApp (1 min)

```
Dashboard → Menú izquierdo → Herramientas (Tools)
               ↓
        Buscar: "Administrador de WhatsApp"
        (o "WhatsApp Manager")
```

**Verás algo como:**
```
┌────────────────────────────────────┐
│ ADMINISTRADOR DE WHATSAPP          │
├────────────────────────────────────┤
│ Números registrados:                │
│ • +1 555 636 6119                   │
│   ID: 989003167640614 ← COPIA ESTO  │
│                                    │
│ • +57 316 9701688 (TU NÚMERO)       │
│   ID: ???? ← O este si lo ves      │
└────────────────────────────────────┘
```

---

### ✅ PASO 3: Registrar tu Número (+57 316 9701688)

**Si VES tu número en la lista:**
→ Copia el `ID` que aparece al lado
→ Ve al PASO 5

**Si NO VES tu número:**

1. Click: **"Agregar número"** o **"Add Phone Number"**
2. Selecciona: **Colombia (+57)**
3. Ingresa: **316 9701688** (sin +57, sin espacios)
4. Click: **Verificar** o **Verify**
5. Meta envía código por SMS/llamada
6. Ingresa el código
7. ✅ Número registrado

**Resultado:** Recibirás un `ID` nuevo
```
phone_number_id = [Un número que Meta genera]
```

---

### ✅ PASO 4: Copiar tus Credenciales (2 min)

En el **Administrador de WhatsApp**, busca la sección **"Configuración de API"** o **"API Credentials"**

**COPIA ESTOS 3 NÚMEROS:**

```
┌─────────────────────────────────┐
│ COPIA ESTOS IDS:                │
├─────────────────────────────────┤
│ 1️⃣ Phone Number ID              │
│    989003167640614              │
│        (o el tuyo si es distinto)│
│                                 │
│ 2️⃣ Business Account ID          │
│    2479057362544519             │
│                                 │
│ 3️⃣ Access Token                 │
│    EAAMGYyYgJogBR...            │
│    (El token largo)             │
└─────────────────────────────────┘
```

---

### ✅ PASO 5: Ejecutar Script de Configuración (3 min)

En tu PC, abre PowerShell en la carpeta del proyecto:

```powershell
# Asegúrate que el backend está CORRIENDO primero:
# cd .\backed
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# En OTRA terminal, ejecuta:
python scripts/configure_whatsapp.py

# Te pedirá:
# 1. Número: +57 316 9701688
# 2. Phone Number ID: [Pega lo que copiaste]
# 3. Business Account: 2479057362544519
# 4. Access Token: [Pega lo que copiaste]
# 5. Verify Token: escribe algo como: mi_token_secreto_2024

# El script guarda todo en la BD automáticamente
```

---

## 🧪 VERIFICAR QUE FUNCIONA

```powershell
# En otra terminal:
python scripts/test_whatsapp.py

# Debería mostrar:
# ✅ Backend is running
# ✅ Webhook verification works
# ✅ Incoming message simulation works
# ALL TESTS PASSED! 🎉
```

---

## 📱 CONFIGURAR EN FACEBOOK DEVELOPERS (Último Paso)

1. Ve a: https://developers.facebook.com/apps
2. Selecciona tu App
3. **WhatsApp** → **Configuration**
4. **Webhook Configuration**:
   - **URL**: `https://tu-dominio.com/whatsapp/webhook`
     - Si estás en local: https://abc123.ngrok.io/whatsapp/webhook
   - **Verify Token**: `mi_token_secreto_2024` (el que escogiste)
5. **Subscribe to**: marca `messages` y `message_status`
6. Click: **SAVE**

---

## ✅ ¿YA FUNCIONA?

**Prueba enviando un mensaje:**

1. Abre WhatsApp
2. Escribe a: **+57 316 9701688** (o el número que registraste)
3. Escribe algo como: "Hola, quiero comprar"
4. **ESPERA 2-3 SEGUNDOS**
5. ✅ Deberías recibir respuesta de tu agente IA automáticamente

---

## 🆘 ERROR: "ID no existe"

```
Significa: Estás usando el ID INCORRECTO

❌ NO USAR: 1095201550345996
✅ USAR: 989003167640614 (o el tuyo)
```

**Solución:**
1. Vuelve a Facebook Business
2. Copia el `phone_number_id` EXACTO
3. Ejecuta `configure_whatsapp.py` de nuevo
4. Ingresa el ID correcto

---

## 🆘 ERROR: "Webhook verification failed"

```
Significa: El Verify Token no coincide

El token que escribiste en configure_whatsapp.py 
debe ser IGUAL al que pusiste en Facebook Developers
```

**Solución:**
1. Apunta el token que usaste: ej. `mi_token_secreto_2024`
2. En Facebook Developers → WhatsApp → Configuration
3. Ingresa el MISMO token
4. Click: SAVE

---

## 🆘 ERROR: "Cannot reach webhook URL"

```
Significa: Tu URL no es accesible desde internet
```

**Solución (para testing):**
1. Descarga ngrok: https://ngrok.com/download
2. Abre terminal:
   ```
   ngrok http 8000
   ```
3. Copias la URL que aparece: `https://abc123def456.ngrok.io`
4. La usas en Facebook Developers:
   ```
   Webhook URL: https://abc123def456.ngrok.io/whatsapp/webhook
   ```

---

## 📋 CHECKLIST - Antes de Probar

- [ ] Backend corriendo en puerto 8000
- [ ] El numero aparece en Facebook Business (registrado)
- [ ] Tengo el Phone Number ID copiado
- [ ] Tengo el Access Token copiado
- [ ] Ejecuté `configure_whatsapp.py` sin errores
- [ ] `test_whatsapp.py` pasa todos los tests
- [ ] Webhook URL configurada en Facebook Developers
- [ ] Verify Token coincide en ambos lados

---

## 🎉 RESULTADO FINAL

Cuando todo funcione:

```
ANTES:
- Escribes a WhatsApp
- Nada pasa ❌

DESPUÉS:
- Escribes a WhatsApp
- Tu agente IA responde automáticamente ✅
```

---

## ⏱️ Tiempo Total
- Pasos 1-5 en Facebook: **8 minutos**
- Ejecutar scripts: **2 minutos**
- TOTAL: **10 minutos**

¡Ya está! 🚀
