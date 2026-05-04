from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
import json
import re
import unicodedata

from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.services.retrieval_service import retrieve_vendor_context, build_context_block
from app.services.order_service import create_order_from_chat
from app.agent.policies import is_within_business_hours, resolve_tone_instruction
from app.agent.prompts import build_sales_agent_system_prompt
from app.schemas.chat_schema import PurchaseContext, CartItem
from app.utils.gender_detection import detect_gender_by_name, infer_gender_from_conversation
from app.utils.data_extraction import (
    extract_customer_name, extract_phone_number, extract_address,
    extract_confirmation_intent, extract_rejection_intent,
    update_purchase_context_from_message, get_client_data_summary
)
from app.utils.product_handler import (
    extract_product_from_catalog_context, extract_product_variants,
    is_customer_confirming_product, is_customer_selecting_variant,
    build_product_summary, extract_all_required_data, should_create_order
)


NO_KNOWLEDGE_REPLY = (
    "Por ahora no tengo esa informacion disponible en el catalogo. "
    "Si quieres, puedo ayudarte con los productos y datos que tengo registrados."
)


def _build_out_of_catalog_reply(user_message: str, vendor_name: str) -> str:
    """
    Mejora la respuesta cuando el usuario pregunta por algo no en el catálogo.
    Extrae lo que buscaba y sugiere alternativas.
    """
    # Extraer lo que el usuario buscaba
    normalized = _normalize_text(user_message)
    
    # Palabras clave para identificar qué busca
    if "ling" in normalized or "linga" in normalized or "lenceria" in normalized:
        searched_item = "lenceria"
        alternatives = "productos basicos, prendas de uso diario o accesorios"
    elif "zapat" in normalized or "zapato" in normalized:
        searched_item = "zapatos"
        alternatives = "prendas de vestir, accesorios o productos complementarios"
    elif "bolsa" in normalized or "bolso" in normalized:
        searched_item = "bolsas"
        alternatives = "accesorios, billeteras o productos de complemento"
    elif "sombrero" in normalized or "gorro" in normalized or "sombrilla" in normalized:
        searched_item = "sombreros o gorros"
        alternatives = "accesorios complementarios o prendas de vestir"
    elif "reloj" in normalized:
        searched_item = "relojes"
        alternatives = "accesorios, joyeria o prendas complementarias"
    else:
        # Respuesta genérica si no identificamos bien qué busca
        return (
            f"Entiendo que buscas algo específico, pero en este momento {vendor_name} "
            "no tiene disponible. Sin embargo, te puedo mostrar opciones similares o complementarias. "
            "¿Prefieres ver categorias disponibles o productos recomendados?"
        )
    
    return (
        f"No encontramos {searched_item} en el catálogo de {vendor_name} en este momento. "
        f"Sin embargo, contamos con excelentes opciones en otras categorias como {alternatives}. "
        "¿Te gustaría explorar alguna de estas opciones?"
    )


def _is_simple_greeting(text: str) -> bool:
    normalized = _normalize_text(text)
    greeting_words = {
        "hola",
        "buenas",
        "buen",
        "dia",
        "dias",
        "tarde",
        "tardes",
        "noche",
        "noches",
        "hey",
        "hello",
        "saludos",
    }
    words = normalized.split()
    
    # Si está vacío, no es saludo
    if not words:
        return False
    
    # Si la PRIMERA palabra es un saludo, considéralo como saludo simple
    # Ignora ruido adicional como "(var1)" que deja "var" o "varX"
    first_word = words[0]
    
    # Verifica si la primera palabra es un saludo o si TODAS las palabras son saludos
    # (para casos como "hola buenas" o "buenos dias")
    if first_word in greeting_words:
        return True
    
    # O si todas las palabras son saludos válidos
    return bool(words) and all(word in greeting_words for word in words)


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _is_catalog_or_sales_query(text: str) -> bool:
    normalized_words = set(_normalize_text(text).split())
    
    # Términos generales de catálogo
    catalog_terms = {
        "catalogo",
        "menu",
        "producto",
        "productos",
        "precio",
        "precios",
        "cuesta",
        "vale",
        "valor",
        "disponible",
        "disponibilidad",
        "stock",
        "tienen",
        "tienes",
        "hay",
        "busco",
        "quiero",
        "necesito",
        "manejan",
        "manejamos",
        "muestrame",
        "mostrar",
        "venden",
        "vendes",
        "recomiendas",
        "recomiendame",
        "comprar",
        "compra",
        "pedido",
        "orden",
        "talla",
        "tallas",
        "color",
        "colores",
        "envio",
        "envios",
        "domicilio",
        "garantia",
        "devolucion",
        "cambio",
        "pagar",
        "pago",
        "interesado",
        "interesada",
        "interes",
        "me",
        # Palabras específicas de productos
        "camisa",
        "camisas",
        "jean",
        "jeans",
        "pantalon",
        "pantalones",
        "vestido",
        "vestidos",
        "falda",
        "faldas",
        "blusa",
        "blusas",
        "playera",
        "playeras",
        "sueter",
        "abrigo",
        "abrigos",
        "chaqueta",
        "chaquetas",
        "zapato",
        "zapatos",
        "tenis",
        "ropa",
        "prenda",
        "prendas",
        "outfit",
        "traje",
        "trajes",
        "sweater",
        "hoodie",
        "corbata",
    }
    return bool(normalized_words & catalog_terms)


def _build_general_reply(vendor_name: str, user_message: str) -> str:
    normalized = _normalize_text(user_message)
    if normalized in {"gracias", "muchas gracias", "ok gracias", "listo gracias"}:
        return "¡Con mucho gusto! Estoy aquí para ayudarte cuando lo necesites."

    if normalized in {"como estas", "que tal", "como vas"}:
        return f"¡Muy bien, gracias por preguntar! Aquí estoy para ayudarte con {vendor_name}."

    if normalized in {"ok", "listo", "perfecto", "vale", "bueno"}:
        return "Perfecto. Quedo atento a lo que necesites."

    return "Claro. Estoy aquí para ayudarte. Cuéntame qué estás buscando o qué necesitas saber."


def _extract_identity(text: str) -> tuple[str | None, str | None]:
    normalized = _normalize_text(text)
    gender = None
    if re.search(r"\b(hombre|masculino|varon)\b", normalized):
        gender = "masculino"
    elif re.search(r"\b(mujer|femenino)\b", normalized):
        gender = "femenino"

    name = None
    match = re.search(
        r"\b(?:soy|me llamo|mi nombre es)\s+([a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)",
        text,
        flags=re.IGNORECASE,
    )
    if match:
        candidate = match.group(1).strip(" ,.;:")
        if _normalize_text(candidate) not in {"hombre", "mujer", "masculino", "femenino"}:
            name = candidate[:1].upper() + candidate[1:]

    return name, gender


def _extract_gender_preference(text: str) -> str | None:
    normalized = _normalize_text(text)

    masculine_patterns = [
        r"\btrata(?:me)?\s+en\s+masculino\b",
        r"\bhablame\s+en\s+masculino\b",
        r"\bsoy\s+hombre\b",
        r"\bmasculino\b",
        r"\bvaron\b",
    ]
    feminine_patterns = [
        r"\btrata(?:me)?\s+en\s+femenino\b",
        r"\bhablame\s+en\s+femenino\b",
        r"\bsoy\s+mujer\b",
        r"\bfemenino\b",
    ]

    if any(re.search(pattern, normalized) for pattern in masculine_patterns):
        return "masculino"
    if any(re.search(pattern, normalized) for pattern in feminine_patterns):
        return "femenino"
    return None


def _infer_gender_preference(
    user_message: str,
    conversation_history: Optional[List[dict]] = None,
) -> str | None:
    current = _extract_gender_preference(user_message)
    if current:
        return current

    # Intentar detectar el género del nombre del cliente
    name = extract_customer_name(user_message)
    if name:
        gender_by_name = detect_gender_by_name(name)
        if gender_by_name:
            return gender_by_name

    # Buscar en el historial
    if conversation_history:
        for message in reversed(conversation_history):
            if message.get("role") != "user":
                continue
            content = str(message.get("content", ""))
            
            # Buscar preferencia explícita
            detected = _extract_gender_preference(content)
            if detected:
                return detected
            
            # Buscar nombre en el historial
            name_in_history = extract_customer_name(content)
            if name_in_history:
                gender_by_name = detect_gender_by_name(name_in_history)
                if gender_by_name:
                    return gender_by_name
        
        # Usar función de inferencia del módulo de detección
        return infer_gender_from_conversation(conversation_history)

    return None


def _build_identity_reply(vendor_name: str, name: str | None, gender: str | None) -> str:
    if name and gender:
        suffix = "listo" if gender == "masculino" else "lista"
        return f"¡Mucho gusto, {name}! Perfecto, te trataré en {gender}. Ya estoy {suffix} para ayudarte con {vendor_name}."
    if name:
        return f"¡Mucho gusto, {name}! ¿Prefieres que te trate en masculino o femenino?"
    if gender:
        suffix = "claro" if gender == "masculino" else "clara"
        return f"Perfecto, lo tengo presente. Para atenderte mejor, ¿me regalas tu nombre?"
    return "Perfecto. ¿Me regalas tu nombre y me dices si prefieres que te trate en masculino o femenino?"


def _is_general_social_message(text: str) -> bool:
    normalized = _normalize_text(text)
    social_phrases = {
        "gracias",
        "muchas gracias",
        "ok gracias",
        "listo gracias",
        "como estas",
        "que tal",
        "como vas",
        "ok",
        "listo",
        "perfecto",
        "vale",
        "bueno",
    }
    # Verificar si es exactamente una frase social
    if normalized in social_phrases:
        return True
    
    # O si la primera palabra es una frase social comun (para ignorar ruido como "(var1)")
    words = normalized.split()
    if words and words[0] in social_phrases:
        return True
    
    return False


def _build_welcome_reply(vendor_name: str) -> str:
    return (
        f"¡Hola! Soy el asistente de {vendor_name}. "
        "Qué gusto atenderte. ¿Me regalas tu nombre y me dices si prefieres que te trate en masculino o femenino? "
        "Así puedo ayudarte de forma más cercana."
    )


def get_vendor_settings(db: Session, vendor_id: int) -> VendorSettings | None:
    # Obtiene la configuración del vendor (horarios, tono, habilitación).
    return db.query(VendorSettings).filter(VendorSettings.vendor_id == vendor_id).first()


def _build_enhanced_query(user_message: str, history: Optional[List[dict]] = None) -> str:
    # Mejora la búsqueda semántica agregando contexto del historial conversacional.
    if not history or len(history) == 0:
        return user_message
    
    # Extrae el último mensaje del agente para contexto
    # Esto ayuda a mantener el tema de conversación
    context_parts = [user_message]
    
    for msg in reversed(history[-4:]):  # Toma últimos 4 mensajes
        if msg.get("role") == "user":
            context_parts.insert(0, msg.get("content", ""))
            break  # Solo el último mensaje del usuario anterior
    
    # Combina para crear una query más contextual
    return " ".join(context_parts)


def _detect_purchase_keywords(text: str) -> bool:
    # Detecta palabras clave de intención de compra (DEPRECADA - no se usa).
    purchase_keywords = [
        r"\bquiero\b",
        r"\bme interesa\b",
        r"\bme lo envíen\b",
        r"\bacéptalo\b",
        r"\bconfirmo\b",
        r"\bcuánto cuesta\b",
        r"\bcómo pago\b",
        r"\bde acuerdo\b",
        r"\bsí, dale\b",
        r"\bperfecto\b",
        r"\besto es\b",
        r"\bfinalizar\b",
        r"\bcomprar\b",
    ]
    
    text_lower = text.lower()
    for keyword in purchase_keywords:
        if re.search(keyword, text_lower):
            return True
    return False


def _strip_repeated_intro(reply: str) -> str:
    intro_patterns = [
        r"^\s*[¡!]?hola[!¡,. ]*\s*",
        r"^\s*soy el asistente(?: virtual)?(?: de [^.?!\n]+)?[.?!]?\s*",
        r"^\s*[¿?¡!]*en qu[eé] puedo ayudarte hoy[?¿!¡]*\s*[,.;:-]?\s*",
    ]

    cleaned = reply
    previous = None
    while previous != cleaned:
        previous = cleaned
        for pattern in intro_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip() or reply


def _create_order_from_response(
    db: Session,
    vendor: Vendor,
    agent_response: str,
    purchase_context: Optional[PurchaseContext]
) -> Optional[dict]:
    """
    Crea una orden cuando el agente confirma la venta.
    Requisitos mínimos: nombre + teléfono + producto (dirección opcional)
    """
    if not purchase_context:
        print("  └─ No hay purchase_context")
        return None
    
    # Verifica que tenga datos mínimos del cliente
    if not purchase_context.customer_name:
        print(f"  └─ Sin nombre del cliente")
        return None
    
    if not purchase_context.customer_phone:
        print(f"  └─ Sin telefono del cliente")
        return None
    
    # Verifica que tenga al menos un producto
    if not purchase_context.items or len(purchase_context.items) == 0:
        print(f"  └─ Sin productos en la orden")
        return None
    
    # Si el flujo ya viene confirmado en contexto, crea la orden de forma determinista
    if purchase_context.is_confirmed:
        print("  └─ purchase_context.is_confirmed=True, creando orden")
        found_confirmation = True
    else:
        # Verifica que el agente haya confirmado la orden
        confirm_keywords = [
            "registré tu orden",
            "registrar tu orden",
            "orden registrada",
            "hemos registrado",
            "quedó registrada",
            "tu orden quedó lista",
            "orden lista",
            "pedido confirmado",
            "pedido registrado",
            "confirmo tu orden",
            "orden confirmada",
            "compra confirmada",
            "gracias por tu compra",
            "dejamos tu orden",
        ]
        
        response_lower = agent_response.lower()
        found_confirmation = any(kw in response_lower for kw in confirm_keywords)
        
        if found_confirmation:
            print(f"  └─ Agente confirmo la orden (contiene 'registr' o similar)")
        else:
            print(f"  └─ Agente NO confirmo explicitamente la orden")
            # Aun asi, si tiene todos los datos y el cliente confirmo, crear
            if not purchase_context.is_confirmed:
                print(f"  └─ Cliente tampoco confirmo, cancelando creacion")
                return None
    
    # Preparar items
    items_data = []
    
    if purchase_context.items and len(purchase_context.items) > 0:
        for item in purchase_context.items:
            item_dict = {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            items_data.append(item_dict)
    else:
        print(f"  └─ No hay items, creando generico")
        return None
    
    # Crear la orden
    try:
        try:
            print(f"  └─ Creando orden:")
            print(f"     • Cliente: {purchase_context.customer_name}")
            print(f"     • Telefono: {purchase_context.customer_phone}")
            print(f"     • Direccion: {purchase_context.customer_address or '(sin especificar)'}")
            print(f"     • Items: {len(items_data)}")
        except:
            pass  # Ignorar errores de encoding en prints
        
        order = create_order_from_chat(
            db=db,
            vendor=vendor,
            customer_name=purchase_context.customer_name,
            customer_phone=purchase_context.customer_phone,
            customer_address=purchase_context.customer_address or "",
            items=items_data,
            conversation_summary="Orden creada desde chat del agente"
        )
        
        try:
            print(f"  └─ [OK] Orden creada exitosamente, ID: {order.get('id')}")
        except:
            pass
        return order
    except Exception as e:
        try:
            print(f"  └─ [ERROR] Error al crear orden: {str(e)}")
        except:
            pass
        import traceback
        traceback.print_exc()
        return None


def generate_agent_reply(
    db: Session,
    vendor: Vendor,
    user_message: str,
    conversation_history: Optional[List[dict]] = None,
    purchase_context: Optional[dict] = None,
    top_k: int = 3
) -> dict:
    # Orquesta el flujo: carga settings → verifica horario → busca contexto → LLM → crea orden si aplica.
    settings = get_vendor_settings(db=db, vendor_id=vendor.id)

    # Configuración por defecto si no existe
    agent_enabled = True
    business_start_hour = None
    business_end_hour = None
    off_hours_message = (
        "Hola, en este momento estamos fuera de horario de atención. "
        "Déjanos tu mensaje y te responderemos pronto."
    )
    tone = "friendly"

    if settings:
        agent_enabled = settings.agent_enabled
        business_start_hour = settings.business_start_hour
        business_end_hour = settings.business_end_hour
        off_hours_message = settings.off_hours_message or off_hours_message
        tone = settings.tone or tone

    if not agent_enabled:
        raise HTTPException(status_code=403, detail="El agente de esta empresa está desactivado.")

    # === ACTUALIZAR PURCHASE_CONTEXT CON DATOS DEL MENSAJE ===
    if not purchase_context:
        purchase_context = {}
    
    try:
        purchase_context = update_purchase_context_from_message(
            purchase_context=purchase_context,
            user_message=user_message,
            conversation_history=conversation_history
        )
    except Exception as e:
        try:
            print(f"WARNING: Error al actualizar purchase_context: {str(e)}")
        except:
            pass
        import traceback
        traceback.print_exc()

    if _is_simple_greeting(user_message):
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": _build_welcome_reply(vendor.name),
            "context_used": "Saludo inicial. No se utilizó contexto del catálogo.",
            "matches_found": 0,
            "purchase_context": purchase_context,
        }

    name, gender = _extract_identity(user_message)
    if name or gender:
        # Actualizar el contexto con nombre si se encuentra
        if name and not purchase_context.get("customer_name"):
            purchase_context["customer_name"] = name
        
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": _build_identity_reply(vendor.name, name, gender),
            "context_used": "Datos de trato del cliente. No se utilizó contexto del catálogo.",
            "matches_found": 0,
            "purchase_context": purchase_context,
        }

    confirmation_intent = extract_confirmation_intent(user_message)
    if _is_general_social_message(user_message) and not confirmation_intent:
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": _build_general_reply(vendor.name, user_message),
            "context_used": "Conversación general. No se utilizó contexto del catálogo.",
            "matches_found": 0,
            "purchase_context": purchase_context,
        }

    if not is_within_business_hours(business_start_hour, business_end_hour):
        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": off_hours_message,
            "context_used": "Fuera de horario. No se utilizó contexto del catálogo.",
            "matches_found": 0,
            "purchase_context": purchase_context,
        }

    # Mejora la query si hay historial para mejor contexto
    enhanced_query = _build_enhanced_query(user_message, conversation_history)

    retrieval_result = retrieve_vendor_context(
        vendor=vendor,
        query=enhanced_query,
        top_k=top_k
    )

    results = retrieval_result["results"]
    if not retrieval_result.get("knowledge_base_ready") or not results:
        if not _is_catalog_or_sales_query(user_message):
            return {
                "vendor_name": vendor.name,
                "user_message": user_message,
                "agent_response": _build_general_reply(vendor.name, user_message),
                "context_used": "Conversación general. No se utilizó contexto del catálogo.",
                "matches_found": 0,
                "purchase_context": purchase_context,
            }

        return {
            "vendor_name": vendor.name,
            "user_message": user_message,
            "agent_response": _build_out_of_catalog_reply(user_message, vendor.name),
            "context_used": "No se encontraron datos relevantes en la base de conocimiento.",
            "matches_found": 0,
            "purchase_context": purchase_context,
        }

    context_block = build_context_block(results)
    if vendor.payment_methods:
        context_block = (
            f"{context_block}\n\n"
            "[Información de la empresa]\n"
            f"Medios de pago disponibles: {vendor.payment_methods}"
        )
    tone_instruction = resolve_tone_instruction(tone)
    gender_preference = _infer_gender_preference(user_message, conversation_history)
    customer_profile_instruction = ""
    if gender_preference == "masculino":
        customer_profile_instruction = (
            "Preferencia de cliente detectada: masculino. "
            "Si recomiendas productos, prioriza opciones de hombre/masculino cuando esa distincion exista en la base de conocimiento. "
            "Si no hay productos masculinos claros en el contexto, dilo de forma transparente y ofrece alternativas neutras del catalogo."
        )
    elif gender_preference == "femenino":
        customer_profile_instruction = (
            "Preferencia de cliente detectada: femenino. "
            "Si recomiendas productos, prioriza opciones de mujer/femenino cuando esa distincion exista en la base de conocimiento. "
            "Si no hay productos femeninos claros en el contexto, dilo de forma transparente y ofrece alternativas neutras del catalogo."
        )

    system_prompt = build_sales_agent_system_prompt(
        vendor_name=vendor.name,
        tone_instruction=tone_instruction,
        context_block=context_block,
        customer_profile_instruction=customer_profile_instruction,
    )

    adapter = OpenAIAdapter()
    agent_reply = adapter.generate_reply(
        system_prompt=system_prompt,
        user_message=user_message
    )
    agent_reply = _strip_repeated_intro(agent_reply)

    # === EXTRAER Y ACTUALIZAR PRODUCTO DESDE LA CONVERSACIÓN ===
    try:
        # Si el cliente está confirmando o especificando un producto
        if is_customer_confirming_product(user_message) or is_customer_selecting_variant(user_message, agent_reply):
            # Extraer el producto del último mensaje del agente (contexto de la recomendación)
            last_agent_msg = ""
            if conversation_history:
                for msg in reversed(conversation_history[-2:]):
                    if msg.get("role") == "assistant":
                        last_agent_msg = msg.get("content", "")
                        break
            
            # Si no hay historial, usar el contexto del catálogo
            if not last_agent_msg:
                last_agent_msg = context_block
            
            # Extraer producto
            product = extract_product_from_catalog_context(
                user_message=user_message,
                agent_last_response=last_agent_msg,
                conversation_history=conversation_history
            )
            
            if product and product.get("product_name"):
                try:
                    print(f"[PRODUCTO] Detectado: {build_product_summary(product)}")
                except:
                    pass
                
                # Actualizar items en purchase_context
                if not purchase_context.get("items"):
                    purchase_context["items"] = []
            
            # Si es una actualización de cantidad/variante del mismo producto
            existing_item = None
            if product and len(purchase_context["items"]) > 0:
                last_item = purchase_context["items"][-1]
                # Si el nombre es muy similar, actualizar en lugar de crear nuevo
                if last_item.get("product_name", "").lower() in product.get("product_name", "").lower():
                    existing_item = last_item
            
            if existing_item and product:
                # Actualizar variantes
                existing_item["variants"] = {**existing_item.get("variants", {}), **product.get("variants", {})}
                try:
                    print(f"   └─ Variantes actualizadas: {existing_item.get('variants')}")
                except:
                    pass
            elif product:
                # Crear nuevo item con product_id basado en nombre
                new_item = {
                    "product_id": re.sub(r"[^a-z0-9]", "_", product.get("product_name", "").lower()),
                    "product_name": product.get("product_name"),
                    "quantity": product.get("quantity", 1),
                    "unit_price": product.get("unit_price", 0),
                    "variants": product.get("variants", {}),
                }
                purchase_context["items"].append(new_item)
                try:
                    print(f"   └─ Producto agregado a carrito")
                except:
                    pass
                
                # Actualizar total
                if purchase_context.get("items"):
                    total = sum(item.get("quantity", 1) * item.get("unit_price", 0) 
                               for item in purchase_context["items"])
                    purchase_context["total_amount"] = total
    except Exception as e:
        print(f"[WARNING] Error al extraer producto: {str(e)}")
        import traceback
        traceback.print_exc()

    # Convertir purchase_context a objeto si viene como dict
    pc_obj = None
    if purchase_context:
        try:
            pc_obj = PurchaseContext(**purchase_context)
        except Exception as e:
            print(f"Error al convertir purchase_context: {e}")
            pc_obj = None

    # Crear orden si es apropiado
    order_created = None
    if pc_obj:
        print(f"[ORDEN] Verificando creación de orden:")
        print(f"   - Datos del cliente: {get_client_data_summary(purchase_context)}")
        print(f"   - Confirmado: {pc_obj.is_confirmed}")
        print(f"   - Agent respuesta contiene confirmación: {'registr' in agent_reply.lower()}")
        
        # Intenta crear orden si el agente confirmó
        order_created = _create_order_from_response(db, vendor, agent_reply, pc_obj)
        
        if order_created:
            print(f"[OK] Orden creada: {order_created}")
        else:
            print(f"[ERROR] No se pudo crear orden")

    response = {
        "vendor_name": vendor.name,
        "user_message": user_message,
        "agent_response": agent_reply,
        "context_used": context_block,
        "matches_found": len(results),
    }
    
    if order_created:
        response["order_created"] = order_created
    
    # Retorna el contexto de compra actualizado
    if pc_obj:
        response["purchase_context"] = pc_obj.model_dump()
    else:
        response["purchase_context"] = purchase_context
    
    return response
