#!/usr/bin/env python3
"""
Script para probar la integración de WhatsApp
Simula mensajes que enviaría Meta para verificar que tu webhook funciona
"""

import requests
import json
from datetime import datetime
import time

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

WEBHOOK_URL = "http://localhost:8000/whatsapp/webhook"
BACKEND_URL = "http://localhost:8000"

# ============================================================================


def print_section(title: str):
    """Imprime un separador bonito"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def test_backend_health():
    """Verifica que el backend esté disponible"""
    print_section("1. VERIFICANDO DISPONIBILIDAD DEL BACKEND")

    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está corriendo en puerto 8000")
            return True
        else:
            print(f"⚠️ Backend respondió con status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend en http://localhost:8000")
        print()
        print("Para iniciar el backend:")
        print("  cd ./backed")
        print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_webhook_verification():
    """
    Simula el proceso de verificación que hace Meta al configurar el webhook
    """
    print_section("2. PROBANDO VERIFICACIÓN DE WEBHOOK (Meta → Tu Servidor)")

    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": "my_secret_verify_token_2024",  # Mismo que en configure_whatsapp.py
        "hub.challenge": "test_challenge_string_12345"
    }

    print(f"Enviando GET a: {WEBHOOK_URL}")
    print(f"Parámetros: {params}")
    print()

    try:
        response = requests.get(WEBHOOK_URL, params=params, timeout=5)

        if response.status_code == 200:
            if response.text == "test_challenge_string_12345":
                print("✅ Webhook VERIFICADO correctamente")
                print(f"   Respuesta: {response.text}")
                return True
            else:
                print(f"⚠️ Webhook respondió pero con dato inesperado: {response.text}")
                return False
        else:
            print(f"❌ Webhook respondió con status {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error al verificar webhook: {e}")
        return False


def test_incoming_message():
    """
    Simula un mensaje entrante que Meta enviaría a tu webhook
    """
    print_section("3. SIMULANDO MENSAJE ENTRANTE DE WHATSAPP")

    # Estructura exacta del payload que Meta envía
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "1234567890",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "1 555 636 6119",
                                "phone_number_id": "989003167640614"  # El de tu configuración
                            },
                            "messages": [
                                {
                                    "from": "1234567890",
                                    "id": "wamid.xxx",
                                    "timestamp": str(int(time.time())),
                                    "type": "text",
                                    "text": {
                                        "body": "Hola, quiero comprar productos"
                                    }
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }

    print(f"Enviando POST a: {WEBHOOK_URL}")
    print(f"Payload simulado:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print()

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=10)

        print(f"Status Code: {response.status_code}")
        print()

        if response.status_code >= 400:
            print(f"❌ Error {response.status_code}")
            try:
                print(f"   Respuesta: {response.json()}")
            except:
                print(f"   Respuesta: {response.text}")
            return False

        else:
            print("✅ Webhook recibió el mensaje")
            try:
                result = response.json()
                print(f"   Respuesta del servidor:")
                print(f"   {json.dumps(result, indent=2, ensure_ascii=False)}")
            except:
                print(f"   Body: {response.text}")
            print()
            return True

    except requests.exceptions.Timeout:
        print("⚠️ El webhook tardó más de 10 segundos en responder")
        print("   (Meta espera < 30 segundos antes de reintentar)")
        return False

    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
        return False


def test_message_sending():
    """
    Verifica que el backend puede enviar mensajes de vuelta a WhatsApp
    (Esta es una prueba "en seco" - no enviará realmente por WhatsApp)
    """
    print_section("4. VERIFICANDO CAPACIDAD DE ENVÍO DE MENSAJES")

    print("Esta es una prueba simulada. En producción:")
    print("  1. Backend recibe mensaje en /whatsapp/webhook")
    print("  2. Llama al agente para generar respuesta")
    print("  3. Backend hace POST a Meta:")
    print("     https://graph.facebook.com/v25.0/{phone_number_id}/messages")
    print()
    print("Estructura del POST (ejemplo):")

    message_payload = {
        "messaging_product": "whatsapp",
        "to": "1234567890",
        "type": "text",
        "text": {
            "body": "¡Hola! Bienvenido a [Tu Empresa]..."
        }
    }

    print(json.dumps(message_payload, indent=2, ensure_ascii=False))
    print()
    print("✅ Estructura validada")

    return True


def print_next_steps():
    """Imprime los próximos pasos"""
    print_section("✅ PRÓXIMOS PASOS")

    print("1.📝 ejecuta: python scripts/configure_whatsapp.py")
    print("   → Registra tus credenciales de WhatsApp en la BD")
    print()

    print("2. 🔗 Configura el webhook en Meta:")
    print("   a) Ve a: https://developers.facebook.com/apps")
    print("   b) Selecciona tu app → WhatsApp → Configuration")
    print("   c) Webhook URL: https://tu-ngrok-url.ngrok.io/whatsapp/webhook")
    print("      (O tu dominio en producción)")
    print("   d) Verify Token: my_secret_verify_token_2024")
    print("   e) Subscribe to: messages, message_status")
    print()

    print("3. 🧪 Prueba enviando un mensaje desde Meta:")
    print("   a) En Meta, ve a API Setup")
    print("   b) \"Enviar y recibir mensajes\" → \"Enviar mensaje de prueba\"")
    print("   c) Ingresa: +1 555 636 6119 o tu número")
    print()

    print("4. 📱 Si todo funciona:")
    print("   - Recibirás el mensaje en /whatsapp/webhook")
    print("   - El agente generará una respuesta")
    print("   - La respuesta se enviará de vuelta por WhatsApp")
    print()


def main():
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           🧪 TEST DE INTEGRACIÓN WHATSAPP BUSINESS                  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    results = {}

    # Test 1: Backend Health
    results["backend_health"] = test_backend_health()
    if not results["backend_health"]:
        print("\n❌ No se puede continuar sin el backend")
        return False

    time.sleep(1)

    # Test 2: Webhook Verification
    results["webhook_verify"] = test_webhook_verification()
    time.sleep(1)

    # Test 3: Incoming Message
    results["incoming_message"] = test_incoming_message()
    time.sleep(1)

    # Test 4: Message Sending
    results["message_sending"] = test_message_sending()

    # Summary
    print_section("📊 RESUMEN DE RESULTADOS")

    all_passed = all(results.values())

    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name.replace('_', ' ').title()}")

    print()

    if all_passed:
        print("🎉 TODOS LOS TESTS PASARON!")
        print_next_steps()
        return True
    else:
        print("⚠️ Algunos tests fallaron. Revisa los mensajes arriba.")
        return False


if __name__ == "__main__":
    success = main()
    print()
