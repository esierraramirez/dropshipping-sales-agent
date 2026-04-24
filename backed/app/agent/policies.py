from datetime import datetime


def is_within_business_hours(start_hour: str | None, end_hour: str | None) -> bool:
    # Verifica si la hora actual está dentro del horario de atención configurado.
    if not start_hour or not end_hour:
        return True

    now = datetime.now().time()

    try:
        start_h, start_m = map(int, start_hour.split(":"))
        end_h, end_m = map(int, end_hour.split(":"))
    except Exception:
        return True

    start_time = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
    end_time = now.replace(hour=end_h, minute=end_m, second=0, microsecond=0)

    current = now
    return start_time <= current <= end_time


def resolve_tone_instruction(tone: str | None) -> str:
    # Convierte el tono configurado en una instrucción textual para el LLM.
    tone_map = {
        "formal": "Responde de manera formal, profesional y respetuosa.",
        "friendly": "Responde de manera cercana, amable y fácil de entender.",
        "sales": "Responde con un enfoque comercial, persuasivo y orientado a conversión.",
        "empathetic": "Responde de forma empática, amable, comprensiva y orientada a ayudar.",
    }

    return tone_map.get(
        tone or "friendly",
        "Responde de manera cordial, clara y útil."
    )
