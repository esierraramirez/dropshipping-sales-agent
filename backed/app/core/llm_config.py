"""
Configuración optimizada de OpenAI para minimizar tokens y costos.

Estrategia de optimización:
1. Modelo: gpt-5.4-nano (más económico)
2. Razonamiento: "medium" (razonamiento balanceado, único soportado por gpt-5.3)
3. Verbosidad: "low" (respuestas concisas)
4. Max output: 300 tokens (respuestas limitadas)
5. Truncado de inputs: 1000 chars máximo
6. Context window: Solo información crítica de productos

Comparativa de costos (aproximada):
- gpt-5.4: $0.05 input / $0.20 output
- gpt-5.4-nano: $0.30 input / $1.20 output PER MILLION tokens
  → ~95% más barato que gpt-5.4 para este caso
"""

from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class ReasoningEffort(str, Enum):
    """Niveles de razonamiento del modelo.
    
    - medium: Razonamiento balanceado (SOPORTADO por gpt-5.3)
    """
    MEDIUM = "medium"


class Verbosity(str, Enum):
    """Nivel de detalle en respuestas.
    
    - medium: Respuestas balanceadas (único soportado por gpt-5.3)
    """
    MEDIUM = "medium"


class LLMConfig(BaseModel):
    """Configuración optimizada del LLM."""
    
    # Modelo a usar (nano es el más económico)
    model: str = "gpt-5.4-nano"
    
    # Parámetros de optimización
    reasoning_effort: ReasoningEffort = ReasoningEffort.MEDIUM
    verbosity: Verbosity = Verbosity.MEDIUM
    
    # Límites de tokens
    max_input_tokens: int = Field(default=1000, description="Máximo de tokens en entrada")
    max_output_tokens: int = Field(default=300, description="Máximo de tokens en salida (respuestas cortas)")
    max_input_chars: int = Field(default=3000, description="Máximo de caracteres en entrada (estimación de tokens)")
    
    # Parámetros de contexto
    product_context_lines: int = Field(default=10, description="Máximo de líneas de contexto de producto")
    retrieval_top_k: int = Field(default=2, description="Máximo de documentos a recuperar (vs 3)")
    
    # Control de temperatura
    temperature: Optional[float] = Field(default=None, description="Solo con reasoning=none")
    top_p: Optional[float] = Field(default=None, description="Solo con reasoning=none")


# Configuración por defecto: optimizada para chat economico
CHAT_OPTIMIZED_CONFIG = LLMConfig(
    model="gpt-5.4-nano",
    reasoning_effort=ReasoningEffort.MEDIUM,
    verbosity=Verbosity.MEDIUM,
    max_input_tokens=1000,
    max_output_tokens=300,
    product_context_lines=10,
    retrieval_top_k=2,
)

# Configuración para análisis más profundo (si es necesario)
ANALYSIS_CONFIG = LLMConfig(
    model="gpt-5.4-mini",  # Más potente pero sigue flexible
    reasoning_effort=ReasoningEffort.MEDIUM,
    verbosity=Verbosity.MEDIUM,
    max_input_tokens=2000,
    max_output_tokens=500,
    product_context_lines=15,
    retrieval_top_k=3,
)

# Configuración para uso agresivo (máximo ahorro)
AGGRESSIVE_COST_CONFIG = LLMConfig(
    model="gpt-5.4-nano",
    reasoning_effort=ReasoningEffort.MEDIUM,
    verbosity=Verbosity.MEDIUM,
    max_input_tokens=500,
    max_output_tokens=150,
    product_context_lines=5,
    retrieval_top_k=1,
)
