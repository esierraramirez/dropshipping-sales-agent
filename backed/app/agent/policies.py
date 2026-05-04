from datetime import datetime
import pytz


def is_within_business_hours(start_hour: str | None, end_hour: str | None, timezone: str = "America/Bogota") -> bool:
    """
    Verifica si la hora actual está dentro del horario de atención configurado.
    
    Args:
        start_hour: Hora de inicio en formato "HH:MM" (e.g., "08:00")
        end_hour: Hora de fin en formato "HH:MM" (e.g., "18:00")
        timezone: Zona horaria para calcular la hora actual (default: Bogotá)
    
    Returns:
        True si está dentro del horario, False si está fuera o no hay horario configurado
    """
    if not start_hour or not end_hour:
        return True  # Si no hay horario configurado, sempre está disponible
    
    try:
        # Obtener hora actual en la zona horaria especificada
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).time()
        
        # Parsear horas
        start_h, start_m = map(int, start_hour.split(":"))
        end_h, end_m = map(int, end_hour.split(":"))
        
        # Crear objetos de tiempo
        start_time = datetime.min.time().replace(hour=start_h, minute=start_m, second=0, microsecond=0)
        end_time = datetime.min.time().replace(hour=end_h, minute=end_m, second=0, microsecond=0)
        
        # Comparar (considerando casos donde end_time < start_time, e.g., 22:00-06:00)
        if start_time <= end_time:
            # Horario normal (e.g., 08:00-18:00)
            return start_time <= now <= end_time
        else:
            # Horario que cruza medianoche (e.g., 22:00-06:00)
            return now >= start_time or now <= end_time
    
    except Exception as e:
        print(f"Error al validar horario: {e}")
        return True  # Por seguridad, si hay error, permitir


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
