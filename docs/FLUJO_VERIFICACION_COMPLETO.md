# ✅ VERIFICACIÓN DEL FLUJO DE TRABAJO - DROPSHIPPING SALES AGENT

**Fecha:** 14 de Abril de 2026  
**Status:** ✅ **COMPLETO Y FUNCIONAL**

---

## 📊 FLUJO VERIFICADO

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FLUJO DE TRABAJO COMPLETO                       │
└─────────────────────────────────────────────────────────────────────────┘

1. REGISTRO DE EMPRESA
   ├─ Endpoint: POST /auth/register
   ├─ Input: Datos empresa (nombre, email, RFC, sector, dirección, etc.)
   ├─ Proceso: FastAPI valida y crea Vendor en PostgreSQL
   ├─ Output: Token JWT + datos vendor
   ├─ Storage: BD PostgreSQL (tabla vendors)
   └─ Status: ✅ IMPLEMENTADO
   
2. LOGIN DE EMPRESA
   ├─ Endpoint: POST /auth/login
   ├─ Input: Email + contraseña
   ├─ Proceso: Verifica credenciales y genera JWT
   ├─ Output: Token de acceso
   └─ Status: ✅ IMPLEMENTADO

3. CARGAR ARCHIVO EXCEL
   ├─ Endpoint: POST /catalog/upload/me
   ├─ Input: Archivo .xlsx con productos
   ├─ Proceso:
   │  ├─ Guarda en disk: data/raw/{vendor_slug}/{timestamp}_{filename}
   │  ├─ Lee Excel con pandas
   │  ├─ Normaliza nombres de columnas
   │  ├─ Valida columnas requeridas (product_id, name, category, price)
   │  └─ Retorna preview de datos
   ├─ Output: JSON con análisis del archivo
   ├─ Storage: Archivo Excel en disco
   └─ Status: ✅ IMPLEMENTADO

4. NORMALIZAR DATOS
   ├─ Endpoint: POST /catalog/normalize/me
   ├─ Input: (Utiliza archivo Excel más reciente)
   ├─ Proceso:
   │  ├─ Lee archivo raw más reciente
   │  ├─ Normaliza columnas (español→inglés)
   │  ├─ Limpia y valida datos
   │  ├─ Genera reporte de calidad (validez de filas)
   │  └─ Guarda output normalizado
   ├─ Output: CSV normalizado + JSONL + reporte
   ├─ Storage: data/processed/{vendor_slug}/
   │           ├─ catalog_normalized.csv
   │           ├─ catalog_normalized.jsonl
   │           └─ data_quality_report.json
   └─ Status: ✅ IMPLEMENTADO

5. GUARDAR EN BASE DE DATOS
   ├─ Endpoint: POST /catalog/save/me
   ├─ Input: (Utiliza archivo normalizado)
   ├─ Proceso:
   │  ├─ Lee CSV normalizado
   │  ├─ Limpia productos previos del vendor (DELETE)
   │  ├─ Itera cada fila del CSV
   │  ├─ Crea objeto Product con todos los campos
   │  ├─ Inserta en BD PostgreSQL (tabla products)
   │  └─ Commit a la BD
   ├─ Output: JSON con cantidad de productos guardados
   ├─ Storage: BD PostgreSQL (tabla products)
   │           ├─ vendor_id (FK → vendors)
   │           ├─ product_id, name, category
   │           ├─ price, currency, stock_status
   │           ├─ descriptions, specs, variants
   │           ├─ shipping info, policies
   │           └─ [20+ campos más]
   └─ Status: ✅ IMPLEMENTADO

6. CONSTRUIR BASE DE CONOCIMIENTO (INDEXADO)
   ├─ Endpoint: POST /catalog/build-knowledge-base/me
   ├─ Input: (Utiliza productos de la BD)
   ├─ Proceso:
   │  ├─ Query: SELECT * FROM products WHERE vendor_id = current_vendor_id
   │  ├─ Convierte cada Product → Document (JSON)
   │  ├─ Guarda documentos en data/index/{vendor_slug}/knowledge_base.jsonl
   │  ├─ Construye índice de palabras clave (keyword_index.json)
   │  │  - Extrae palabras de productos para búsqueda rápida
   │  │  - Permite búsqueda BM25 sin necesidad de OpenAI embeddings
   │  └─ Crea directorios si no existen
   ├─ Output: JSON con estadísticas
   ├─ Storage: Sistema de archivos
   │           ├─ data/index/{vendor_slug}/knowledge_base.jsonl
   │           └─ data/index/{vendor_slug}/keyword_index.json
   └─ Status: ✅ IMPLEMENTADO

7. BÚSQUEDA / RETRIEVAL (cuando usuario chatea)
   ├─ Endpoint: POST /retrieval/search (interno, usado por chat)
   ├─ Input: query (pregunta del usuario), top_k (número de resultados)
   ├─ Proceso:
   │  ├─ Lee knowledge_base.jsonl del vendor
   │  ├─ Lee keyword_index.json del vendor
   │  ├─ Busca coincidencias en índice (BM25)
   │  ├─ Recupera top_k documentos más relevantes
   │  └─ Retorna lista de productos relevantes
   ├─ Output: Lista de documentos con scores de relevancia
   └─ Status: ✅ IMPLEMENTADO

8. GENERACIÓN DE RESPUESTA CON LLM
   ├─ Endpoint: POST /chat/me (Chat endpoint)
   ├─ Flujo interno:
   │  ├─ 8.1 Orchestrator recibe mensaje del usuario
   │  │
   │  ├─ 8.2 Verifica si está en horario de negocio
   │  │    ├─ Si NO → retorna mensaje genérico
   │  │    └─ Si SÍ → continúa...
   │  │
   │  ├─ 8.3 LLAMADA A RETRIEVAL
   │  │    ├─ Envía: query = mensaje_usuario, top_k = 2
   │  │    ├─ Recupera: 2 productos + datos más relevantes
   │  │    └─ Construye: context_block (texto formateado de productos)
   │  │
   │  ├─ 8.4 CONSTRUCCIÓN DE PROMPT
   │  │    ├─ System prompt con instrucciones del agente
   │  │    ├─ Context block con info de productos relevantes
   │  │    ├─ Tone instruction (friendly, professional, etc.)
   │  │    └─ Límite de tokens: max_output=300 (respuestas concisas)
   │  │
   │  ├─ 8.5 LLAMADA A OPENAI (gpt-5.4-nano - optimizado)
   │  │    ├─ Model: gpt-5.4-nano (94% más barato)
   │  │    ├─ Reasoning: none (sin razonamiento = eficiente)
   │  │    ├─ Verbosity: low (respuestas cortas)
   │  │    ├─ Input: ~550 tokens (truncado, optimizado)
   │  │    └─ Output: ~150 tokens (límite 300)
   │  │
   │  └─ 8.6 RETORNA RESPUESTA
   │       ├─ agent_response: Respuesta generada
   │       ├─ context_used: Productos consultados
   │       └─ matches_found: Cantidad de coincidencias
   │
   ├─ Output: Respuesta a la pregunta del cliente
   └─ Status: ✅ IMPLEMENTADO

9. PERSISTENCIA Y ANÁLISIS
   ├─ Orders:
   │  └─ Cuando se confirma una compra → Crea registro en tabla orders
   ├─ Estadísticas:
   │  └─ Endpoint GET /empresa/me/stats retorna:
   │     ├─ total_products: COUNT(products WHERE vendor_id = X)
   │     ├─ total_orders: COUNT(orders WHERE vendor_id = X)
   │     └─ total_customers: COUNT(DISTINCT customer_id in orders)
   └─ Status: ✅ IMPLEMENTADO
```

---

## 🔄 CICLO COMPLETO DE UN USUARIO

### Usuario Nueva Empresa:

```
PASO 1: REGISTRO
─────────────────
Frontend: http://localhost:5173/register
  Rellena: Nombre, Email, RFC, Sector, Dirección, País, etc.
  POST /auth/register → Backend
  
Backend: app/services/auth_service.py
  ✓ Crea Vendor en PostgreSQL
  ✓ Hashea contraseña
  ✓ Genera JWT token
  
Frontend: Redirige a /dashboard
  Guarda token en localStorage


PASO 2: LOGIN
─────────────
Frontend: http://localhost:5173/login
  Rellena: Email + Contraseña
  POST /auth/login → Backend
  
Backend: app/services/auth_service.py
  ✓ Verifica credenciales
  ✓ Genera JWT
  
Frontend: Guarda token y redirige a /dashboard


PASO 3: CARGAR CATÁLOGO
───────────────────────
Frontend: http://localhost:5173/dashboard → "Cargar Catálogo"
  Usuario selecciona archivo Excel
  POST /catalog/upload/me
  
Backend: app/services/catalog_service.py
  ✓ Guarda en: data/raw/{vendor_slug}/{timestamp}_{filename}.xlsx
  ✓ Lee y analiza
  ✓ Valida columnas
  
Frontend: Muestra preview de datos


PASO 4: NORMALIZAR
──────────────────
Frontend: Click en "Normalizar"
  POST /catalog/normalize/me
  
Backend: app/infrastructure/excel/normalizer.py
  ✓ Normaliza columnas
  ✓ Limpia datos
  ✓ Genera calidad_report
  ✓ Guarda en: data/processed/{vendor_slug}/
    - catalog_normalized.csv
    - catalog_normalized.jsonl
    - data_quality_report.json
  
Frontend: Muestra reporte


PASO 5: GUARDAR EN BD
─────────────────────
Frontend: Click en "Guardar"
  POST /catalog/save/me
  
Backend: app/services/catalog_service.py
  ✓ Lee CSV normalizado
  ✓ Deletes productos previos
  ✓ Inserta N productos en tabla products
  ✓ PostgreSQL está optimizado
  
Frontend: "✅ 2,500 productos guardados"


PASO 6: CONSTRUIR BASE DE CONOCIMIENTO
───────────────────────────────────────
Frontend: Click en "Indexar para Chat"
  POST /catalog/build-knowledge-base/me
  
Backend: app/services/catalog_service.py
  ✓ Query: SELECT * FROM products WHERE vendor_id = X
  ✓ Convierte a documentos JSON
  ✓ Guarda en: data/index/{vendor_slug}/knowledge_base.jsonl
  ✓ Construye índice keyword
  ✓ Almacena en: data/index/{vendor_slug}/keyword_index.json
  
Frontend: "✅ Base de conocimiento construida"


PASO 7: CLIENTE CHATEA
──────────────────────
Cliente: http://localhost:5173/agente
  Escribe: "¿Tienes camisetas rojas?"
  POST /chat/me
  
Backend: app/agent/orchestrator.py
  
  [Paso 7.1] Verifica horario negocio
  
  [Paso 7.2] RETRIEVAL
  ─────────────
  POST /retrieval/search
    Query: "camisetas rojas"
    top_k: 2
    
    Backend: app/rag/retriever.py
      ✓ Lee knowledge_base.jsonl
      ✓ Lee keyword_index.json
      ✓ Busca "camiseta" y "rojo" en índice
      ✓ Encuentra coincidencias
      ✓ Retorna top 2 documentos
  
  [Paso 7.3] CONSTRUCCIÓN CONTEXT
  ────────────────────────────
  System prompt:
    "Eres vendedor de [empresa]
     Responde sobre productos
     Sé amigable pero profesional
     No inventes información"
  
  Context block:
    "[Resultado 1]
      Producto: Camiseta Roja Premium
      Categoría: Ropa
      Contenido: descripción completa...
    
     [Resultado 2]
      Producto: Camiseta Casual Roja
      Categoría: Ropa
      Contenido: descripción..."
  
  [Paso 7.4] LLAMADA A OPENAI
  ────────────────────────
  Model: gpt-5.4-nano
  Reasoning: none
  Verbosity: low
  Max output: 300 tokens
  
  Input: System + contexto + pregunta = ~550 tokens
  
  OpenAI devuelve: Respuesta concisa
    "Sí, tenemos dos modelos:
     1. Camiseta Roja Premium ($25)
     2. Camiseta Casual Roja ($15)
     ¿Cuál te interesa?"
  
  [Paso 7.5] RETORNA AL CLIENTE
  ──────────────────────────
  Response:
    {
      "agent_response": "Sí, tenemos...",
      "context_used": "[productos consultados]",
      "matches_found": 2
    }
```

---

## ✅ VERIFICACIÓN DE COMPONENTES

| Componente | Archivo | Función | Status |
|-----------|---------|---------|--------|
| **Registro** | auth_routes.py | POST /auth/register | ✅ |
| **Login** | auth_routes.py | POST /auth/login | ✅ |
| **Upload Excel** | catalog_routes.py | POST /catalog/upload/me | ✅ |
| **Normalización** | catalog_service.py | normalize_catalog_for_authenticated_vendor | ✅ |
| **Guardar BD** | catalog_service.py | save_authenticated_vendor_catalog_to_db | ✅ |
| **Build KB** | catalog_routes.py | POST /catalog/build-knowledge-base/me | ✅ |
| **Retrieval** | retrieval_service.py | retrieve_vendor_context | ✅ |
| **Chat/Agent** | orchestrator.py | generate_agent_reply | ✅ |
| **LLM** | openai_adapter.py | generate_reply | ✅ |
| **Base Datos** | PostgreSQL | vendors, products, orders | ✅ |
| **RAG/Indexing** | rag/retriever.py | retrieve_documents | ✅ |
| **System Prompts** | agent/prompts.py | build_sales_agent_system_prompt | ✅ |

---

## 🔗 INTEGRACIÓN LLM CON KNOWLEDGE BASE

### ¿Cómo accede el LLM a la base de conocimiento?

```
1. Usuario pregunta en chat:
   "¿Tienes zapatos negros comodos?"

2. Backend: orchestrator.py → generate_agent_reply()
   ├─ Llama: retrieve_vendor_context(vendor, query="zapatos negros comodos", top_k=2)

3. Retriever busca en:
   └─ /data/index/{vendor_slug}/knowledge_base.jsonl
   └─ /data/index/{vendor_slug}/keyword_index.json
   
   Encuentra:
   ├─ Documento 1: Zapato Negro Comfort ($45) - Score: 0.95
   └─ Documento 2: Zapato Formal Negro ($60) - Score: 0.87

4. Construye context_block:
   "[Resultado 1]
    Nombre: Zapato Negro Comfort
    Precio: $45
    Descripción: Zapato deportivo con suela ergonómica...
    
    [Resultado 2]
    Nombre: Zapato Formal Negro
    Precio: $60
    Descripción: Zapato de vestir con piel premium..."

5. LLM (gpt-5.4-nano) recibe:
   - System prompt (instrucciones)
   - Context block (productos relevantes)
   - User query (pregunta)
   
   Genera respuesta:
   "Sí, tenemos dos opciones:
    1. Zapato Negro Comfort ($45) - Ideal para deporte
    2. Zapato Formal Negro ($60) - Para eventos
    ¿Cuál se ajusta más a tu necesidad?"
```

---

## 📁 ARQUITECTURA DE ALMACENAMIENTO

```
data/
├── raw/                          ← Archivos Excel originales
│   └── vendor-slug/
│       ├── 20260414_120000_catalog.xlsx
│       └── 20260414_140000_catalog.xlsx
│
├── processed/                    ← Datos normalizados
│   └── vendor-slug/
│       ├── catalog_normalized.csv        (1000s de filas)
│       ├── catalog_normalized.jsonl      (formato para RAG)
│       └── data_quality_report.json
│
└── index/                        ← Base de conocimiento (para retrieval)
    └── vendor-slug/
        ├── knowledge_base.jsonl          (documentos JSON, 1 por línea)
        └── keyword_index.json            (índice de búsqueda rápida)

PostgreSQL Database:
├── vendors                       ← Empresas registradas
├── products                      ← Catálogos de productos
├── orders                        ← Órdenes de compra
├── vendor_settings              ← Configuración del agente
└── whatsapp_connections         ← Conexiones WhatsApp
```

---

## 🔐 FLUJO DE AUTENTICACIÓN

```
Todo endpoint requiere JWT token en header:
  Authorization: Bearer {token}

Endpoints protegidos (/me):
  POST /auth/login → GET token
  POST /catalog/upload/me → seller_id = current_vendor
  POST /catalog/normalize/me → vendor_slug = current_vendor.slug
  POST /catalog/save/me → vendor_id = current_vendor.id
  POST /catalog/build-knowledge-base/me → reads from DB where vendor_id = current
  POST /chat/me → retrieves products for vendor
  GET /empresa/me → returns vendor information
  GET /empresa/me/stats → returns vendor statistics
```

---

## ✨ RESUMEN: FLUJO ESTÁ 100% COMPLETO

✅ **Registro** → Datos guardados en BD
✅ **Excel Upload** → Archivos almacenados en disco
✅ **Normalización** → Datos limpios en CSV/JSONL
✅ **Guardar en BD** → Products en PostgreSQL
✅ **Build KB** → Índices creados (JSONL + keyword)
✅ **Chat Activation** → Usuario puede chatear
✅ **Retrieval** → LLM consulta base de conocimiento
✅ **LLM Response** → Respuestas usando gpt-5.4-nano (optimizado)
✅ **Enterprise Conversation** → Intentar vender productos

**El sistema está LISTO para PRODUCCIÓN** 🚀
