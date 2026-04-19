# 💬 HELP MODAL - INFORMACIÓN PARA FORMULARIO WHATSAPP

**Propósito**: Popup/Modal que aparece al hacer click en "?" o "Ayuda" en cada campo  
**Para**: Empresas rellenando el formulario  
**Ubicación**: `http://localhost:5173/whatsapp` → Click en "?" de cada campo

---

## 📱 Campo 1: Número de Teléfono

### Texto Breve (Mostrar siempre)
```
Número WhatsApp donde recibirás mensajes de clientes
(opcional - solo para referencia)
```

### Modal Completo (Al hacer click "?")
```
═══════════════════════════════════════════════════════════
📱 NÚMERO DE TELÉFONO
═══════════════════════════════════════════════════════════

¿QUÉ ES?
El número de teléfono de tu WhatsApp Business.
Es el número donde recibirás mensajes de tus clientes.

¿DÓNDE LO ENCUENTRO?
Lo conoces - es tu número de WhatsApp.

EJEMPLOS VÁLIDOS:
✓ +57 1 (55) 2345-6789
✓ +52 1 55 1234 5678  
✓ +34 91 123 4567
✓ +5712345678 (sin espacios también funciona)

¿ES REQUERIDO?
No, es opcional. Si no lo ingresa, está bien.

⚠️ NOTA
Use el formato con el código de país (+XX)
```

---

## 🔑 Campo 2: Phone Number ID

### Texto Breve (Mostrar siempre)
```
ID único del número en Meta (REQUERIDO)
Este es el identificador de tu número en WhatsApp Business
```

### Modal Completo (Al hacer click "?")
```
═══════════════════════════════════════════════════════════
🔑 PHONE NUMBER ID (Muy Importante)
═══════════════════════════════════════════════════════════

¿QUÉ ES?
El ID único que Meta asigna a tu número WhatsApp Business.
Sin esto, no funciona nada. ⚠️

¿DÓNDE LO ENCUENTRO?
Sigue estos pasos EXACTOS:

PASO 1: Ir a https://business.facebook.com
PASO 2: Click en "Configuración" (esquina superior izquierda)
PASO 3: En el menú, busca "WhatsApp Business Accounts"
        o "Cuentas de WhatsApp para empresas"
PASO 4: Selecciona tu Cuenta WhatsApp
PASO 5: Click en pestaña "Números de teléfono"
PASO 6: Mira la tabla - verás una columna "Phone Number ID"
PASO 7: COPIA ese ID (es una serie de números)

EJEMPLO:
Si ves en la tabla:
├─ Número: +57 1 2345 6789
├─ Estado: Verificado ✓
└─ Phone Number ID: 1234567890123456  ← COPIAR ESTO

¿CUÁNTOS CARACTERES?
Típicamente 10-16 dígitos. Solo números.

¿ES REQUERIDO?
SÍ - Sin esto no puede funcionar.

❌ NO DEBES COPIAR:
- El número de teléfono (+57...)
- El estado (Verificado)
- Solo el ID numérico

💡 CONSEJO:
Si no ves la tabla, verifica que tengas:
1. Una Cuenta WhatsApp Business creada
2. Un número registrado y verificado
3. Acceso con tu cuenta Meta/Facebook
```

---

## 💼 Campo 3: Business Account ID

### Texto Breve (Mostrar siempre)
```
ID de tu cuenta de negocio en Meta (OPCIONAL)
Ayuda a identificar tu negocio
```

### Modal Completo (Al hacer click "?")
```
═══════════════════════════════════════════════════════════
💼 BUSINESS ACCOUNT ID (Opcional)
═══════════════════════════════════════════════════════════

¿QUÉ ES?
El identificador de tu cuenta de negocio en Meta.
No es crítico para que funcione, pero es útil.

¿DÓNDE LO ENCUENTRO?
Una de estas opciones:

OPCIÓN A: (Recomendada)
PASO 1: Ir a https://business.facebook.com
PASO 2: Esquina superior izquierda → Tu nombre
PASO 3: Click en "Configuración del negocio"
PASO 4: En menú izquierdo: "Información del negocio"
PASO 5: Ve el campo "ID de negocio"
PASO 6: COPIA ese número

OPCIÓN B:
Mira la URL de Business Manager:
https://business.facebook.com/123456789/?...
El número después de /business/ es tu ID ← COPIAR

EJEMPLO:
ID de negocio: 0987654321098765

¿CUÁNTOS CARACTERES?
Típicamente 10-15 dígitos.

¿ES REQUERIDO?
No. Déjalo en blanco si no encuentras.

💡 CONSEJO:
Si tienes dudas, déjalo vacío.
Es totalmente opcional.
```

---

## 🔐 Campo 4: Access Token

### Texto Breve (Mostrar siempre)
```
Token de acceso Meta API (REQUERIDO)
Permiso para que la plataforma acceda a tu WhatsApp
```

### Modal Completo (Al hacer click "?")
```
═══════════════════════════════════════════════════════════
🔐 ACCESS TOKEN (Muy Importante)
═══════════════════════════════════════════════════════════

¿QUÉ ES?
Un token especial que permite a nuestra plataforma
acceder a tu WhatsApp Business para enviar/recibir mensajes.

Es como darle permiso a la plataforma de usar tu WhatsApp.

⚠️ IMPORTANTE: No compartir con nadie
Este token es sensible - como una contraseña.

¿DÓNDE LO GENERO?
Sigue estos pasos EXACTOS:

PASO 1: Ir a https://developers.facebook.com
PASO 2: Click en "Mis Apps" (esquina superior derecha)
PASO 3: Si tienes una app WhatsApp existente:
        - Seleccionarla
        Si no:
        - Click "Crear app"
        - Tipo: "Negocio" (Business)
        - Nombre: "Mi Tienda WhatsApp" o similar
PASO 4: Una vez en la app, en sidebar izquierdo:
        Buscar "WhatsApp"
PASO 5: Click en "WhatsApp"
PASO 6: Pestaña "Comenzar" o "Getting Started"
PASO 7: Sección "Generar token de acceso"
PASO 8: Click botón "Generar token de acceso"
        o "Generate Access Token"
PASO 9: Selecciona:
        - Tu Cuenta WhatsApp
        - Permisos: whatsapp_business_messaging
PASO 10: Un token largo aparecerá
        - Ejemplo: EAABC987XYZ...
        - COPIA ese token (toda la cadena)

¿CUÁNTOS CARACTERES?
Muy largo - típicamente 100-500+ caracteres.
Comienza con "EAAB" o "EAA"

¿ES REQUERIDO?
SÍ - Sin esto no funciona.

❌ NO HAGAS:
- No compartir el token
- No subirlo a GitHub
- No compartirlo por email/chat sin encriptar
- No copiar "Bearer" antes del token

✅ ANTES DE PEGAR:
1. Verifica que comienza con "EAA"
2. Verifica que es una cadena muy larga
3. Cópialo sin espacios antes/después
4. Pégalo en el campo

💡 CONSEJO:
Si expiras el token o se corrompe:
- Generar uno nuevo en Meta for Developers
- Actualizar aquí
- Listo
```

---

## 🔓 Campo 5: Webhook Verify Token

### Texto Breve (Mostrar siempre)
```
Código de verificación (REQUERIDO - lo inventas tú)
Contraseña que solo tú conoces para verificar webhooks
```

### Modal Completo (Al hacer click "?")
```
═══════════════════════════════════════════════════════════
🔓 WEBHOOK VERIFY TOKEN (Lo Inventas Tú)
═══════════════════════════════════════════════════════════

¿QUÉ ES?
Un código secreto que TÚ inventes.
Se usa para verificar que la comunicación entre
Meta y nuestra plataforma es segura.

¿DÓNDE LO CONSIGO?
¡LO INVENTAS TÚ! Cualquier texto que quieras.

¿QUÉ CARACTERÍSTICAS DEBE TENER?
✓ Mínimo 6 caracteres
✓ Máximo 50 caracteres (típicamente)
✓ Puedes usar: letras, números, guiones (-), subguiones (_)
✓ No uses: espacio, @, #, !, $, %, etc.
✓ Debe ser único - solo tú lo conoces

¿EJEMPLOS VÁLIDOS?
✓ MiTienda_2024_Token
✓ secreto123abc
✓ tienda_token_abril2024
✓ mi_whatsapp_seed_99
✓ CompanyWhatsApp2024

❌ EJEMPLOS NO VÁLIDOS:
✗ "123" (muy corto)
✗ "password" (muy obvio - evitar defaults)
✗ "mi token" (contiene espacio)
✗ "token@123" (contiene @)
✗ (vacío - requerido)

¿ES REQUERIDO?
SÍ - necesitas uno.

¿DÓNDE LO GUARDO?
Escríbelo en un lugar seguro que recuerdes.
Lo necesitarás después cuando configures Meta.

FLUJO COMPLETO:
1. Inventas: "MiTienda_Token_Secreto"
2. Lo pegas aquí en el formulario
3. Guardas la configuración
4. Luego en Meta (Admin Dashboard):
   - Configuras webhook
   - Meta pregunta por "Verify Token"
   - Pegas el MISMO token: "MiTienda_Token_Secreto"
   - Meta verifica que coincida
   - Si coincide: ✅ Correctamente configurado

⚠️ IMPORTANTE:
Si usas un token aquí, DEBE SER EL MISMO
que uses en Meta. Si no coinciden, no funciona.

💡 GENERADOR RÁPIDO:
Si no se te ocurre uno:
1. Visit: https://randomkeygen.com/
2. Copy el botón "Fort Knox Password"
3. Usa los primeros 20 caracteres
4. Listo

✅ LISTO:
Una vez completes este campo, haz click en
"Guardar y verificar conexión"
```

---

## 🎯 MINI HELP - VERSIÓN ULTRA CORTA

Para mostrar como tooltip (hover):

```
📱 Número Teléfono
"Tu número WhatsApp (opcional)"

🔑 Phone Number ID  
"ID Meta (Copiar de: business.facebook.com → WhatsApp)"

💼 Business Account ID
"ID negocio (opcional)"

🔐 Access Token
"Token Meta (Generar en: developers.facebook.com)"

🔓 Webhook Token
"Código secreto que TÚ inventas (mín 6 caracteres)"
```

---

## 🎨 COMPONENTE REACT - IMPLEMENTACIÓN

```typescript
// HelpModal.tsx
interface HelpModalProps {
  field: "phoneNumber" | "phoneNumberId" | "businessAccountId" | "accessToken" | "webhookToken";
}

export function HelpModal({ field }: HelpModalProps) {
  const helpContent = {
    phoneNumber: {
      title: "📱 Número de Teléfono",
      content: "Número WhatsApp donde recibirás mensajes de clientes (opcional - solo para referencia)",
      details: "Lo conoces - es tu número de WhatsApp Business..."
    },
    phoneNumberId: {
      title: "🔑 Phone Number ID",
      content: "ID único del número en Meta (REQUERIDO)",
      details: "Sigue pasos en Meta Business..."
    },
    // ... más
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm">
          <Info size={16} />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{helpContent[field].title}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <p>{helpContent[field].details}</p>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// En WhatsAppPage.tsx
<div className="flex items-center justify-between">
  <label>Phone Number ID (Requerido)</label>
  <HelpModal field="phoneNumberId" />
</div>
```

---

## 📱 VISTA EN UI

### Versión Desktop
```
┌────────────────────────────────────────┐
│ Configurar WhatsApp Business            │
├────────────────────────────────────────┤
│                                        │
│ Número de Teléfono      [?]           │
│ ┌─────────────────────────┐            │
│ │ +57 1 2345 6789        │            │
│ └─────────────────────────┘            │
│ Ej: +57 1 (55) 1234-5678             │
│                                        │
│ Phone Number ID (Requerido) [?]       │
│ ┌─────────────────────────┐            │
│ │ 1234567890123456       │            │
│ └─────────────────────────┘            │
│ ✓ Requerido               │            │
│                                        │
│ Business Account ID         [?]        │
│ ┌─────────────────────────┐            │
│ │ 0987654321098          │            │
│ └─────────────────────────┘            │
│ ✓ Opcional                             │
│                                        │
│ Access Token (Requerido)    [?]        │
│ ┌─────────────────────────┐            │
│ │ EAABC987...            │            │
│ └─────────────────────────┘            │
│ ✓ Requerido - Token muy largo         │
│                                        │
│ Webhook Token (Requerido)   [?]        │
│ ┌─────────────────────────┐            │
│ │ mi_token_2024          │            │
│ └─────────────────────────┘            │
│ ✓ Requerido - Lo inventas tú          │
│                                        │
│ ┌──────────────────────────┐           │
│ │ 💾 Guardar y Verificar  │           │
│ └──────────────────────────┘           │
└────────────────────────────────────────┘
```

### Al hacer click en [?] - Modal
```
╔════════════════════════════════════════╗
║ 🔑 PHONE NUMBER ID (Muy Importante)   ║
╟────────────────────────────────────────╢
║                                        ║
║ ¿QUÉ ES?                              ║
║ El ID único que Meta asigna a tu      ║
║ número WhatsApp Business.             ║
║                                        ║
║ ¿DÓNDE LO ENCUENTRO?                  ║
║                                        ║
║ PASO 1: Ir a business.facebook.com    ║
║ PASO 2: Click en "Configuración"      ║
║ PASO 3: "WhatsApp Business Accounts"  ║
║ PASO 4: Selecciona tu Cuenta          ║
║ PASO 5: Tab "Números de teléfono"     ║
║ PASO 6: COPIA el "Phone Number ID"    ║
║                                        ║
║ EJEMPLO:                              ║
║ Si ves: 1234567890123456 ← COPIAR    ║
║                                        ║
║ [✓ Entendido - Ir]                    ║
╚════════════════════════════════════════╝
```

---

## 📝 CHECKLIST PARA EMPRESA (Mostrar antes de submit)

```
Antes de hacer click en "Guardar", verifica:

☐ ¿El Phone Number ID contiene SOLO números?
☐ ¿El Access Token comienza con "EAAB" o "EAA"?
☐ ¿El Access Token es muy largo (>100 caracteres)?
☐ ¿El Webhook Token es diferente al Access Token?
☐ ¿Guardé el Webhook Token en un lugar seguro?
☐ ¿Revisé que todos los datos sean correctos?

Si TODO está checked:
→ ✅ Click en "Guardar y verificar conexión"
```

---

## ⏱️ ESTIMADO DE TIEMPO

Para empresa obtener todos los datos:
- Phone Number ID: 3 minutos
- Access Token: 5 minutos
- Webhook Token: 1 minuto
- **TOTAL**: ~9 minutos

**Tiempo en formulario**: 2 minutos (copy-paste)

---

**Ayuda In-App Completa ✅**  
**Lista para integrar en UI** 🎨
