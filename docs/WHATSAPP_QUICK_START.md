# ⚡ GUÍA RÁPIDA - CONFIGURAR WHATSAPP EN 5 MINUTOS

## 🆘 El Error que Recibiste

```
❌ ERROR:
"Solicitud de publicación no compatible. El objeto con ID '1095201550345996' 
no existe, no se puede cargar debido a la falta de permisos..."
```

## ✅ La Solución

**Usas el ID INCORRECTO.** Aquí están los IDs CORRECTOS:

### IDs que DEBES usar:

```
✅ Phone Number ID:      989003167640614
✅ Business Account ID:  2479057362544519
✅ Access Token:         EAAMGYyYgJogBRdcJDJvGchUBoej5m... (el tuyo)

❌ NUNCA USAR:           1095201550345996 ← Este es el problema
```

---

## 🚀 5 Pasos para Configurar

### Paso 1️⃣ - Verifica IDs en Meta
**URL:** https://developers.facebook.com/apps → Tu App → WhatsApp → API Setup

Busca en "Seleccionar números de teléfono":
- Copia: **Identificador de número de teléfono** = `989003167640614`
- Copia: **Identificador de la cuenta** = `2479057362544519`

⏱️ **1 minuto**

---

### Paso 2️⃣ - Registra en tu BD
```powershell
python scripts/configure_whatsapp.py
```

El script te preguntará interactivamente por:
- Número de teléfono: `+1 555 636 6119`
- Phone Number ID: `989003167640614` ← CORRECTO
- Business Account ID: `2479057362544519` ← CORRECTO
- Access Token: Tu token (pégalo)
- Verify Token: `my_secret_verify_token_2024` (puede ser cualquier string)

⏱️ **2 minutos**

---

### Paso 3️⃣ - Configura Webhook en Meta
**URL:** https://developers.facebook.com/apps → Tu App → WhatsApp → Configuration

#### Para Desarrollo (Local con ngrok):
1. Abre terminal nueva:
   ```powershell
   ngrok http 8000
   ```
   Resultado: `https://abc123def456.ngrok.io`

2. En Meta → Configuration → Webhook Configuration:
   - **Webhook URL**: `https://abc123def456.ngrok.io/whatsapp/webhook`
   - **Verify Token**: `my_secret_verify_token_2024` (MISMO del Paso 2)

#### Para Producción:
   - **Webhook URL**: `https://tu-dominio.com/whatsapp/webhook`
   - **Verify Token**: `my_secret_verify_token_2024` (MISMO del Paso 2)

3. En "Eventos de Webhook": Marca `messages` y `message_status`

4. Click: **Guardar**

⏱️ **1 minuto**

---

### Paso 4️⃣ - Prueba que Funcione
```powershell
python scripts/test_whatsapp.py
```

Debería mostrar: ✅ Todos los tests pasaron

Si algo falla, lee el mensaje de error y verifica el paso anterior.

⏱️ **1 minuto**

---

### Paso 5️⃣ - Envía Mensaje de Prueba
En Meta → WhatsApp → API Setup → "Enviar y recibir mensajes":
1. Click en **"Enviar mensaje de prueba"**
2. Ingresa tu número: `+57 3169701688` (o el que tengas)
3. Click: **Enviar**

**Lo que debería pasar:**
- ✅ Recibes el mensaje en tu WhatsApp
- ✅ Tu backend recibe POST en `/whatsapp/webhook`
- ✅ El agente genera una respuesta
- ✅ Recibes la respuesta automática en WhatsApp 🎉

⏱️ **1 minuto**

---

## ⚠️ Checklist de Validación

Antes de confirmar que funciona, verifica:

- [ ] **Backend corriendo:** `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- [ ] **Phone Number ID es**: `989003167640614` (números, > 10 caracteres)
- [ ] **Business Account ID es**: `2479057362544519` (números, > 10 caracteres)
- [ ] **Access Token**: Comienza con `EAA` y tiene > 100 caracteres
- [ ] **Verify Token**: El MISMO en Meta Y en tu BD
- [ ] **Webhook URL**: Sin typos, accesible desde internet
- [ ] **Events**: `messages` y `message_status` marcados en Meta
- [ ] **Script configure_whatsapp.py**: Ejecutado sin errores
- [ ] **Script test_whatsapp.py**: Mostró "✅ Todos los tests pasaron"

---

## 🔧 Troubleshooting Rápido

### ❌ "Error 404 - Webhook not found"
→ La URL en Meta es incorrecta o el backend no está corriendo

### ❌ "Webhook verification failed"
→ El `verify_token` en Meta no coincide con el de tu BD

### ❌ "No recibo mensajes"
→ Verifica que Meta esté enviando a la URL correcta (prueba con curl)

### ❌ Script falla al conectar
→ Verifica que tu backend esté corriendo: `http://localhost:8000/health`

### ❌ Uso ID incorrecto nuevamente
→ Copia-pega directamente:
```
Phone Number ID:      989003167640614
Business Account ID:  2479057362544519
```

---

## 📱 Flujo Final (Una Vez Funcionando)

```
1. Cliente escribe mensaje en WhatsApp
   ↓
2. Meta lo envía a tu webhook: /whatsapp/webhook
   ↓
3. Tu backend recibe el mensaje
   ↓
4. Extrae el phone_number_id: 989003167640614
   ↓
5. Busca tu empresa en la BD
   ↓
6. Llama al agente
   ↓
7. El agente genera respuesta
   ↓
8. Tu backend envía respuesta a Meta
   ↓
9. Cliente recibe respuesta en WhatsApp ✅
```

---

## 📞 Recursos

- 📚 Documentación completa: `/docs/WHATSAPP_SETUP_GUIDE.md`
- 🧪 Script de prueba: `scripts/test_whatsapp.py`
- ⚙️ Script de configuración: `scripts/configure_whatsapp.py`
- 📋 API completa: `/RESUMEN_FINAL_COMPLETO.md`

---

## 💡 Pro Tips

1. **Guarda el verify_token** en tus notas - lo necesitarás si reconfiguran
2. **Ngrok cambia de URL** cada vez que se desconecta - reinicialo con la nueva URL en Meta
3. **Los tokens de acceso expiran** - Meta te dirá cuando 
4. **Para números reales**: En Meta → Administrador de WhatsApp → Agrega y verifica tu número
5. **Respuestas lentas**: Si el agente tarda, Meta reintentará hasta 30 segundos

---

## ✅ ¡Listo!

Una vez funcione, tu agente responderá automáticamente a TODOS los mensajes que lleguen a tu número de WhatsApp.

¿Ya lo tienes funcionando? ¡Cuéntame! 🚀
