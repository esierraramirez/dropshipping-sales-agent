# 🔌 GUÍA DE SETUP WHATSAPP - INFORMACIÓN A SOLICITAR A LA EMPRESA

**Objetivo**: Explicar exactamente qué información pedir a cada empresa y dónde obtenerla  
**Fecha**: 19 de Abril 2026  
**Público**: Administrador de la plataforma & Empresas

---

## 📋 INFORMACIÓN REQUERIDA (en orden)

### Campo 1: 📱 Número de Teléfono (OPCIONAL - informativo)
**Por qué**: Para recordar qué número WhatsApp está configurado  
**Formato**: +57 1 2345 6789 o +573012345678  
**Dónde obtenerlo**: La empresa lo conoce, es su número WhatsApp Business actual

**Ejemplo**:
```
+57 1 (55) 1234-5678
+52 1 55 1234 5678
+34 91 123 4567
```

**✅ Validación para empresa**:
- "¿Este es el número WhatsApp donde recibirás mensajes de clientes?"

---

### Campo 2: 🔑 Phone Number ID (REQUERIDO - lo más importante!)
**Por qué**: Meta ID del número WhatsApp, único para cada número  
**Formato**: Serie de números, típicamente 15-20 dígitos (ej: 1234567890)  
**Dónde obtenerlo**: Meta Business Manager → WhatsApp Business Account → Phone Numbers

#### 🎯 PASOS EXACTOS para la empresa:

```
1. Ir a: https://business.facebook.com/
2. Ingresar con cuenta Meta

3. Button superior izquierda → "Configuración"
   (Puede estar en idioma del navegador)

4. En sidebar izquierdo:
   Buscar: "WhatsApp Business Accounts"
   o "Cuentas de negocio de WhatsApp"

5. Hacer click en tu cuenta WhatsApp

6. En la pestaña "Números de teléfono"
   (o "Phone Numbers")

7. Ver la tabla con tus números registrados

8. COPIAR el "Phone Number ID"
   Ejemplo: 1234567890123456
   (está en la columna "Phone Number ID")

9. Pegar en el campo del formulario
```

**Visual Reference**:
```
Meta Business Manager dashboard:
├─ Configuración (settings icon)
│  └─ WhatsApp Business Accounts
│     └─ [Tu Cuenta WhatsApp]
│        └─ Números de teléfono
│           └─ Tabla:
│              ├─ Número: +57 1 2345 6789
│              ├─ Estado: Verificado ✓
│              └─ Phone Number ID: 1234567890123456  ← COPIAR ESTO
```

**⚠️ SI NO APARECE LA TABLA**:
- Verificar que tienes WhatsApp Business Account creada
- Si no: Crear en Meta Business Suite → Add Account → WhatsApp
- Vincular número telefónico

---

### Campo 3: 💼 Business Account ID (OPCIONAL pero recomendado)
**Por qué**: Identificar cuál es tu cuenta de negocio asociada  
**Formato**: Números, típicamente 13-15 dígitos (ej: 0987654321098)  
**Dónde obtenerlo**: Meta Business Manager → Business Information

#### 🎯 PASOS EXACTOS:

```
1. Ir a: https://business.facebook.com/

2. Esquina superior izquierda → Tu nombre
   → "Configuración del negocio"
   o "Business Settings"

3. En sidebar: "Información del negocio"
   o "Business Information"

4. Ver campo: "ID de negocio"
   o "Business ID"

5. COPIAR ese ID
   Ejemplo: 0987654321098
```

**📌 NOTA**: No es tan crítico como Phone Number ID, pero ayuda  
Si no quieres complicar, déjalo vacío (es opcional)

---

### Campo 4: 🔐 Access Token (REQUERIDO - muy importante!)
**Por qué**: Token de autenticación para que nuestra plataforma acceda a Meta API  
**Formato**: Comienza con "EAA" seguido de muchos caracteres alfanuméricos  
**Ejemplo**: `EAABC...xyzABCxyzABC...`  
**Duración**: Puede expirar (típicamente: permanente si es bien generado)

#### 🎯 PASOS EXACTOS:

```
1. Ir a: https://developers.facebook.com/

2. Ingresar o crear cuenta de developer (gratuito)

3. En "Mis apps" (o "My Apps"):
   - Si ya tienes app WhatsApp: Seleccionar
   - Si no: Crear nueva app
     - Tipo: "Negocio" (Business)
     - Nombre: "Mi Tienda WhatsApp" o similar

4. Una vez en la app, en sidebar:
   "WhatsApp" o sección similar

5. Pestaña: "Comenzar" o "Getting Started"

6. Buscar sección: "Generar token" o "Generate Token"

7. Click: "Generar token de acceso"
   o "Generate Access Token"

8. Seleccionar:
   ✓ WhatsApp Business Account (tu account)
   - Permisos: whatsapp_business_messaging

9. Copiar el token que aparece
   (Es una cadena larga que empieza con EAA)

10. ⚠️ GUARDAR EN LUGAR SEGURO
    - No compartir con nadie
    - No subirlo a GitHub
    - Es como contraseña
```

**⚠️ IMPORTANTE**:
- El token es sensible ↔ No compartir
- Si lo ve alguien, puede acceder a tu WhatsApp
- Si lo pierdes: Generar nuevo desde Meta

**🔄 Regeneración**:
- Token expiró o se compuso?
- Ir a: Meta → App → WhatsApp → Generate token
- Generar uno nuevo
- Actualizar en nuestra plataforma

---

### Campo 5: 🔓 Webhook Verify Token (REQUERIDO - creas tú!)
**Por qué**: Verificación de seguridad entre Meta y nuestra plataforma  
**Formato**: Cualquier cadena alfanumérica que quieras (ej: mi_token_secreto_2024)  
**Ejemplo**: 
- `secreto123`
- `mi_token_whatsapp_2024`
- `tienda_token_abc123`

#### 🎯 PASOS EXACTOS:

```
1. Inventar una contraseña que SOLO TÚ CONOCES
   ⚠️ No usar: "111", "password", "123456"
   
2. Usar algo como:
   - Combinación de números y letras
   - Mínimo 8 caracteres
   - Ej: "MiTienda_2024_Token"

3. GUARDAR este token en lugar seguro
   (necesitarás usarlo en Meta también)

4. Pegar ese token en OUR formulario

5. Luego, cuando configures webhook en Meta:
   - Usar el MISMO token
   - Meta verifica que coincida
   - Si coincide: comunicación validada ✓
```

**ejemplo de creación de token**:
```
Opción 1: Usar contraseña del negocio
"NombreTienda_Token_123"

Opción 2: Usar date + random
"tienda_20260419_abc8d3"

Opción 3: Usar generador
Visit: https://randomkeygen.com/
Copy: "Fort Knox Password"
Use: First 20 characters
```

**✅ Requisitos**:
- Mín 8 caracteres
- Alfanumérico (números + letras)
- Que recuerdes fácilmente
- Diferente del Access Token

---

## 🎯 RESUMEN - TABLA DE CAMPOS

| Campo | Requerido | Qué es | Dónde obtenerlo | Ejemplo |
|-------|-----------|--------|-----------------|---------|
| **Phone Number** | ❌ No | Número visible | Lo sabe la empresa | +57 1 2345 6789 |
| **Phone Number ID** | ✅ SÍ | ID del número en Meta | Meta Business → Phone Numbers | 1234567890 |
| **Business Account ID** | ❌ No | ID de tu negocio | Meta → Business Settings | 0987654321 |
| **Access Token** | ✅ SÍ | Token de acceso Meta API | Meta Developers → Generate | EAABx...xyz |
| **Webhook Token** | ✅ SÍ | Token de verificación (la creas tú) | Lo inventas | mi_token_2024 |

**✅ REQUERIDOS** (sin esto no funciona):
- Phone Number ID
- Access Token
- Webhook Token

**❌ OPCIONALES** (pero útiles):
- Phone Number
- Business Account ID

---

## 📝 CHECKLIST PARA LA EMPRESA

Darle esto a cada empresa para que complete:

```
☐ Tengo acceso a Meta Business Manager (https://business.facebook.com)
☐ Tengo una cuenta WhatsApp Business creada en Meta
☐ Tengo al menos un número WhatsApp registrado y verificado
☐ Tengo acceso a Meta for Developers (https://developers.facebook.com)
☐ He copiado el Phone Number ID de Meta
☐ He generado un Access Token en Meta Developers
☐ He creado y guardé un Webhook Verify Token (contraseña que inventé)
☐ Tengo todos los datos listos para copiar en el formulario
```

---

## 🔗 PASOS (Visión Integrada)

### Para Empresa: Obtener 5 Datos

```
META ACCOUNT SETUP (lo hacen una sola vez)
1. Tener cuenta Meta 
2. Crear WhatsApp Business Account
3. Verificar/registrar número telefónico

OBTENER 2 IDs DE META
4. Copiar: Phone Number ID (de Meta Business)
5. Copiar: Business Account ID (opcional)

GENERAR CREDENCIALES  
6. Crear: Access Token (en Meta for Developers)
7. Inventar: Webhook Verify Token (contraseña propia)

INGRESAR EN NUESTRA PLATAFORMA
8. Ir a http://localhost:5173/whatsapp
9. Pegar los 5 datos en formulario
10. Click "Guardar y verificar conexión"
```

---

## ⚠️ ERRORES COMUNES (Prevenir)

| Error | Causa | Solución |
|-------|-------|----------|
| "Phone Number ID inválido" | Copió mal /  número incompleto | Copiar de Meta nuevamente, sin espacios |
| "Access Token expirado" | Token de Meta expiró | Generar nuevo en Meta for Developers |
| "Webhook no verifica" | Webhook token no coincide | Usar el MISMO token en Meta y aquí |
| "401 Unauthorized" | Test no autorizado | Verificar Access Token sea válido |
| "No recibo mensajes" | Webhook no configurado en Meta | Configurar webhook URL en Meta |

---

## 📌 INSTRUCCIONES PARA LA EMPRESA (Texto a Copiar)

```
CONECTAR TU WHATSAPP BUSINESS
═══════════════════════════════════════

Necesitarás obtener 3-5 datos de Meta. Sigue estos pasos:

PASO 1: Phone Number ID
1. Ve a https://business.facebook.com
2. Click en "Configuración" → "Cuentas de WhatsApp Business"
3. Selecciona tu Cuenta WhatsApp
4. Pestaña "Números de teléfono"
5. Copia el "Phone Number ID" (ej: 1234567890)

PASO 2: Access Token  
1. Ve a https://developers.facebook.com
2. Selecciona tu app (o crea una nueva)
3. En "WhatsApp" → "Getting Started"
4. Click "Generate Access Token"
5. Copia el token (comienza con EAAB...)

PASO 3: Webhook Token (lo inventas tú)
1. Piensa una contraseña fuerte (ej: MiToken_2024_ABC)
2. Recuérdala, la usarás después

PASO 4: Ingresa los datos aquí
1. Ve a http://localhost:5173/whatsapp
2. Pega cada dato en su campo correspondiente
3. Click "Guardar y verificar conexión"
4. ¡Listo! Tus clientes pueden escribir en WhatsApp

⚠️ NO compartir:
- Access Token (es como contraseña)
- Tu número de teléfono
```

---

## 🎓 VALIDACIÓN EN TIEMPO REAL

Cuando empresa ingrese datos, validar:

```
Phone Number ID:
✓ Contiene solo dígitos
✓ Entre 10-20 caracteres
✓ No espacios

Access Token:
✓ Comienza con "EAAB" o "EAA"
✓ Al menos 100 caracteres
✓ Sin espacios al inicio/fin

Webhook Token:
✓ Al menos 6 caracteres
✓ Alfanumérico
✓ Sin espacios
```

---

## 📊 DATOS COMPLETOS DE EJEMPLO

```
Campo                 │ Valor Ejemplo
──────────────────────┼──────────────────────────────────
Número Teléfono       │ +57 1 (55) 2345-6789
Phone Number ID       │ 1234567890123456
Business Account ID   │ 0987654321098765
Access Token          │ EAABxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Webhook Token         │ MiTienda_2024_Secret

Resultado:
✅ Empresa conectada
✅ Agente IA respondera mensajes
✅ Clientes ven respuestas automáticas
```

---

## 🔐 PREGUNTAS DE SEGURIDAD

**¿Es seguro compartir estos datos?**
- Access Token = NO (muy sensible)
- Phone Number ID = SÍ (es público)
- Business Account ID = SÍ (es identificador)
- Webhook Token = NO (solo entre Meta y tu servidor)

**¿Qué pasa si alguien tiene mi Access Token?**
Puede:
- Enviar mensajes desde tu WhatsApp
- Ver tu información de negocio
- Costar dinero (Meta cobra por mensajes)

**Solucion**: Regenerar token inmediatamente en Meta

---

## 📱 FORMATO DE NÚMERO TELEFÓNICO (Opcional)

Si empresa ingresa número, aceptar formatos:
```
✓ +57 1 2345 6789
✓ +5712345678
✓ 57 1 2345 6789
✓ 0 1 2345 6789
✓ +57-1-2345-6789

Todos se normalizan a: +57 (1) 2345-6789
```

---

## ✅ FINAL CHECKLIST

Antes de que empresa intente conectarse, verificar:

- [x] Documentación clara
- [x] Pasos numerados
- [x] Ejemplos reales
- [x] Errores comunes listados
- [x] Requisitos claros
- [x] Texto copyable listo

**Resultado**: Empresa puede obtener datos sin confusión

---

**Guía Completa para Obtener Credenciales ✅**  
**Lista para Compartir con Empresas 📤**
