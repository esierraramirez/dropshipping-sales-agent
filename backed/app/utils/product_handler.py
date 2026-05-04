"""
Módulo mejorado para captura de productos y variantes de la conversación.
Extrae el producto seleccionado y sus variantes (talla, color, etc).
"""

import re
from typing import Optional, Dict, List, Any


def extract_product_from_catalog_context(
    user_message: str,
    agent_last_response: str = "",
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Optional[Dict[str, Any]]:
    """
    Extrae el producto del contexto de la conversación.
    Busca en el último mensaje del agente el producto recomendado.
    """
    if not agent_last_response:
        return None
    
    # Patrones para extraer producto del mensaje del agente
    # Busca texto entre asteriscos: *Nombre del Producto*
    product_pattern = r"\*([^*]+)\*"
    product_matches = re.findall(product_pattern, agent_last_response)
    
    if not product_matches:
        return None
    
    # El primer match suele ser el nombre del producto
    product_name = product_matches[0].strip()
    
    # Extraer precio (formato: 159.900 COP o $159.900)
    price_pattern = r"(\d+[.,]\d{1,3})\s*(?:COP|pesos)?"
    price_match = re.search(price_pattern, agent_last_response)
    unit_price = 0.0
    
    if price_match:
        price_str = price_match.group(1).replace(".", "").replace(",", "")
        try:
            unit_price = float(price_str)
        except:
            unit_price = 0.0
    
    # Extraer variantes (talla, color, etc.)
    variants = extract_product_variants(user_message, agent_last_response)
    
    return {
        "product_name": product_name,
        "unit_price": unit_price,
        "quantity": 1,
        "variants": variants,
    }


def extract_product_variants(user_message: str, agent_context: str = "") -> Dict[str, str]:
    """
    Extrae las variantes del producto (talla, color, etc).
    Busca en el mensaje del usuario las especificaciones.
    """
    variants = {}
    
    # TALLA (numbers: 6, 8, 10, XS, S, M, L, XL, etc.)
    talla_patterns = [
        r"talla\s+([0-9XSMLxsml]+)",
        r"size\s+([0-9XSMLxsml]+)",
        r"(talla|size)?\s+([0-9]{1,2})(?:\s|$)",
        r"\b([0-9]{1,2})\b.*(?:talla|size)",
    ]
    
    for pattern in talla_patterns:
        match = re.search(pattern, user_message + " " + agent_context, re.IGNORECASE)
        if match:
            # Tomar el grupo que sea número/letra
            for group in match.groups():
                if group and any(c in "0123456789XSMLxsml" for c in group):
                    variants["talla"] = group.strip()
                    break
            if "talla" in variants:
                break
    
    # COLOR (palabras de color comunes)
    color_patterns = [
        r"color\s+([a-záéíóúñ]+)",
        r"([a-záéíóúñ]+)\s+(?:color|claro|oscuro|medio)",
        r"\b(azul|rojo|verde|negro|blanco|gris|marrón|rosa|amarillo|naranja|beige|morado|violeta|celeste|turquesa|dorado|plateado)\b",
    ]
    
    for pattern in color_patterns:
        match = re.search(pattern, user_message, re.IGNORECASE)
        if match:
            color = match.group(1) if match.lastindex else match.group(0)
            variants["color"] = color.strip().lower()
            break
    
    # CANTIDAD
    qty_patterns = [
        r"(\d+)\s+(?:de|unidades|piezas)",
        r"dame\s+(\d+)",
        r"quiero\s+(\d+)",
        r"cantidad\s+(\d+)",
    ]
    
    quantity = 1
    for pattern in qty_patterns:
        match = re.search(pattern, user_message, re.IGNORECASE)
        if match:
            try:
                quantity = int(match.group(1))
                variants["cantidad"] = quantity
            except:
                pass
            break
    
    # GÉNERO (si aplica)
    genero_patterns = [
        r"\b(para\s+hombres?|para\s+mujeres?|de\s+hombre|de\s+mujer|masculino|femenino|mujer|hombre)\b",
    ]
    
    for pattern in genero_patterns:
        match = re.search(pattern, user_message + " " + agent_context, re.IGNORECASE)
        if match:
            genero_text = match.group(1).lower()
            if "mujer" in genero_text or "femenino" in genero_text:
                variants["genero"] = "mujer"
            elif "hombre" in genero_text or "masculino" in genero_text:
                variants["genero"] = "hombre"
            break
    
    # MATERIAL (si aplica)
    material_patterns = [
        r"\b(algodón|denim|algodon|cuero|nylon|poliéster|lana|seda|lino|algodón|tela)\b",
    ]
    
    for pattern in material_patterns:
        match = re.search(pattern, user_message + " " + agent_context, re.IGNORECASE)
        if match:
            variants["material"] = match.group(1).lower()
            break
    
    return variants


def is_customer_confirming_product(text: str) -> bool:
    """
    Detecta si el cliente está confirmando que quiere el producto recomendado.
    """
    confirmation_patterns = [
        r"\b(?:si|dale|dale dale|ok|vale|perfecto|excelente|bueno|listo|me gusta|me encanta)\b",
        r"\b(?:lo quiero|quiero ese|quiero esa|quiero ese jean|quiero esa camisa)\b",
        r"\b(?:confirmó|confirmado|de acuerdo|estoy de acuerdo|adelante)\b",
        r"\b(?:porfa|envíamelo|envía|manda|házmelo)\b",
        r"^(si|dale|ok|listo|perfecto)$",
    ]
    
    text_lower = text.lower().strip()
    for pattern in confirmation_patterns:
        if re.search(pattern, text_lower):
            return True
    
    return False


def is_customer_selecting_variant(text: str, agent_context: str = "") -> bool:
    """
    Detecta si el cliente está especificando variantes (talla, color, etc).
    """
    variant_keywords = [
        r"talla\s+",
        r"size\s+",
        r"color\s+",
        r"\b(azul|rojo|verde|negro|blanco|gris|marrón|rosa|amarillo|naranja|beige)\b",
        r"\b([0-9XSMLxsml]+)\b",  # Números o tallas
        r"(?:para|de)\s+(?:hombre|mujer)",
    ]
    
    text_combined = text.lower() + " " + agent_context.lower()
    for pattern in variant_keywords:
        if re.search(pattern, text_combined):
            return True
    
    return False


def build_product_summary(product: Dict[str, Any]) -> str:
    """
    Construye un resumen del producto con variantes.
    Ej: "Jean Recto Azul Central (Talla 6, Color Azul Central)"
    """
    name = product.get("product_name", "Producto")
    variants = product.get("variants", {})
    
    variant_parts = []
    if variants.get("talla"):
        variant_parts.append(f"Talla {variants['talla']}")
    if variants.get("color"):
        variant_parts.append(f"Color {variants['color'].title()}")
    if variants.get("genero"):
        variant_parts.append(f"{variants['genero'].title()}")
    
    if variant_parts:
        return f"{name} ({', '.join(variant_parts)})"
    return name


def extract_all_required_data(
    purchase_context: Dict[str, Any],
    agent_last_response: str = ""
) -> Dict[str, Any]:
    """
    Verifica si están todos los datos requeridos para crear la orden.
    Retorna dict con estado y datos faltantes.
    """
    required_data = {
        "customer_name": purchase_context.get("customer_name"),
        "customer_phone": purchase_context.get("customer_phone"),
        "customer_address": purchase_context.get("customer_address"),
        "items": purchase_context.get("items", []),
    }
    
    missing_data = []
    
    if not required_data["customer_name"]:
        missing_data.append("nombre")
    if not required_data["customer_phone"]:
        missing_data.append("teléfono")
    if not required_data["customer_address"]:
        missing_data.append("dirección")
    if not required_data["items"] or len(required_data["items"]) == 0:
        missing_data.append("producto")
    
    return {
        "complete": len(missing_data) == 0,
        "required_data": required_data,
        "missing_data": missing_data,
    }


def should_create_order(
    user_message: str,
    purchase_context: Dict[str, Any],
    agent_response: str = ""
) -> bool:
    """
    Determina si se debe crear la orden.
    Requisitos:
    1. Todos los datos presentes (nombre, teléfono, dirección, producto)
    2. Cliente confirmó la compra (explícitamente)
    3. Agente está respondiendo con "registré" o similar
    """
    # Verificar datos completos
    data_check = extract_all_required_data(purchase_context, agent_response)
    if not data_check["complete"]:
        return False
    
    # Verificar confirmación explícita
    if not purchase_context.get("is_confirmed"):
        return False
    
    # Verificar que agente está confirmando (no el usuario)
    if "registr" not in agent_response.lower():
        return False
    
    return True


def validate_product_specification(
    user_message: str,
    agent_context: str,
    product_variants: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Valida que el cliente haya especificado suficientemente el producto.
    Retorna si hay variantes faltantes que preguntar.
    """
    result = {
        "is_complete": True,
        "missing_variants": [],
        "message": ""
    }
    
    # Detectar si hay variantes en el contexto que NO se especificaron
    # (e.g., si el catálogo muestra "talla 6, 8, 10" pero el cliente no especificó)
    
    # Buscar variantes disponibles en contexto del agente
    available_variants = {
        "talla": r"talla.*\(" in agent_context,
        "color": r"color" in agent_context.lower(),
        "genero": r"(?:hombre|mujer)" in agent_context.lower(),
    }
    
    specified_variants = product_variants
    
    for variant_type, is_available in available_variants.items():
        if is_available and variant_type not in specified_variants:
            result["is_complete"] = False
            result["missing_variants"].append(variant_type)
    
    if not result["is_complete"]:
        missing_str = ", ".join(result["missing_variants"])
        result["message"] = f"Por favor especifica: {missing_str}"
    
    return result
