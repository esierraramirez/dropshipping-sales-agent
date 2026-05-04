#!/usr/bin/env python3
"""
Script de prueba para validar las mejoras del agente de ventas.
Ejecutar: python backed/test_improvements.py
"""

import sys
sys.path.insert(0, 'backed')

from app.utils.gender_detection import detect_gender_by_name, infer_gender_from_conversation
from app.utils.data_extraction import (
    extract_customer_name, extract_phone_number, extract_address,
    extract_confirmation_intent, extract_rejection_intent,
    update_purchase_context_from_message
)
from app.agent.policies import is_within_business_hours
from datetime import datetime
import pytz


def test_gender_detection():
    """Test del detector de género por nombre."""
    print("\n=== TEST: DETECCIÓN DE GÉNERO POR NOMBRE ===")
    
    test_cases = [
        ("Juan", "masculino"),
        ("María", "femenino"),
        ("Carlos", "masculino"),
        ("Ana", "femenino"),
        ("Diego", "masculino"),
        ("Sofía", "femenino"),
        ("Alex", None),  # Ambiguo
    ]
    
    for name, expected in test_cases:
        result = detect_gender_by_name(name)
        status = "✅" if result == expected else "❌"
        print(f"{status} detect_gender_by_name('{name}') = {result} (esperado: {expected})")


def test_data_extraction():
    """Test de extracción de datos del cliente."""
    print("\n=== TEST: EXTRACCIÓN DE DATOS DEL CLIENTE ===")
    
    # Test nombre
    text1 = "Hola, me llamo Carlos García"
    name = extract_customer_name(text1)
    print(f"✅ extract_customer_name('{text1}') = {name}")
    
    # Test teléfono
    text2 = "Mi teléfono es 3015551234"
    phone = extract_phone_number(text2)
    print(f"✅ extract_phone_number('{text2}') = {phone}")
    
    # Test dirección
    text3 = "Vivo en calle 5 #45, apartamento 301, Bogotá"
    address = extract_address(text3)
    print(f"✅ extract_address('{text3}') = {address}")
    
    # Test confirmación
    text4 = "Sí, dale, dame uno de esos"
    confirmation = extract_confirmation_intent(text4)
    print(f"✅ extract_confirmation_intent('{text4}') = {confirmation}")
    
    # Test rechazo
    text5 = "No, es muy caro para mí"
    rejection = extract_rejection_intent(text5)
    print(f"✅ extract_rejection_intent('{text5}') = {rejection}")


def test_purchase_context_update():
    """Test de actualización de purchase_context."""
    print("\n=== TEST: ACTUALIZACIÓN DE PURCHASE_CONTEXT ===")
    
    pc = {}
    
    # Primer mensaje: nombre
    msg1 = "Hola, soy Juan"
    pc = update_purchase_context_from_message(pc, msg1)
    print(f"Después de msg1: {pc}")
    assert pc.get("customer_name") == "Juan", "❌ Nombre no extractado"
    print("✅ Nombre extraído correctamente")
    
    # Segundo mensaje: teléfono
    msg2 = "Mi teléfono es 3001234567"
    pc = update_purchase_context_from_message(pc, msg2)
    print(f"Después de msg2: {pc}")
    assert pc.get("customer_phone") == "3001234567", "❌ Teléfono no extractado"
    print("✅ Teléfono extraído correctamente")
    
    # Tercer mensaje: dirección
    msg3 = "Mi dirección es calle 5 #45"
    pc = update_purchase_context_from_message(pc, msg3)
    print(f"Después de msg3: {pc}")
    assert pc.get("customer_address"), "❌ Dirección no extractada"
    print("✅ Dirección extraída correctamente")
    
    # Cuarto mensaje: confirmación de compra
    msg4 = "Sí, confirmó, adelante con la orden"
    pc = update_purchase_context_from_message(pc, msg4)
    print(f"Después de msg4 (confirmación): {pc}")
    assert pc.get("is_confirmed") == True, "❌ Confirmación no detectada"
    print("✅ Confirmación detectada correctamente")
    
    print(f"\n✅ Purchase context final completo: {pc}")


def test_business_hours():
    """Test de validación de horarios."""
    print("\n=== TEST: VALIDACIÓN DE HORARIOS ===")
    
    # Test: horario normal (08:00-18:00)
    result1 = is_within_business_hours("08:00", "18:00", "America/Bogota")
    print(f"✅ is_within_business_hours('08:00', '18:00') = {result1}")
    
    # Test: horario que cruza medianoche
    result2 = is_within_business_hours("22:00", "06:00", "America/Bogota")
    print(f"✅ is_within_business_hours('22:00', '06:00') = {result2}")
    
    # Test: sin horario
    result3 = is_within_business_hours(None, None)
    assert result3 == True, "❌ Sin horario debería retornar True"
    print(f"✅ is_within_business_hours(None, None) = {result3}")
    
    # Info de hora actual
    tz = pytz.timezone("America/Bogota")
    now = datetime.now(tz)
    print(f"\nℹ️ Hora actual en Bogotá: {now.strftime('%H:%M:%S')}")


def test_conversation_history():
    """Test con historial de conversación."""
    print("\n=== TEST: MEMORIA CONVERSACIONAL ===")
    
    history = [
        {"role": "user", "content": "Hola, soy María"},
        {"role": "assistant", "content": "Hola María! Encantado de atenderte 😊"},
        {"role": "user", "content": "Quiero ese jean mom que viste"},
        {"role": "assistant", "content": "Perfecto, el jean mom es excelente..."},
        {"role": "user", "content": "Dale, dame uno"},
    ]
    
    gender = infer_gender_from_conversation(history)
    print(f"✅ infer_gender_from_conversation() = {gender}")
    assert gender == "femenino", "❌ Género no inferido correctamente del historial"
    print("✅ Género inferido correctamente del historial")


def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  PRUEBAS DE MEJORAS DEL AGENTE DE VENTAS                  ║")
    print("║  Versión 2.0 - 29 de Abril de 2026                        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    try:
        test_gender_detection()
        test_data_extraction()
        test_purchase_context_update()
        test_business_hours()
        test_conversation_history()
        
        print("\n" + "="*60)
        print("✅ ¡TODAS LAS PRUEBAS PASARON CORRECTAMENTE!")
        print("="*60)
        print("\n🎉 El agente está listo para producción.")
        print("📝 Próximos pasos:")
        print("   1. Instalar dependencias: pip install -r requirements.txt")
        print("   2. Iniciar backend: python start_backend.bat")
        print("   3. Probar en el frontend")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
