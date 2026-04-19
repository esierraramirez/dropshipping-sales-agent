# 📋 RESUMEN VISUAL - INFORMACIÓN WHATSAPP (Quick Reference)

**Propósito**: Ver de un vistazo qué pedir, cómo obtener y cómo validar  
**Audiencia**: Admin + Empresa  
**Formato**: Tablas visuales y checklists

---

## 🎯 TABLA MAESTRA - LOS 5 CAMPOS

```
┌──────────────┬──────┬────────────────┬──────────────┬────────────────────────┐
│ Campo        │ Req. │ Qué es         │ Dónde obtener│ Validación             │
├──────────────┼──────┼────────────────┼──────────────┼────────────────────────┤
│ Teléfono     │ ❌   │ Número visible │ Lo sabes     │ Formato +XX 123 4567   │
│ Phone ID     │ ✅   │ ID en Meta     │ Meta Biz     │ Solo dígitos, 10-16    │
│ Account ID   │ ❌   │ ID negocio     │ Meta Config  │ Solo dígitos, 9-15     │
│ Access Token │ ✅   │ Token API Meta │ Developers  │ EAA+ >100 chars        │
│ Webhook Token│ ✅   │ Lo inventas   │ Creas tú     │ 6-50 alfanumérico      │
└──────────────┴──────┴────────────────┴──────────────┴────────────────────────┘

MAPA MENTAL:
         ┌─── OPCIONAL (nice to have)
         │
EMPRESA ─┼─── PHONE ID ──→ META BUSINESS (1° copiar)
         │
         └─── ACCESS TOKEN ──→ META DEVELOPERS (2° generar)
                                    │
                                    └─── WEBHOOK TOKEN ──→ TÚ (3° inventar)
```

---

## 📱 CAMPO 1: NÚMERO DE TELÉFONO

```
┌─────────────────────────────────────────────┐
│ NÚMERO DE TELÉFONO                          │
├─────────────────────────────────────────────┤
│ Requerido:        ❌ NO                     │
│ Crítico:          ❌ NO                     │
│ Sourced by:       EMPRESA (Lo sabe)         │
│ Effort:           ⭐ (muy fácil)            │
│ Time to get:      < 1 minuto                │
│                                             │
│ Formatos válidos:                           │
│ ✓ +57 1 2345 6789                          │
│ ✓ +5712345678                              │
│ ✓ +57-1-2345-6789                          │
│ ✓ (57) 1 2345 6789                         │
│                                             │
│ Qué hacer si falta: Dejar vacío ✓           │
│                                             │
│ Validar:                                    │
│ ☐ Parece número real (9-13 dígitos)        │
│ ☐ Tiene código de país                     │
│ ☐ Está correcto según empresa              │
└─────────────────────────────────────────────┘
```

---

## 🔑 CAMPO 2: PHONE NUMBER ID

```
┌─────────────────────────────────────────────┐
│ PHONE NUMBER ID                             │
├─────────────────────────────────────────────┤
│ Requerido:        ✅ SÍ ← CRÍTICO!          │
│ Crítico:          ✅ SÍ                     │
│ Sourced by:       META BUSINESS MANAGER     │
│ Effort:           ⭐⭐⭐ (3 minutos)        │
│ Time to get:      ~3 minutos                │
│                                             │
│ DÓNDE COPIAR:                               │
│ business.facebook.com                       │
│ → Configuración                             │
│ → WhatsApp Business Accounts                │
│ → Tu Cuenta                                 │
│ → Números de teléfono                       │
│ → Columna "Phone Number ID"                 │
│                                             │
│ Ejemplo:                                    │
│ 1234567890123456                            │
│                                             │
│ Qué validar:                                │
│ ☐ Solo números (sin letras)                │
│ ☐ 10-16 dígitos típicamente                │
│ ☐ Sin espacios, guiones, etc.              │
│ ☐ Copiado directamente de Meta             │
│                                             │
│ Si no aparece:                              │
│ ❌ No tienes WhatsApp Account creada        │
│ ❌ Tu número no está registrado             │
│ → Crear primero en Meta                     │
│                                             │
│ Qué hacer si es incorrecto:                 │
│ → Copiar de nuevo desde Meta                │
│ → NO inventar ni usar anterior              │
└─────────────────────────────────────────────┘
```

---

## 💼 CAMPO 3: BUSINESS ACCOUNT ID

```
┌─────────────────────────────────────────────┐
│ BUSINESS ACCOUNT ID                         │
├─────────────────────────────────────────────┤
│ Requerido:        ❌ NO                     │
│ Crítico:          ❌ NO                     │
│ Sourced by:       META BUSINESS SETTINGS    │
│ Effort:           ⭐⭐ (1-2 minutos)       │
│ Time to get:      ~2 minutos                │
│                                             │
│ DÓNDE COPIAR:                               │
│ business.facebook.com                       │
│ → Tu nombre (esquina superior izquierda)    │
│ → Configuración del negocio                 │
│ → Información del negocio                   │
│ → Campo "ID de negocio"                     │
│                                             │
│ O buscar en URL (alternativa):              │
│ business.facebook.com/[ID_AQUI]/?...        │
│                                             │
│ Ejemplo:                                    │
│ 0987654321098765                            │
│                                             │
│ Qué validar:                                │
│ ☐ Solo números                             │
│ ☐ 9-15 dígitos típicamente                 │
│ ☐ Sin caracteres especiales                │
│                                             │
│ Qué hacer si no encuentras:                │
│ → Está OK, es OPCIONAL ✓                    │
│ → Déjalo vacío, no hay problema            │
│                                             │
│ Restricción:                                │
│ ⚠️ No usar ID de otra empresa              │
│ ⚠️ Debe ser tu propio ID                   │
└─────────────────────────────────────────────┘
```

---

## 🔐 CAMPO 4: ACCESS TOKEN

```
┌─────────────────────────────────────────────┐
│ ACCESS TOKEN                                │
├─────────────────────────────────────────────┤
│ Requerido:        ✅ SÍ ← MUY CRÍTICO!      │
│ Crítico:          ✅ SÍ                     │
│ Sourced by:       META FOR DEVELOPERS       │
│ Effort:           ⭐⭐⭐⭐⭐ (5 min)     │
│ Time to get:      ~5 minutos                │
│                                             │
│ PASOS:                                      │
│ 1. developers.facebook.com                  │
│ 2. Mis Apps (o crear nueva)                 │
│ 3. Seleccionar app WhatsApp                 │
│ 4. Pestaña "WhatsApp"                       │
│ 5. Sección "Generar Access Token"           │
│ 6. Seleccionar Cuenta WhatsApp              │
│ 7. COPIAR token                             │
│                                             │
│ Ejemplo (TRUNCADO):                         │
│ EAABC987XYZ123...ABC123XYZ987...           │
│ (El token real es MUCHO más largo)         │
│                                             │
│ Qué validar:                                │
│ ☐ Comienza con "EAAB" o "EAA"             │
│ ☐ MUY largo (>100 caracteres)              │
│ ☐ Sin espacios adentro                     │
│ ☐ Sin "Bearer" al principio                │
│ ☐ Freshly generated (esta semana)          │
│                                             │
│ ⚠️ SEGURIDAD CRÍTICA:                      │
│ • NO compartir nunca                        │
│ • NO subir a GitHub                        │
│ • NO enviar por email sin encriptar        │
│ • Es como UNA CONTRASEÑA                   │
│                                             │
│ Si expira o se corrompe:                    │
│ → Generar TOKEN NUEVO en Meta              │
│ → Actualizar aquí                          │
│ → Listo                                    │
└─────────────────────────────────────────────┘
```

---

## 🔓 CAMPO 5: WEBHOOK VERIFY TOKEN

```
┌─────────────────────────────────────────────┐
│ WEBHOOK VERIFY TOKEN                        │
├─────────────────────────────────────────────┤
│ Requerido:        ✅ SÍ                     │
│ Crítico:          ✅ SÍ                     │
│ Sourced by:       TÚ MISMO (Lo inventas)    │
│ Effort:           ⭐ (muy fácil)            │
│ Time to get:      < 1 minuto                │
│                                             │
│ ¿QUÉ HACER?                                 │
│ INVENTA una contraseña:                     │
│                                             │
│ ✓ Ejemplos válidos:                         │
│   - MiTienda_Token_2024                     │
│   - secreto123abc                           │
│   - tienda_whatsapp_seed_99                 │
│                                             │
│ ✗ Ejemplos inválidos:                       │
│   - "123" (muy corto)                       │
│   - "password" (muy obvio)                  │
│   - "mi token" (contiene espacio)           │
│   - "token@123" (caracteres especiales)     │
│                                             │
│ Requisitos:                                 │
│ ☐ Mín 6 caracteres                         │
│ ☐ Máx 50 caracteres                        │
│ ☐ Alfanumérico + guiones/guiones bajos     │
│ ☐ Sin espacios                             │
│ ☐ Lo recuerdas                             │
│ ☐ Único/no compartido                      │
│                                             │
│ GUARDAR TOKEN:                              │
│ Escribe en lugar seguro:                    │
│ ___________________________________         │
│                                             │
│ ⚠️ IMPORTANTE:                              │
│ Este token lo usarás TAMBIÉN en Meta       │
│ Debe coincidir exactamente:                │
│ 1. Generas: "MyToken2024"                  │
│ 2. Pegas aquí: "MyToken2024" ✓             │
│ 3. Pegas en Meta: "MyToken2024" ✓          │
│ 4. Si coinciden → Funciona ✓               │
│ 5. Si NO coinciden → ❌ Error              │
└─────────────────────────────────────────────┘
```

---

## 🎯 PASO A PASO VISUAL

```
EMPRESA QUIERE CONECTAR WHATSAPP
│
├─ PASO 1: Obtener Phone Number ID
│  └─ browser.facebook.com → WhatsApp → Copiar ID
│     Tiempo: 3 min ⭐⭐⭐
│     Dificultad: Media
│
├─ PASO 2: Generar Access Token
│  └─ developers.facebook.com → Generate token
│     Tiempo: 5 min ⭐⭐⭐⭐⭐
│     Dificultad: Alta (requiere varios clicks)
│
├─ PASO 3: Inventar Webhook Token
│  └─ Pensar en contraseña fuerte
│     Tiempo: 1 min ⭐
│     Dificultad: Muy fácil
│
├─ PASO 4: Copiar en formulario
│  └─ http://localhost:5173/whatsapp
│     Tiempo: 2 min ⭐⭐
│     Dificultad: Fácil (copy-paste)
│
└─ RESULTADO: ✅ WhatsApp Conectado
```

---

## ✅ CHECKLIST RÁPIDO

### Para EMPRESA (Antes de ingresar datos)

```
TENGO ACCESO A:
☐ Meta Business Manager (facebook.com)
☐ Mi Cuenta WhatsApp Business creada
☐ Mi número WhatsApp verificado
☐ Meta for Developers (developers.facebook.com)

HE COPIADO:
☐ Phone Number ID (de Meta Business)
☐ Access Token (de Meta Developers)
☐ Business Account ID (opcional, de Meta Settings)

HE CREADO:
☐ Webhook Token (inventé una contraseña)

HE GUARDADO:
☐ Todos los datos en lugar seguro
☐ El Webhook Token en mis notas

ESTOY LISTO:
☐ Ir a http://localhost:5173/whatsapp
☐ Pegar los 5 datos
☐ Click "Guardar y verificar conexión"
```

### Para ADMIN (Validando datos recibidos)

```
VALIDAR Phone Number ID:
☐ Solo números
☐ 10-16 caracteres
☐ Sin espacios

VALIDAR Access Token:
☐ Comienza con "EAA"
☐ > 100 caracteres
☐ Sin espacios

VALIDAR Webhook Token:
☐ 6-50 caracteres
☐ Alfanumérico
☐ Sin espacios especiales

RESULTADO:
☐ Todos los datos válidos → ✅ APROBAR
☐ Algo falta o es inválido → ❌ RECHAZAR + correcciones
```

---

## 🚨 MATRIZ DE ERRORES

```
┌────────────────────┬──────────────┬─────────────────────────────────┐
│ Error              │ Severidad    │ Solución                        │
├────────────────────┼──────────────┼─────────────────────────────────┤
│ Phone ID inválido  │ 🔴 CRÍTICA   │ Copiar nuevamente de Meta       │
│ Token expirado     │ 🔴 CRÍTICA   │ Generar nuevo token en Meta     │
│ Webhook no verifica│ 🔴 CRÍTICA   │ Usar mismo token en Meta        │
│ ID no coincide     │ 🔴 CRÍTICA   │ Verificar ID correcto en Meta   │
│ Correo incompleto  │ 🟠 MEDIA     │ Copiar nuevamente completo      │
│ Teléfono invalido  │ 🟡 BAJA      │ Corregir formato O dejar vacío  │
│ Account ID vacío   │ 🟢 BAJA      │ OK - es opcional                │
└────────────────────┴──────────────┴─────────────────────────────────┘
```

---

## 📊 RESUMEN TABLA FINAL

| Aspecto | Phone | Phone ID | Account ID | Access Token | Webhook Token |
|---------|-------|----------|-----------|--------------|---------------|
| **Requerido** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Crítico** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Origen** | Empresa | Meta Biz | Meta Config | Meta Dev | Empresa |
| **Tiempo** | <1 min | 3 min | 2 min | 5 min | 1 min |
| **Dificultad** | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Validación** | Formato | Dígitos | Dígitos | EAA+largo | Alfanumérico |
| **Sensible** | ❌ | ❌ | ❌ | ✅ | ⚠️ |
| **Compartir** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Puede variar** | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## ⏱️ TIMELINE TOTAL

```
Empresa obtiene datos:
├─ Fase 1 (1 min):   Verifica acceso a Meta
├─ Fase 2 (3 min):   Copia Phone ID
├─ Fase 3 (5 min):   Genera Access Token
├─ Fase 4 (1 min):   Inventa Webhook Token
├─ Fase 5 (2 min):   Ingresa datos en formulario
│
└─ TOTAL: ~12 minutos ⏱️

Si ya tiene experiencia: ~6-8 minutos
Si es primera vez: ~15-20 minutos
```

---

## 🎓 QUICK TEACH (Para explicar a empresa)

```
"Necesito 5 datos para conectar tu WhatsApp:

1. Tu número (opcional) - Sabes
2. ID del número (Meta) - Copiar 3 min
3. ID negocio (Meta) - Opcional, 2 min
4. Token acceso (Developers) - Generar 5 min ⚠️ SENSIBLE
5. Token de seguridad (Tú) - Inventar 1 min

Total: ~12 minutos

Dos campos son especiales:
- Access Token: ES CLAVE, no compartir con nadie
- Webhook Token: Lo inventas, lo usarás también en Meta

¿Tienes dudas en algún paso?"
```

---

## 📌 RECORD SHEET (Para admin)

```
EMPRESA: ___________________________
FECHA: _____________________________

DATOS INGRESADOS:
☐ Teléfono:          _______________________________
☐ Phone ID:          _______________________________
☐ Account ID:        _______________________________ (opt)
☐ Access Token:      PRESENTE ☐ / AUSENTE ☐
☐ Webhook Token:     PRESENTE ☐ / AUSENTE ☐

VALIDACIÓN:
☐ Phone ID: dígitos ✓ / longitud ✓ / formato ✓
☐ Access Token: EAA ✓ / largo ✓ / sin espacios ✓
☐ Webhook Token: válido ✓ / alfanumérico ✓

RESULTADO:
☐ ✅ APROBADO - Todo correcto
☐ ⚠️ REVISIÓN - Algunos datos dudosos
☐ ❌ RECHAZADO - Errores, reenviando a empresa

NOTAS:
_________________________________________
_________________________________________
```

---

**Referencia Rápida Completa ✅**  
**Lista para Imprimir o Tener a Mano** 📋
