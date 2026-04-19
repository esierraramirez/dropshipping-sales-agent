# ✅ VALIDACIÓN DE DATOS WHATSAPP - GUÍA PARA ADMINISTRADOR

**Objetivo**: Saber exactamente qué verificar cuando una empresa ingresa sus credenciales  
**Para**: Admin de plataforma / Soporte  
**Fecha**: 19 de Abril 2026

---

## 🔍 VALIDACIÓN DE 5 CAMPOS

### Campo 1: 📱 Número de Teléfono

**Lo que esperas recibir:**
```
+57 1 2345 6789
+52 1 55 1234 5678
+34 91 123 4567
+1 (555) 123-4567
```

**Validación:**
```
✅ CORRECTO:
- Comienza con +
- Tiene país (2-3 dígitos después del +)
- Tiene dígitos para el número
- Puede incluir espacios, guiones, paréntesis

❌ INCORRECTO:
- Sin + (ej: 573012345678)
- Solo números sin espacios (confuso)
- Mal formato (001 234)
```

**Qué hacer:**
- [x] Es opcional, si la empresa no quiere copiar, OK
- [x] Si lo ingresa, verificar que sea un número real de teléfono
- [x] No es crítico para el funcionamiento

**Acción**: ✅ Solicitar confirmación
- "¿Es este el número de WhatsApp donde recibirán mensajes de clientes?"

---

### Campo 2: 🔑 Phone Number ID (CRÍTICO)

**Lo que esperas recibir:**
```
1234567890123456
9876543210
123456789012

(Típicamente 10-16 dígitos, SOLO números)
```

**Validación:**
```
✅ CORRECTO:
- Solo dígitos
- 10-16 caracteres
- Copiado directamente de Meta

❌ INCORRECTO:
- Contiene letras (1a2b3c)
- Con espacios (1234 5678 9000)
- Con guiones (1234-5678-9000)
```

**Cómo verificar que sea válido:**
```
1. Pedirle a empresa capturazo (screenshot) de Meta
2. Ver en screenshot:
   - Column "Phone Number ID"
   - Sin espacios, sin caracteres especiales
3. Comprobación: Si es válido, más tarde recibirá webhooks

4. Test técnico: Si el ID es falso, webhooks fallarán con 404
```

**Errores comunes:**
```
Empresa envía:    │ Problema              │ Solución
──────────────────┼───────────────────────┼──────────────
"1234 5678 9000"  │ Tiene espacios        │ Quitar espacios
"PHONE_1234567890"│ Tiene prefijo         │ Solo números
"123"             │ Muy corto             │ Pedir que copie bien
"1234567890-01"   │ Con guión             │ Quitar caracteres
```

**Acción": ✅ REQUERIDO - No dejar pasar sin validar

---

### Campo 3: 💼 Business Account ID

**Lo que esperas recibir:**
```
0123456789
987654321098765
12345678901234
```

**Validación:**
```
✅ CORRECTO:
- Solo dígitos
- 9-15 caracteres típicamente
- Copiado de Meta Business Settings

❌ INCORRECTO:
- Con letras
- Con caracteres especiales
```

**Qué hacer:**
- [x] Es OPCIONAL
- [x] Si lo dejan vacío, no hay problema
- [x] Si lo ingresa, validar que sean dígitos
- [x] No es crítico

**Acción**: ✅ Solicitar pero aceptar vacío

---

### Campo 4: 🔐 Access Token (MUY CRÍTICO)

**Lo que esperas recibir:**
```
EAABC987XYZ123...ABC123XYZ987...ABC123XYZ987 (cadena muy larga)

Ejemplo real completo (truncado):
EAABC981234567890ABCXYZ...YXVgkhKDL...jK10LmN2OpQ3sT4uV5w...
```

**Validación:**
```
✅ CORRECTO:
- Comienza con "EAAB" o "EAA"
- Muy largo (típicamente 100-500+ caracteres)
- Solo caracteres alfanuméricos
- Sin espacios

❌ INCORRECTO:
- No empieza con EAA (ej: "1234567890")
- Muy corto (< 50 caracteres)
- Tiene espacios adentro
- Tiene caracteres especiales (!@#$)
- Comienza con "Bearer" (eso va en header, no aquí)
```

**Cómo verificar que sea válido:**
```
Opción 1: Patrón
- Si comienza con "EAAB" y tiene >100 caracteres: ✅ Probablemente válido

Opción 2: Test en backend
- Guardar en BD
- Hacer test request a Meta API
- Si Meta responde 200: ✅ Token válido
- Si Meta responde 401: ❌ Token inválido/expirado

Opción 3: Usuario confirma
- "¿Copiaste el token desde Meta Developers? ✓"
- "¿Empieza con EAAB? ✓"
- "¿Tiene más de 100 caracteres? ✓"
```

**Errores comunes:**
```
Empresa envía:           │ Problema
─────────────────────────┼─────────────────────────
"Bearer EAAB123..."      │ Incluye palabra "Bearer"
"EAAB123" (muy corto)    │ Incompleto
"1234567890"             │ No es token (es contraseña)
"access_token=EAAB..."   │ Incluye atribución
"abc123xyz"              │ No comienza con EAA
```

**Acción**: ✅ REQUERIDO - Validar estrictamente

---

### Campo 5: 🔓 Webhook Verify Token

**Lo que esperas recibir:**
```
mi_token_secreto_2024
MiTienda_2024_Token
secreto123abc
tienda_abc_123_xyz
```

**Validación:**
```
✅ CORRECTO:
- Alfanumérico (números, letras, guiones, guiones bajos)
- 6-50 caracteres típicamente
- Lo inventó la empresa (NO vino de Meta)
- Sin espacios

❌ INCORRECTO:
- Muy corto (< 6 caracteres)
- Espacios adentro
- Caracteres especiales (!@#$%^&*)
- "password" o "123456" (muy obvio)
```

**Cómo verificar que sea válido:**
```
Opción 1: Inspección
- ¿Tiene sentido? (no es default)
- ¿Es único? (empresa lo creó)
- ¿Empresa lo recuerda? (lo necesitará en Meta)

Opción 2: Test técnico
- Guardarlo en BD
- Luego cuando Meta envíe webhook, validar que el token coincida
- Si coincide: ✅ Correctamente configurado

Opción 3: Pedir confirmación
- "¿Este es un token que inventaste y solo tú conoces?"
- "¿Lo escribiste en un lugar seguro?"
```

**Errores comunes:**
```
Empresa envía:     │ Problema
───────────────────┼──────────────────
"123"              │ Muy corto
"password"         │ Muy obvio
"mi token"         │ Tiene espacio
"123@456"          │ Caracteres especiales
(vacío)            │ Requerido
```

**Acción**: ✅ REQUERIDO - Validar que sea string válido

---

## 📊 TABLA DE VALIDACIÓN RÁPIDA

| Campo | Required | Primero? | Rango | Validation | Action |
|-------|----------|----------|-------|------------|--------|
| **Phone Number** | ❌ | No | Cualquier formato | Formato inteligente | ✅ Aceptar |
| **Phone Number ID** | ✅ | 1° | `\d{10,16}` | Solo dígitos | ⚠️ Rechazar si inválido |
| **Business Account ID** | ❌ | - | `\d{9,15}` | Solo dígitos | ✅ Aceptar o vacío |
| **Access Token** | ✅ | 2° | EAA + >100 chars | Patrón + longitud | ⚠️ Rechazar si inválido |
| **Webhook Token** | ✅ | 3° | 6-50 alphanumeric | Sin espacios/especiales | ⚠️ Rechazar si inválido |

---

## 🚨 SEÑALES DE ALERTA

Si empresa proporciona:

```
🚨 ALERTA EXTREMA - No procesar:
- "Token de alguien más"
- "Datos que encontré en internet"
- "Datos de versión anterior"
- "Mi contraseña de Facebook"

🚨 ALERTA CRÍTICA - Verificar múltiples veces:
- "No sé de dónde copiar esto"
- "Lo inventé completamente"
- "No lo puedo reproducir"

⚠️ ALERTA BAJA - Seguidor adelante (pero advertir):
- "Token muy corto"
- "Formato extraño pero funcionó antes"
- "Mi colega me lo pasó"
```

---

## ✅ FLUJO DE VALIDACIÓN (PASO A PASO)

```
1️⃣ USUARIO INGRESA 5 CAMPOS EN FORMULARIO
   ├─ Phone Number
   ├─ Phone Number ID
   ├─ Business Account ID
   ├─ Access Token
   └─ Webhook Token

2️⃣ FRONTEND VALIDA (antes de enviar)
   ├─ ✅ Phone Number ID: solo dígitos ✓
   ├─ ✅ Access Token: comienza EAA ✓
   ├─ ✅ Webhook Token: 6+ caracteres ✓
   └─ Si algo falla: mostrar error en UI

3️⃣ FRONTEND ENVÍA A BACKEND (PUT /whatsapp/me)

4️⃣ BACKEND VALIDA (en servidor)
   ├─ ✅ Phone Number ID: longitud correcta
   ├─ ✅ Access Token: >100 caracteres
   ├─ ✅ Webhook Token: válido
   └─ Si algo falla: retornar 422 (validation error)

5️⃣ BACKEND GUARDA EN BD
   ├─ Crear o actualizar WhatsAppConnection
   ├─ Guardar todos los campos
   └─ Marcar is_connected = true

6️⃣ RESPUESTA TOP FRONTEND
   ├─ ✅ Mensaje: "Conexión guardada exitosamente"
   ├─ Estados: Loading → Success
   └─ Botón: "Guardar" → "Desconectar"

7️⃣ PRUEBA REAL (si quieres validar 100%)
   ├─ Cliente envía mensaje a WhatsApp de empresa
   ├─ Meta envía webhook a tu servidor
   ├─ Backend procesa con Access Token
   └─ Si funciona: ✅ Tokens correctos
   └─ Si falla: ❌ Revisar tokens
```

---

## 🔧 VALIDACIÓN TÉCNICA EN BACKEND (Pseudocódigo)

```python
def validate_whatsapp_credentials(data):
    # 1. Phone Number ID
    if not data.phone_number_id or not data.phone_number_id.isdigit():
        raise ValidationError("Phone Number ID debe ser solo números")
    if len(data.phone_number_id) < 10:
        raise ValidationError("Phone Number ID muy corto")
    
    # 2. Access Token  
    if not data.access_token or not data.access_token.startswith("EAAB"):
        if not data.access_token.startswith("EAA"):
            raise ValidationError("Access Token debe comenzar con EAA")
    if len(data.access_token) < 100:
        raise ValidationError("Access Token muy corto o incompleto")
    
    # 3. Webhook Token
    if not data.verify_token or len(data.verify_token) < 6:
        raise ValidationError("Webhook Token: mínimo 6 caracteres")
    if not all(c.isalnum() or c in "-_" for c in data.verify_token):
        raise ValidationError("Webhook Token: solo alfanumérico, guiones y guiones bajos")
    
    # 4. Business Account ID (opcional pero si viene, validar)
    if data.business_account_id:
        if not data.business_account_id.isdigit():
            raise ValidationError("Business Account ID debe ser solo números")
    
    return ✅ Valid
```

---

## 📞 PREGUNTAS A HACER A EMPRESA

Si te dice que algo no funciona:

```
1. "¿El Access Token comienza con EAAB?" 
   → Si NO: Pedir que lo copie nuevamente de Meta

2. "¿El Phone Number ID contiene SOLO números?"
   → Si NO: Pedir que lo copie nuevamente sin espacios

3. "¿Tu Webhook Verify Token es el que TÚ creaste?"
   → Si NO: Verificar si lo ingresó correctamente en Meta

4. "¿Tu número de WhatsApp está verificado en Meta?"
   → Si NO: Pedir que verifique primero en Meta

5. "¿El Access Token es reciente (generado esta semana)?"
   → Si NO: Pedir que genere uno nuevo en Meta
```

---

## 🎯 SITUACIONES REALES

### Situación 1: "No funciona"
```
Pasos para diagnosticar:
1. ✅ Verificar que datos se guardaron en BD
   SELECT * FROM whatsapp_connections WHERE vendor_id = X;

2. ✅ Verificar que webhook token se guardó
   SELECT verify_token FROM whatsapp_connections WHERE vendor_id = X;

3. ✅ Pedir que envíe mensaje de prueba
   - Cliente envía mensaje al WhatsApp de empresa
   - Ver logs de backend si webhook llega

4. ✅ Si webhook no llega:
   - Verificar que webhook está configurado en Meta
   - Usar verify token correcto en Meta

5. ✅ Si llega pero falla:
   - Verificar Access Token válido
   - Revisar logs de backend
```

### Situación 2: "Antes funcionaba, ahora no"
```
Causas probables:
1. ❌ Access Token expiró
   → Solución: Generar nuevo en Meta

2. ❌ Cambió el número de WhatsApp
   → Solución: Actualizar Phone Number ID

3. ❌ Meta cambió la configuración
   → Solución: Revisar documentación Meta

4. ❌ Webhook se desconfiguró
   → Solución: Reconfiguren webhook en Meta
```

### Situación 3: "Veo el error 'Unauthorized'"
```
Significa: Access Token inválido o expirado

Solución rápida:
1. Meta for Developers → App → WhatsApp
2. Generate Access Token nuevamente
3. Copiar nuevo token
4. Actualizar en nuestra plataforma
5. Listo
```

---

## 📋 CHECKLIST ADMIN ANTES DE APROBAR

- [ ] Phone Number ID: solo dígitos ✓
- [ ] Access Token: comienza con EAA ✓
- [ ] Access Token: >100 caracteres ✓
- [ ] Webhook Token: 6-50 caracteres ✓
- [ ] Webhook Token: sin espacios ✓
- [ ] Empresa confirma todos los datos ✓
- [ ] Datos en BD guardados correctamente ✓
- [ ] Estado muestra "Conectado" en UI ✓

**Si todo está checked**: ✅ LISTO

---

## 🚀 VALIDACIÓN FINAL

```
ANTES DE USAR EN PRODUCCIÓN:
1. ✅ Empresa prueba 1: Enviar mensaje de prueba
2. ✅ Empresa prueba 2: Verificar que no mezclan datos
3. ✅ Load test: 10 mensajes simultáneos por empresa
4. ✅ Error test: Invalidar token e intenta enviar (debe fallar correctamente)
```

---

**Guía de Validación Completa ✅**  
**Listo para Usar en Soporte** 🎯
