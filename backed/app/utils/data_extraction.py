"""
Módulo para extraer información del cliente desde la conversación.
Extrae nombre, teléfono, dirección, productos seleccionados, etc.
"""

import re
from typing import Optional, List, Dict, Any


def extract_phone_number(text: str) -> Optional[str]:
    """
    Extrae número de teléfono del texto.
    Reconoce formatos comunes en Latinoamérica.
    """
    # Teléfono con +34, +56, +57, etc.
    patterns = [
        r'\+?[\d]{1,3}[\s.-]?[\d]{6,14}',  # Formato internacional
        r'[\s(](\d{3})[\s\-.]?(\d{3})[\s\-.]?(\d{4})',  # (123) 456-7890
        r'\d{10}',  # Número simple de 10 dígitos
        r'\d{7,14}',  # Números largos
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Extraer solo los dígitos
            phone = re.sub(r'[^\d+]', '', match.group(0))
            if len(phone) >= 7:  # Al menos 7 dígitos
                return phone
    
    return None


def extract_customer_name(text: str) -> Optional[str]:
    """
    Extrae el nombre del cliente del texto.
    Busca patrones como "me llamo", "soy", "mi nombre es".
    """
    patterns = [
        r"(?:me llamo|soy|mi nombre es)\s+([a-záéíóúñüA-ZÁÉÍÓÚÑÜ\s]+?)(?:[,.?!\n]|$)",
        r"(?:llamame|me llama|me puedes llamar)\s+([a-záéíóúñüA-ZÁÉÍÓÚÑÜ\s]+?)(?:[,.?!\n]|$)",
        r"(?:soy )?([a-záéíóúñüA-ZÁÉÍÓÚÑÜ]{3,})\s+(?:con quien hablas|quien soy)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Limpiar caracteres indeseados
            name = re.sub(r'[,.?!\n]', '', name).strip()
            if len(name) >= 2 and len(name.split()) <= 3:  # Entre 2 y 3 palabras
                return name
    
    return None


def extract_address(text: str) -> Optional[str]:
    """
    Extrae dirección del texto.
    Busca patrones comunes de direcciones.
    """
    patterns = [
        r"(?:dirección|envío a|vivo en|mi casa es|casa en|apartamento en|apto)\s+([^,.?!\n]+)",
        r"(?:calle|carrera|avenida|av\.?|cra\.?|cll\.?)\s+([^,.?!\n]+)",
        r"(?:barrio|zona|sector)\s+([^,.?!\n]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            address = match.group(1).strip()
            address = re.sub(r'[,?!\n]', '', address).strip()
            if len(address) >= 5:
                return address
    
    return None


def extract_product_mention(text: str, catalog_context: str = "") -> Optional[Dict[str, Any]]:
    """
    Extrae menciones de productos del texto.
    Busca nombres de productos del catálogo si está disponible.
    """
    # Esta es una función simplificada. En producción, usar búsqueda semántica.
    # Por ahora, detecta patrones comunes de interés en productos.
    
    patterns = [
        r"(?:quiero|me interesa|dame|dame uno de|necesito|búscame)\s+(?:un|una|unos|unas)?\s*([a-záéíóúñüA-ZÁÉÍÓÚÑÜ\s]+?)(?:\s+(?:en|de|color|talla|tamaño)|[,.?!\n]|$)",
        r"(?:ese|esa|esos|esas|el|la|los|las)\s+([a-záéíóúñüA-ZÁÉÍÓÚÑÜ\s]+?)(?:\s+(?:en|de|color|talla|tamaño)|[,.?!\n]|$)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            product_mention = match.group(1).strip()
            product_mention = re.sub(r'[,.?!\n]', '', product_mention).strip()
            
            if len(product_mention) >= 2 and len(product_mention) <= 100:
                return {
                    "mention": product_mention,
                    "quantity": extract_quantity(text) or 1,
                }
    
    return None


def extract_quantity(text: str) -> Optional[int]:
    """
    Extrae la cantidad mencionada.
    Busca números o palabras como 'dos', 'tres', etc.
    """
    # Patrones de números
    number_pattern = r"(?:quiero|dame|necesito|envía)\s+(\d+)\s+(?:de|un|una)"
    match = re.search(number_pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Palabras numéricas en español
    word_numbers = {
        "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    }
    
    for word, number in word_numbers.items():
        if re.search(rf"\b{word}\b", text, re.IGNORECASE):
            return number
    
    return None


def extract_confirmation_intent(text: str) -> bool:
    """
    Detecta si el cliente está confirmando la compra.
    Retorna True si hay intención clara de compra.
    """
    confirmation_keywords = [
        r"\b(?:si|dale|dale dale|ok|vale|perfecto|excelente|bueno|listo|procede|adelante|confirmo|confirmado)\b",
        r"\b(?:compralo|lo compro|me lo envies|enviamelo|hazme la orden|registra la orden|crea la orden)\b",
        r"\b(?:acepto|acepta|aceptado|de acuerdo|estoy de acuerdo|si señor|si señora)\b",
    ]
    
    text_lower = text.lower()
    for pattern in confirmation_keywords:
        if re.search(pattern, text_lower):
            return True
    
    return False


def extract_rejection_intent(text: str) -> bool:
    """
    Detecta si el cliente está rechazando la compra.
    Retorna True si hay intención clara de rechazo.
    """
    rejection_keywords = [
        r"\b(?:no|nope|nunca|jamás|de ninguna forma|para nada|negativo)\b",
        r"\b(?:no quiero|no necesito|no me interesa|no sirve|no vale|no me gusta|no es para mi)\b",
        r"\b(?:muy caro|demasiado caro|no tengo plata|sin dinero|estoy sin dinero)\b",
    ]
    
    text_lower = text.lower()
    for pattern in rejection_keywords:
        if re.search(pattern, text_lower):
            return True
    
    return False


def extract_question_intent(text: str) -> Optional[str]:
    """
    Detecta el tipo de pregunta que hace el cliente.
    Retorna el tipo: 'precio', 'disponibilidad', 'envio', 'caracteristicas', etc.
    """
    intent_patterns = {
        "precio": [r"\b(?:cuanto cuesta|precio|cuanto vale|valor|costo)\b"],
        "disponibilidad": [r"\b(?:hay|tienen|tienes|disponible|stock|en existencia)\b"],
        "envio": [r"\b(?:envio|envios|domicilio|entrega|a donde llega)\b"],
        "caracteristicas": [r"\b(?:color|colores|talla|tallas|tamaño|material|marca|descripcion)\b"],
        "tiempo": [r"\b(?:cuanto tiempo|demora|cuantos dias|cuando|entrega en)\b"],
    }
    
    text_lower = text.lower()
    for intent, patterns in intent_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return intent
    
    return None


def extract_previous_product_reference(
    conversation_history: List[Dict[str, str]],
    current_message: str
) -> Optional[str]:
    """
    Detecta si el cliente se refiere a un producto mencionado anteriormente.
    Por ejemplo: si antes habló de "jean mom" y dice "ese", retorna "jean mom".
    """
    # Palabras que indican referencia al anterior
    reference_keywords = [r"\b(?:ese|esa|esos|esas|el|la|los|las|uno de esos|una de esas|igual|similar)\b"]
    
    current_lower = current_message.lower()
    has_reference = any(re.search(kw, current_lower) for kw in reference_keywords)
    
    if not has_reference or not conversation_history:
        return None
    
    # Buscar productos mencionados en el historial
    for msg in reversed(conversation_history[-5:]):  # Últimos 5 mensajes
        if msg.get("role") == "assistant":
            content = msg.get("content", "").lower()
            # Buscar palabras que típicamente acompañan nombres de productos
            product_patterns = [
                r"tenemos\s+([a-záéíóúñ\s]+?)(?:\s+en|,|\.)",
                r"recomiendo\s+([a-záéíóúñ\s]+?)(?:\s+(?:en|de|color|talla)|,|\.)",
                r"este\s+([a-záéíóúñ\s]+?)(?:\s+(?:es|de|color)|,|\.)",
            ]
            
            for pattern in product_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
    
    return None


def update_purchase_context_from_message(
    purchase_context: Dict[str, Any],
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Actualiza el contexto de compra basado en el mensaje del usuario.
    Extrae nombre, teléfono, dirección y otras informaciones relevantes.
    """
    if not purchase_context:
        purchase_context = {}
    
    # Extraer nombre
    name = extract_customer_name(user_message)
    if name and not purchase_context.get("customer_name"):
        purchase_context["customer_name"] = name
    
    # Extraer teléfono
    phone = extract_phone_number(user_message)
    if phone and not purchase_context.get("customer_phone"):
        purchase_context["customer_phone"] = phone
    
    # Extraer dirección
    address = extract_address(user_message)
    if address and not purchase_context.get("customer_address"):
        purchase_context["customer_address"] = address
    
    # Detectar intención de compra
    if extract_confirmation_intent(user_message):
        purchase_context["is_confirmed"] = True
    
    # Detectar rechazo
    if extract_rejection_intent(user_message):
        purchase_context["is_rejected"] = True
    
    return purchase_context


def get_client_data_summary(purchase_context: Dict[str, Any]) -> str:
    """
    Genera un resumen de los datos del cliente para verificación.
    """
    summary_parts = []
    
    if purchase_context.get("customer_name"):
        summary_parts.append(f"Nombre: {purchase_context['customer_name']}")
    
    if purchase_context.get("customer_phone"):
        summary_parts.append(f"Teléfono: {purchase_context['customer_phone']}")
    
    if purchase_context.get("customer_address"):
        summary_parts.append(f"Dirección: {purchase_context['customer_address']}")
    
    if purchase_context.get("items"):
        items_summary = ", ".join([
            f"{item.get('quantity', 1)}x {item.get('product_name', 'Producto')}"
            for item in purchase_context["items"]
        ])
        summary_parts.append(f"Productos: {items_summary}")
    
    return " | ".join(summary_parts) if summary_parts else "Sin datos"
