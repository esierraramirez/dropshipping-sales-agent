# Mapa de Endpoints para Validacion con CSV

Este documento sirve para probar la funcionalidad del sistema endpoint por endpoint y verificar dos trazas distintas en CSV:

- `data/audit/endpoint_requests.csv`: se llena por cada request HTTP que entra al backend.
- `data/audit/crud_operations.csv`: se llena cuando hay operaciones ORM de `CREATE`, `READ`, `UPDATE` o `DELETE`.

## Regla de lectura

- Si el endpoint solo responde con datos o valida algo sin tocar la BD, debe modificar solo `endpoint_requests.csv`.
- Si el endpoint consulta o muta modelos SQLAlchemy, debe modificar `endpoint_requests.csv` y, además, `crud_operations.csv`.
- Si el endpoint falla antes de ejecutar SQL, aun asi debe dejar huella en `endpoint_requests.csv` con su `status_code`.

## Orden sugerido de pruebas

1. Autenticacion y perfil.
2. Empresa y configuracion.
3. Catalogo y productos.
4. Ordenes.
5. Auditoria y trazabilidad.
6. WhatsApp, retrieval, chat, LLM y dashboard.
7. Health y endpoints de control.

## Mapa de endpoints

| Metodo | Endpoint | Modelo o recurso principal | Debe modificar `endpoint_requests.csv` | Debe modificar `crud_operations.csv` | Observacion de prueba |
|---|---|---|---|---|---|
| GET | `/health` | Salud del backend | Si | No | Validar que aun sin BD se escriba una fila HTTP. |
| POST | `/auth/register` | Vendor | Si | Si | Crea vendor y token. Debe registrar CREATE. |
| POST | `/auth/login` | Vendor | Si | Si | Consulta vendor y autentica. Debe registrar READ. |
| GET | `/auth/me` | Vendor | Si | Si | Lee perfil del vendor autenticado. |
| GET | `/empresa/me` | Vendor | Si | Si | Consulta datos de empresa. |
| PATCH | `/empresa/me` | Vendor | Si | Si | Actualiza datos de empresa. Debe registrar UPDATE. |
| GET | `/empresa/me/stats` | Vendor / agregados | Si | Si | Valida estadisticas y conteos. |
| DELETE | `/empresa/me` | Vendor | Si | Si | Desactivacion logica. Debe dejar historicidad. |
| POST | `/catalog/upload/me` | Catalogo de archivo | Si | No necesariamente | Guarda archivo subido y deja huella HTTP. |
| POST | `/catalog/normalize/me` | Catalogo | Si | Si | Normaliza datos; suele generar archivos procesados. |
| POST | `/catalog/save/me` | Product | Si | Si | Inserta productos en BD. Debe registrar CREATE por producto. |
| GET | `/catalog/products/me` | Product | Si | Si | Lista productos del vendor. Debe registrar READ. |
| GET | `/catalog/products/me/filter` | Product | Si | Si | Filtro por `category` y/o `stock_status`. |
| GET | `/catalog/products/{product_id}` | Product | Si | Si | Consulta por ID con 404 si no existe. |
| PATCH | `/catalog/products/{product_id}` | Product | Si | Si | Actualiza campos permitidos. Debe registrar UPDATE. |
| DELETE | `/catalog/products/{product_id}` | Product | Si | Si | Soft delete con historicidad y auditoria. |
| POST | `/catalog/build-knowledge-base/me` | Knowledge base / Product | Si | Si | Construye indice semantico del catalogo. |
| GET | `/catalog/knowledge-base/me` | Knowledge base / Product | Si | No necesariamente | Solo consulta metadata del KB. |
| POST | `/orders/me` | Order | Si | Si | Crea orden. Debe registrar CREATE. |
| GET | `/orders/me` | Order | Si | Si | Lista ordenes del vendor. |
| GET | `/orders/me/{order_id}` | Order | Si | Si | Detalle de una orden. |
| PATCH | `/orders/me/{order_id}/status` | Order | Si | Si | Actualiza estado de orden. |
| DELETE | `/orders/me/{order_id}` | Order | Si | Si | Elimina orden y registra DELETE. |
| GET | `/audit/products/{product_id}/history` | AuditLog / Product | Si | Si | Lee historial del producto. |
| GET | `/audit/products/deleted` | Product | Si | Si | Lista productos archivados. |
| POST | `/audit/products/{product_id}/restore` | Product / AuditLog | Si | Si | Restaura producto y registra evento. |
| GET | `/audit/logs` | AuditLog | Si | Si | Lista logs historicos. |
| GET | `/settings/me` | VendorSettings | Si | Si | Consulta configuracion del agente. |
| PUT | `/settings/me` | VendorSettings | Si | Si | Crea o actualiza configuracion. |
| POST | `/llm/test` | LLM / prueba tecnica | Si | No necesariamente | Debe escribir solo request HTTP si no toca BD. |
| POST | `/retrieval/search` | RAG / retrieval | Si | Si o No | Depende de si consulta BD o indice. Igual debe escribir HTTP CSV. |
| POST | `/chat/me` | Chat / agente | Si | Si o No | Debe escribir HTTP CSV siempre; si consulta BD, tambien CRUD CSV. |
| GET | `/dashboard/me` | Dashboard | Si | Si o No | Normalmente solo lectura agregada. |
| GET | `/vendors` | Vendor | Si | Si | Listado de vendors; valida lectura de modelo. |
| PUT | `/whatsapp/me` | WhatsAppConnection | Si | Si | Upsert de credenciales/configuracion. |
| GET | `/whatsapp/me` | WhatsAppConnection | Si | Si | Consulta la conexion activa. |
| GET | `/whatsapp/webhook` | WhatsAppConnection | Si | No necesariamente | Verificacion del webhook; puede no tocar BD si falla el token. |
| POST | `/whatsapp/webhook` | WhatsApp / agente | Si | Si o No | Procesamiento de mensajes entrantes; debe dejar huella HTTP. |

## Mapa por modelo

### Vendor

- Crear: `POST /auth/register`
- Leer: `POST /auth/login`, `GET /auth/me`, `GET /empresa/me`, `GET /empresa/me/stats`, `GET /vendors`
- Actualizar: `PATCH /empresa/me`
- Eliminar: `DELETE /empresa/me`

### Product

- Crear: `POST /catalog/save/me`
- Leer: `GET /catalog/products/me`, `GET /catalog/products/me/filter`, `GET /catalog/products/{product_id}`
- Actualizar: `PATCH /catalog/products/{product_id}`
- Eliminar: `DELETE /catalog/products/{product_id}`
- Historial: `GET /audit/products/{product_id}/history`, `GET /audit/products/deleted`, `POST /audit/products/{product_id}/restore`

### Order

- Crear: `POST /orders/me`
- Leer: `GET /orders/me`, `GET /orders/me/{order_id}`
- Actualizar: `PATCH /orders/me/{order_id}/status`
- Eliminar: `DELETE /orders/me/{order_id}`

### VendorSettings

- Leer: `GET /settings/me`
- Crear/actualizar: `PUT /settings/me`

### WhatsAppConnection

- Crear/actualizar: `PUT /whatsapp/me`
- Leer: `GET /whatsapp/me`
- Verificar webhook: `GET /whatsapp/webhook`
- Recibir webhook: `POST /whatsapp/webhook`

### AuditLog

- Leer historial global: `GET /audit/logs`
- Leer historial por producto: `GET /audit/products/{product_id}/history`

### Recursos tecnicos sin CRUD de BD claro

- `GET /health`
- `POST /llm/test`
- `POST /retrieval/search`
- `POST /chat/me`
- `GET /dashboard/me`
- `POST /catalog/build-knowledge-base/me`
- `GET /catalog/knowledge-base/me`

## Que debes validar en CSV

### `endpoint_requests.csv`

- Que exista una fila por request.
- Que aparezcan `method`, `path`, `status_code` y `endpoint`.
- Que los errores tambien se registren.
- Que no se filtren secretos: `password`, `token`, `secret`, `authorization` deben quedar redaccionados.

### `crud_operations.csv`

- Que se registren `CREATE`, `READ`, `UPDATE` y `DELETE`.
- Que el campo `model` coincida con la entidad tocada.
- Que `payload_json` refleje el cambio o la consulta.
- Que los borrados queden con historico para auditoria.

## Secuencia recomendada de pruebas

1. `POST /auth/register`
2. `POST /auth/login`
3. `GET /auth/me`
4. `PATCH /empresa/me`
5. `POST /catalog/save/me`
6. `GET /catalog/products/me`
7. `GET /catalog/products/me/filter?category=shirts`
8. `GET /catalog/products/{product_id}`
9. `PATCH /catalog/products/{product_id}`
10. `DELETE /catalog/products/{product_id}`
11. `POST /orders/me`
12. `GET /orders/me`
13. `PATCH /orders/me/{order_id}/status`
14. `DELETE /orders/me/{order_id}`
15. `PUT /settings/me`
16. `PUT /whatsapp/me`
17. `GET /whatsapp/me`
18. `GET /audit/logs`
19. `GET /audit/products/{product_id}/history`
20. `GET /health`
21. `POST /llm/test`
22. `POST /retrieval/search`
23. `POST /chat/me`
24. `GET /dashboard/me`

## Criterio de aceptacion operativo

El sistema cumple esta verificacion si, al ejecutar la secuencia anterior:

- `endpoint_requests.csv` recibe una fila por cada request.
- `crud_operations.csv` recibe filas para todos los endpoints que hacen lectura o mutacion sobre SQLAlchemy.
- Las operaciones de eliminacion quedan representadas con trazabilidad historica.
- Los endpoints que no usan BD siguen dejando huella en `endpoint_requests.csv`.
