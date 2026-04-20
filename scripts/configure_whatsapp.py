#!/usr/bin/env python3
"""
Script para configurar WhatsApp Business API connection
Uso: python configure_whatsapp.py
"""

import requests
import json
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN - Reemplaza estos valores con los tuyos
# ============================================================================

BACKEND_URL = "http://localhost:8000"
AUTH_TOKEN = ""  # Tu JWT token - déjalo vacío para que te lo pida interactivamente
PHONE_NUMBER = "+1 555 636 6119"  # El número de WhatsApp
PHONE_NUMBER_ID = "989003167640614"  # Copia de Meta - Identificador de número de teléfono
BUSINESS_ACCOUNT_ID = "2479057362544519"  # Copia de Meta - Identificador de la cuenta
ACCESS_TOKEN = ""  # Copia de Meta - Token de acceso
VERIFY_TOKEN = "my_secret_verify_token_2024"  # Genera uno (puede ser cualquier string)

# ============================================================================


def get_input_or_use_default(prompt: str, default_value: str = None, is_secret=False) -> str:
    """
    Pide input al usuario, con opción de usar valor default si lo hay.
    Si is_secret=True, no muestra el valor mientras se tipea.
    """
    if default_value:
        display_value = default_value[:10] + "..." if len(default_value or "") > 10 else default_value
        if is_secret:
            display_value = "***" * 5
        prompt_with_default = f"{prompt} [{display_value}]: "
    else:
        prompt_with_default = f"{prompt}: "

    user_input = input(prompt_with_default).strip()

    if not user_input and default_value:
        return default_value

    if not user_input:
        print("❌ Campo requerido. Por favor, ingresa un valor.")
        return get_input_or_use_default(prompt, default_value, is_secret)

    return user_input


def validate_phone_number_id(phone_id: str) -> bool:
    """Valida que el phone_number_id tenga format correcto (números)"""
    return phone_id.isdigit() and len(phone_id) > 10


def validate_business_account_id(bus_id: str) -> bool:
    """Valida que el business_account_id tenga format correcto"""
    return bus_id.isdigit() and len(bus_id) > 10


def validate_access_token(token: str) -> bool:
    """Valida que el access_token tenga format correcto"""
    return token.startswith("EAA") and len(token) > 100


def main():
    print("=" * 70)
    print("🔐 CONFIGURACIÓN DE WHATSAPP BUSINESS API")
    print("=" * 70)
    print()

    # ========================================================================
    # PASO 1: Obtener JWT Token
    # ========================================================================
    print("📝 PASO 1: Autenticación")
    print("-" * 70)

    global AUTH_TOKEN
    if not AUTH_TOKEN:
        print("Necesitamos tu JWT token para autenticarte.")
        print("Puedes obtenerlo en: http://localhost:5173/login")
        print()
        auth_input = get_input_or_use_default(
            "Ingresa tu JWT token",
            "",
            is_secret=True
        )
        AUTH_TOKEN = auth_input
    else:
        print(f"✅ Usando JWT token configurado")

    print()

    # ========================================================================
    # PASO 2: Obtener credenciales de WhatsApp
    # ========================================================================
    print("📱 PASO 2: Credenciales de WhatsApp Business")
    print("-" * 70)
    print("Obtén estos valores en: https://developers.facebook.com/apps")
    print("  → WhatsApp → API Setup → Números disponibles")
    print()

    # Phone Number
    global PHONE_NUMBER
    PHONE_NUMBER = get_input_or_use_default(
        "Número de teléfono WhatsApp (ej. +1 555 636 6119)",
        PHONE_NUMBER
    )

    # Phone Number ID
    global PHONE_NUMBER_ID
    while True:
        PHONE_NUMBER_ID = get_input_or_use_default(
            "Identificador de número de teléfono (solo números)",
            PHONE_NUMBER_ID
        )
        if validate_phone_number_id(PHONE_NUMBER_ID):
            break
        print("❌ El formato debe ser solo números y > 10 caracteres")

    # Business Account ID
    global BUSINESS_ACCOUNT_ID
    while True:
        BUSINESS_ACCOUNT_ID = get_input_or_use_default(
            "Identificador de la cuenta de WhatsApp Business",
            BUSINESS_ACCOUNT_ID
        )
        if validate_business_account_id(BUSINESS_ACCOUNT_ID):
            break
        print("❌ El formato debe ser solo números y > 10 caracteres")

    # Access Token
    global ACCESS_TOKEN
    while True:
        ACCESS_TOKEN = get_input_or_use_default(
            "Token de acceso (comienza con 'EAA')",
            ACCESS_TOKEN,
            is_secret=True
        )
        if validate_access_token(ACCESS_TOKEN):
            break
        print("❌ El token debe empezar con 'EAA' y tener > 100 caracteres")

    # Verify Token
    global VERIFY_TOKEN
    VERIFY_TOKEN = get_input_or_use_default(
        "Verify Token (tu clave secreta, puede ser cualquier string)",
        VERIFY_TOKEN
    )

    print()

    # ========================================================================
    # PASO 3: Confirmar datos
    # ========================================================================
    print("🔍 RESUMEN DE CONFIGURACIÓN")
    print("-" * 70)
    print(f"Número de teléfono:        {PHONE_NUMBER}")
    print(f"Identificador de número:   {PHONE_NUMBER_ID}")
    print(f"Identificador de cuenta:   {BUSINESS_ACCOUNT_ID}")
    print(f"Token de acceso:           {ACCESS_TOKEN[:20]}...")
    print(f"Verify Token:              {VERIFY_TOKEN}")
    print()

    confirmar = input("¿Estos datos son correctos? (s/n): ").strip().lower()
    if confirmar != "s":
        print("❌ Operación cancelada.")
        return False

    print()

    # ========================================================================
    # PASO 4: Enviar al backend
    # ========================================================================
    print("📤 PASO 3: Enviando configuración al backend...")
    print("-" * 70)

    payload = {
        "phone_number": PHONE_NUMBER,
        "phone_number_id": PHONE_NUMBER_ID,
        "business_account_id": BUSINESS_ACCOUNT_ID,
        "access_token": ACCESS_TOKEN,
        "verify_token": VERIFY_TOKEN,
    }

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(
            f"{BACKEND_URL}/whatsapp/me",
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Configuración guardada exitosamente!")
            print()
            print("Respuesta del servidor:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            return True

        else:
            print(f"❌ Error {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   Razón: {error_detail.get('detail', 'Error desconocido')}")
            except:
                print(f"   Respuesta: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ No se pudo conectar a {BACKEND_URL}")
        print("   Asegúrate de que el backend esté ejecutándose en puerto 8000")
        print()
        print("   Para iniciar el backend, ejecuta:")
        print("   cd ./backed")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return False

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


if __name__ == "__main__":
    success = main()

    print()
    print("=" * 70)
    if success:
        print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
        print()
        print("Próximos pasos:")
        print("1. Ve a https://developers.facebook.com/apps → Tu app → WhatsApp")
        print("2. Configuration → Webhook Configuration")
        print("3. Ingresa tu Webhook URL:")
        print("   - Local: https://tu-ngrok-url.ngrok.io/whatsapp/webhook")
        print("   - Producción: https://tu-dominio.com/whatsapp/webhook")
        print(f"4. Verify Token: {VERIFY_TOKEN}")
        print()
        print("5. En Meta, prueba enviando un mensaje de prueba")
        print("6. Deberías recibirlo en tu backend (revisa los logs)")
        print()
        print("¡Tu agente está listo para recibir mensajes de WhatsApp!")
    else:
        print("⚠️ Configuración no completada.")
        print("Por favor, verifica los datos e intenta nuevamente.")
    print("=" * 70)
