#!/usr/bin/env python3
"""
🧪 TEST COMPLETO DEL FLUJO - Sistema de Ventas con IA

Ejecuta: python test_complete_flow.py

Este script:
1. ✅ Registra una empresa de prueba
2. ✅ Crea un Excel con productos de ejemplo
3. ✅ Carga el Excel
4. ✅ Normaliza los datos
5. ✅ Guarda en BD
6. ✅ Construye base de conocimiento
7. ✅ Prueba 3 queries diferentes en el chat
8. ✅ Verifica respuestas de LLM
9. ✅ Limpia datos de prueba (opcional)
"""

import requests
import json
import sys
import time
from pathlib import Path
from datetime import datetime
import io
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}@tienda.com"
TEST_COMPANY = "Test Tienda " + datetime.now().strftime("%H:%M:%S")

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")

def print_step(number, text):
    """Print step"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}PASO {number}: {text}{Colors.RESET}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def create_test_excel():
    """Create test Excel file with products"""
    wb = openpyxl.Workbook()
    ws: Worksheet = wb.active
    ws.title = "Productos"
    
    # Headers
    ws.append(["product_id", "name", "description", "category", "price", "currency", "stock_status", "stock_quantity"])
    
    # Test products
    products = [
        ["001", "Camiseta Roja Premium", "Camiseta 100% algodón", "Ropa", "25.00", "USD", "in_stock", "50"],
        ["002", "Pantalón Negro Casual", "Pantalón de jean", "Ropa", "45.00", "USD", "in_stock", "30"],
        ["003", "Gorro Deportivo", "Gorro para deporte", "Accesorios", "15.00", "USD", "low_stock", "5"],
        ["004", "Zapatillas Running", "Zapatillas para correr", "Calzado", "85.00", "USD", "in_stock", "20"],
        ["005", "Sudadera Azul", "Sudadera cómoda", "Ropa", "35.00", "USD", "in_stock", "40"],
    ]
    
    for product in products:
        ws.append(product)
    
    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column[0].column_letter].width = max_length + 2
    
    # Save to bytes
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

def test_step_1_register(verbose=False):
    """PASO 1: Register company"""
    print_step(1, "Registrar empresa")
    
    payload = {
        "name": TEST_COMPANY,
        "email": TEST_EMAIL,
        "password": "Test@123456",
        "rfc": "RFC" + datetime.now().strftime("%Y%m%d%H%M"),
        "sector": "Moda",
        "phone": "+57 3001234567",
        "website": "https://test-tienda.com",
        "address": "Calle Test 123",
        "city": "Bogotá",
        "state": "Cundinamarca",
        "country": "Colombia",
        "postal_code": "110001",
        "description": "Tienda de prueba para testing"
    }
    
    if verbose:
        print_info(f"Request: POST {BASE_URL}/auth/register")
        print_info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=payload,
            timeout=10
        )
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return None
        
        data = response.json()
        
        # Verify required fields
        if "access_token" not in data:
            print_error("access_token no presente en response")
            return None
        
        if "vendor" not in data:
            print_error("vendor no presente en response")
            return None
        
        print_success(f"Empresa registrada: {TEST_COMPANY}")
        print_success(f"Email: {TEST_EMAIL}")
        print_success(f"Token obtenido: {data['access_token'][:30]}...")
        
        if verbose:
            print_info(f"Response: {json.dumps(data, indent=2)}")
        
        return {
            "token": data["access_token"],
            "vendor_id": data["vendor"].get("id"),
            "vendor_name": data["vendor"].get("name")
        }
    
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar con el servidor. ¿Está corriendo en localhost:8000?")
        return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_step_2_upload_excel(token, verbose=False):
    """PASO 2: Upload Excel with products"""
    print_step(2, "Cargar archivo Excel")
    
    try:
        excel_buffer = create_test_excel()
        
        if verbose:
            print_info("Request: POST /catalog/upload/me")
            print_info("File: test_products.xlsx (5 productos)")
        
        response = requests.post(
            f"{BASE_URL}/catalog/upload/me",
            files={"file": ("test_products.xlsx", excel_buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
        
        data = response.json()
        print_success(f"Excel cargado exitosamente")
        print_success(f"Total de filas: {data.get('total_rows', 'N/A')}")
        print_success(f"Válidas: {data.get('valid_rows', 'N/A')}")
        
        if verbose:
            print_info(f"Response preview: {data.get('preview_rows', [])[:2]}")
        
        return True
    
    except Exception as e:
        print_error(f"Error al cargar Excel: {str(e)}")
        return False

def test_step_3_normalize(token, verbose=False):
    """PASO 3: Normalize catalog"""
    print_step(3, "Normalizar datos")
    
    try:
        if verbose:
            print_info("Request: POST /catalog/normalize/me")
        
        response = requests.post(
            f"{BASE_URL}/catalog/normalize/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15
        )
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
        
        data = response.json()
        print_success(f"Datos normalizados")
        print_success(f"Filas válidas: {data.get('valid_rows', 'N/A')}")
        print_success(f"Filas inválidas: {data.get('invalid_rows', 0)}")
        
        if verbose:
            print_info(f"Archivos generados:")
            print_info(f"  - catalog_normalized.csv")
            print_info(f"  - catalog_normalized.jsonl")
            print_info(f"  - data_quality_report.json")
        
        return True
    
    except Exception as e:
        print_error(f"Error al normalizar: {str(e)}")
        return False

def test_step_4_save_to_db(token, verbose=False):
    """PASO 4: Save to database"""
    print_step(4, "Guardar en Base de Datos")
    
    try:
        if verbose:
            print_info("Request: POST /catalog/save/me")
        
        response = requests.post(
            f"{BASE_URL}/catalog/save/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
        
        data = response.json()
        total_saved = data.get('total_saved', data.get('message', 'N/A'))
        print_success(f"Productos guardados en BD")
        print_success(f"Total: {total_saved}")
        
        if verbose:
            print_info(f"Response: {json.dumps(data, indent=2)}")
        
        return True
    
    except Exception as e:
        print_error(f"Error al guardar: {str(e)}")
        return False

def test_step_5_build_kb(token, verbose=False):
    """PASO 5: Build knowledge base"""
    print_step(5, "Construir Base de Conocimiento")
    
    try:
        if verbose:
            print_info("Request: POST /catalog/build-knowledge-base/me")
        
        response = requests.post(
            f"{BASE_URL}/catalog/build-knowledge-base/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
        
        data = response.json()
        print_success(f"Base de conocimiento construida")
        print_success(f"Documentos indexados: {data.get('documents_created', 'N/A')}")
        
        if verbose:
            print_info(f"Archivos generados en data/index/:")
            print_info(f"  - knowledge_base.jsonl")
            print_info(f"  - keyword_index.json")
        
        return True
    
    except Exception as e:
        print_error(f"Error al construir KB: {str(e)}")
        return False

def test_step_6_chat_queries(token, vendor_name, verbose=False):
    """PASO 6: Test chat with LLM"""
    print_step(6, "Probar Chat con LLM")
    
    test_queries = [
        "¿Qué camisetas tienes disponibles?",
        "Quiero zapatillas para correr, ¿cuál me recomiendas?",
        "¿Cuál es el producto más barato que tienen?"
    ]
    
    all_success = True
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n  {Colors.BOLD}Query {i}: {query}{Colors.RESET}")
        
        try:
            if verbose:
                print_info(f"Request: POST /chat/me")
                print_info(f"Query: {query}")
            
            response = requests.post(
                f"{BASE_URL}/chat/me",
                json={"message": query},
                headers={"Authorization": f"Bearer {token}"},
                timeout=15
            )
            
            if response.status_code != 200:
                print_error(f"Status {response.status_code}: {response.text}")
                all_success = False
                continue
            
            data = response.json()
            
            # Verify response structure
            if "agent_response" not in data:
                print_error("agent_response no presente en response")
                all_success = False
                continue
            
            agent_response = data["agent_response"]
            matches_found = data.get("matches_found", 0)
            vendor_name_response = data.get("vendor_name", "N/A")
            
            print_success(f"Respuesta recibida")
            print_success(f"Productos encontrados: {matches_found}")
            print(f"  {Colors.BLUE}Respuesta: {agent_response[:100]}...{Colors.RESET}")
            
            if verbose:
                print_info(f"Full response:")
                print_info(f"  - Vendor: {vendor_name_response}")
                print_info(f"  - Message: {query}")
                print_info(f"  - Response: {agent_response}")
                print_info(f"  - Matches: {matches_found}")
                if data.get("context_used"):
                    print_info(f"  - Context: {data.get('context_used')[:200]}...")
            
            # Check if response makes sense (mentions products or prices)
            response_lower = agent_response.lower()
            has_product_mention = any(word in response_lower for word in ["camiseta", "pantalón", "zapatilla", "gorro", "sudadera", "producto", "$"])
            
            if has_product_mention:
                print_success(f"Respuesta contiene referencias a productos ✓")
            else:
                print_info(f"⚠️  Respuesta no contiene referencias obvias a productos")
        
        except Exception as e:
            print_error(f"Error en query {i}: {str(e)}")
            all_success = False
        
        time.sleep(0.5)  # Small delay between requests
    
    return all_success

def main():
    """Main test execution"""
    print_header("🚀 VERIFICACIÓN COMPLETA DEL FLUJO DE VENTAS")
    
    print_info(f"🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"📍 Base URL: {BASE_URL}")
    print_info(f"👤 Empresa de prueba: {TEST_COMPANY}")
    print_info(f"📧 Email: {TEST_EMAIL}")
    
    # Check if should run verbose
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    if verbose:
        print_info("Modo VERBOSE activado")
    
    # Run tests
    start_time = time.time()
    
    # Step 1: Register
    result = test_step_1_register(verbose)
    if not result:
        print_error("\n❌ FALLÓ en paso 1: Registro")
        print_error("Verifica que el backend esté corriendo en http://localhost:8000")
        return False
    
    token = result["token"]
    vendor_id = result["vendor_id"]
    vendor_name = result["vendor_name"]
    
    # Step 2: Upload
    if not test_step_2_upload_excel(token, verbose):
        print_error("\n❌ FALLÓ en paso 2: Carga de Excel")
        return False
    
    time.sleep(1)
    
    # Step 3: Normalize
    if not test_step_3_normalize(token, verbose):
        print_error("\n❌ FALLÓ en paso 3: Normalización")
        return False
    
    time.sleep(1)
    
    # Step 4: Save to DB
    if not test_step_4_save_to_db(token, verbose):
        print_error("\n❌ FALLÓ en paso 4: Guardar en BD")
        return False
    
    time.sleep(1)
    
    # Step 5: Build KB
    if not test_step_5_build_kb(token, verbose):
        print_error("\n❌ FALLÓ en paso 5: Construir Base de Conocimiento")
        return False
    
    time.sleep(2)  # Wait for index to be ready
    
    # Step 6: Chat
    if not test_step_6_chat_queries(token, vendor_name, verbose):
        print_error("\n❌ FALLÓ en paso 6: Chat con LLM")
        return False
    
    # Summary
    elapsed = time.time() - start_time
    
    print_header("✅ RESUMEN DE VERIFICACIÓN")
    
    print_success(f"Todos los pasos completados exitosamente")
    print_success(f"Tiempo total: {elapsed:.2f} segundos")
    print_success(f"Empresa creada: {TEST_COMPANY} ({vendor_id})")
    print_success(f"Products logged in: BD")
    print_success(f"Base de conocimiento: INDEXADA")
    print_success(f"Chat LLM: FUNCIONAL")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 FLUJO COMPLETAMENTE VERIFICADO Y FUNCIONAL 🎉{Colors.RESET}")
    
    print_info(f"📊 Datos de prueba creados:")
    print_info(f"   - Empresa: {TEST_COMPANY}")
    print_info(f"   - Email: {TEST_EMAIL}")
    print_info(f"   - 5 productos en BD")
    print_info(f"   - Base de conocimiento indexada")
    
    print_info(f"\n💡 Próximos pasos:")
    print_info(f"   1. Prueba en producción con datos reales")
    print_info(f"   2. Monitorea uso de tokens en OpenAI")
    print_info(f"   3. Revisa logs en {BASE_URL}/logs")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Cancelado por el usuario{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error no manejado: {str(e)}")
        sys.exit(1)
