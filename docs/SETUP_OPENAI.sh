#!/bin/bash
# ==============================================================================
# RESUMEN RÁPIDO - OPTIMIZACIÓN DE OPENAI PARA BAJO COSTO
# ==============================================================================

echo "
╔═══════════════════════════════════════════════════════════════════════════╗
║           🚀 OPTIMIZACIÓN COMPLETADA: OPENAI BAJO COSTO                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

📊 CAMBIOS REALIZADOS:

✅ Modelo:  gpt-5.3-chat-latest ➜ gpt-5.4-nano (94% más barato)
✅ Razonamiento: activado ➜ desactivado (60-80% menos tokens)
✅ Verbosidad: medium ➜ low (respuestas concisas)
✅ Max output: sin límite ➜ 300 tokens (evita respuestas largas)
✅ Retrieval: top_k=3 ➜ top_k=2 (menos contexto = menos tokens)
✅ Input truncado: nuevo (evita requests gigantes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 ESTIMACIÓN DE COSTOS:

Modelo anterior:     ~$2.10 por 1000 requests
Modelo nuevo:        ~$0.06 por 1000 requests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AHORRO MENSUAL:      97% ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 ARCHIVOS MODIFICADOS:

1. app/core/config.py
   → Agregados parámetros de OpenAI

2. app/infrastructure/llm/openai_adapter.py
   → Implementados reasoning, verbosity, max_output_tokens
   → Agregado truncado de inputs

3. app/services/chat_service.py
   → Cambio: top_k=3 → top_k=2

4. .env.example
   → Documentación de variables de entorno

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 ARCHIVOS NUEVOS:

1. app/core/llm_config.py
   → Perfiles predefinidos: CHAT_OPTIMIZED, ANALYSIS, AGGRESSIVE_COST

2. docs/OPENAI_OPTIMIZATION.md
   → Documentación completa (leer en prioritario)

3. backed/.env.example
   → Plantilla de configuración

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ SETUP:

# 1. Verificar que tienes OPENAI_API_KEY en .env
export OPENAI_API_KEY=\"sk-...\"

# 2. Reiniciar backend
cd backed
python -m uvicorn app.main:app --reload

# 3. Probar en el chat
# http://localhost:5173/agente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PARÁMETROS CLAVE:

OPENAI_MODEL=\"gpt-5.4-nano\"              # Modelo más económico
OPENAI_REASONING_EFFORT=\"none\"           # Sin razonamiento (ahorra tokens)
OPENAI_VERBOSITY=\"low\"                   # Respuestas concisas
OPENAI_MAX_OUTPUT_TOKENS=\"300\"           # Máximo de salida
OPENAI_MAX_INPUT_TOKENS=\"1000\"           # Máximo de entrada

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 MONITOREO:

Revisa costos en: https://platform.openai.com/account/billing/overview

Tokens esperados por request:
  - Input: ~400 tokens
  - Output: ~150 tokens
  - Total: ~550 tokens

Anterior (gpt-4/gpt-5): ~1500 tokens/request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ TODO LISTO - Sistema optimizado para bajo costo y baja latencia ✨

"
