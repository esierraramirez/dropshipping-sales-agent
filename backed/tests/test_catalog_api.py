"""
🧪 Pruebas Automatizadas - Catálogo de Productos
Ubicación: backed/tests/test_catalog_api.py
Uso: python -m pytest test_catalog_api.py -v
     o: python test_catalog_api.py
"""

import requests
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

BASE_URL = "http://127.0.0.1:8000"
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Colores para salida
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_section(title: str):
    """Imprimir encabezado de sección"""
    print(f"\n{Color.CYAN}{Color.BOLD}{'='*60}{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{title:^60}{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'='*60}{Color.RESET}\n")

def print_pass(test_name: str, message: str = ""):
    """Imprimir resultado positivo"""
    msg = f" | {message}" if message else ""
    print(f"{Color.GREEN}✅ PASS{Color.RESET} {test_name}{msg}")

def print_fail(test_name: str, message: str = ""):
    """Imprimir resultado negativo"""
    msg = f" | {message}" if message else ""
    print(f"{Color.RED}❌ FAIL{Color.RESET} {test_name}{msg}")

# ==================================================
# FUNCIONALIDAD 1: Schema Validation
# ==================================================

def test_1_valid_upload():
    """Test 1.1: Subir archivo válido"""
    print_section("FUNCIONALIDAD 1: Validación de Esquema")
    
    try:
        with open(TEST_DATA_DIR / 'valid_catalog.xlsx', 'rb') as f:
            files = {'file': f}
            data = {'vendor_name': 'TestVendor'}
            response = requests.post(f"{BASE_URL}/catalog/upload", files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('is_valid') and len(result.get('missing_required_columns', [])) == 0:
                print_pass("1.1: Archivo válido cargado", f"Columnas: {len(result.get('detected_columns', []))}")
                return True
        
        print_fail("1.1: Archivo válido cargado", f"Status: {response.status_code}")
        return False
    except Exception as e:
        print_fail("1.1", str(e))
        return False

def test_1_missing_columns():
    """Test 1.2: Detectar columnas faltantes"""
    try:
        with open(TEST_DATA_DIR / 'invalid_missing_columns.xlsx', 'rb') as f:
            files = {'file': f}
            data = {'vendor_name': 'TestVendor2'}
            response = requests.post(f"{BASE_URL}/catalog/upload", files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            missing = result.get('missing_required_columns', [])
            if len(missing) > 0 and not result.get('is_valid'):
                print_pass("1.2: Columnas faltantes detectadas", f"Faltantes: {len(missing)}")
                return True
        
        print_fail("1.2: Columnas faltantes detectadas")
        return False
    except Exception as e:
        print_fail("1.2", str(e))
        return False

# ==================================================
# FUNCIONALIDAD 2: Upload & Validation
# ==================================================

def test_2_upload_storage():
    """Test 2.1: Archivo se guarda correctamente"""
    print_section("FUNCIONALIDAD 2: Carga y Validación")
    
    try:
        with open(TEST_DATA_DIR / 'dirty_data.xlsx', 'rb') as f:
            files = {'file': f}
            data = {'vendor_name': 'TestVendor3'}
            response = requests.post(f"{BASE_URL}/catalog/upload", files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            saved_path = Path(result.get('saved_path', ''))
            if saved_path.exists():
                print_pass("2.1: Archivo guardado en data/raw/", f"Filas: {result.get('total_rows', 0)}")
                return True
        
        print_fail("2.1: Archivo guardado en data/raw/")
        return False
    except Exception as e:
        print_fail("2.1", str(e))
        return False

def test_2_preview():
    """Test 2.2: Preview de datos disponible"""
    try:
        with open(TEST_DATA_DIR / 'valid_catalog.xlsx', 'rb') as f:
            files = {'file': f}
            data = {'vendor_name': 'TestVendor4'}
            response = requests.post(f"{BASE_URL}/catalog/upload", files=files, data=data, timeout=10)
        
        result = response.json()
        if 'preview_rows' in result and len(result.get('preview_rows', [])) > 0:
            print_pass("2.2: Preview disponible", f"Rows: {len(result['preview_rows'])}")
            return True
        
        print_fail("2.2: Preview disponible")
        return False
    except Exception as e:
        print_fail("2.2", str(e))
        return False

# ==================================================
# FUNCIONALIDAD 3: Normalization
# ==================================================

def test_3_normalize():
    """Test 3.1: Normalizar datos"""
    print_section("FUNCIONALIDAD 3: Normalización")
    
    try:
        # Primero subir
        with open(TEST_DATA_DIR / 'dirty_data.xlsx', 'rb') as f:
            files = {'file': f}
            data = {'vendor_name': 'TestVendor5'}
            requests.post(f"{BASE_URL}/catalog/upload", files=files, data=data, timeout=10)
        
        # Luego normalizar
        response = requests.post(f"{BASE_URL}/catalog/normalize", 
                                data={'vendor_name': 'TestVendor5'}, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('valid_rows', 0) > 0:
                print_pass("3.1: Datos normalizados", 
                          f"Válidas: {result.get('valid_rows')} | "
                          f"Inválidas: {result.get('invalid_rows')}")
                return True
        
        print_fail("3.1: Datos normalizados")
        return False
    except Exception as e:
        print_fail("3.1", str(e))
        return False

def test_3_quality_report():
    """Test 3.2: Reporte de calidad generado"""
    try:
        # Usando TestVendor5 del test anterior
        response = requests.post(f"{BASE_URL}/catalog/normalize", 
                                data={'vendor_name': 'TestVendor5'}, timeout=10)
        
        result = response.json()
        report_path = Path(result.get('quality_report_path', ''))
        if report_path.exists():
            print_pass("3.2: Reporte de calidad generado", f"Ruta: {report_path.name}")
            return True
        
        print_fail("3.2: Reporte de calidad generado")
        return False
    except Exception as e:
        print_fail("3.2", str(e))
        return False

# ==================================================
# FUNCIONALIDAD 4: Database Storage
# ==================================================

def test_4_save_to_db():
    """Test 4.1: Guardar en BD"""
    print_section("FUNCIONALIDAD 4: Base de Datos")
    
    try:
        # Preparar datos
        with open(TEST_DATA_DIR / 'valid_catalog.xlsx', 'rb') as f:
            files = {'file': f}
            data = {'vendor_name': 'TestVendor6'}
            requests.post(f"{BASE_URL}/catalog/upload", files=files, data=data, timeout=10)
        
        requests.post(f"{BASE_URL}/catalog/normalize", 
                     data={'vendor_name': 'TestVendor6'}, timeout=10)
        
        # Guardar
        response = requests.post(f"{BASE_URL}/catalog/save", 
                                data={'vendor_name': 'TestVendor6'}, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('products_saved', 0) > 0:
                print_pass("4.1: Guardado en BD", f"Productos: {result['products_saved']}")
                return True
        
        print_fail("4.1: Guardado en BD")
        return False
    except Exception as e:
        print_fail("4.1", str(e))
        return False

def test_4_query_products():
    """Test 4.2: Consultar productos"""
    try:
        response = requests.get(f"{BASE_URL}/catalog/products?vendor_name=TestVendor6", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('total_products', 0) > 0:
                print_pass("4.2: Consultar productos", f"Total: {result['total_products']}")
                return True
        
        print_fail("4.2: Consultar productos")
        return False
    except Exception as e:
        print_fail("4.2", str(e))
        return False

# ==================================================
# FUNCIONALIDAD 5: Knowledge Base
# ==================================================

def test_5_build_kb():
    """Test 5.1: Construir KB"""
    print_section("FUNCIONALIDAD 5: Base de Conocimiento")
    
    try:
        # Usar TestVendor6 que ya está guardado
        response = requests.post(f"{BASE_URL}/catalog/build-knowledge-base", 
                                data={'vendor_name': 'TestVendor6'}, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('documents_created', 0) > 0:
                print_pass("5.1: KB construida", f"Documentos: {result['documents_created']}")
                return True
        
        print_fail("5.1: KB construida")
        return False
    except Exception as e:
        print_fail("5.1", str(e))
        return False

def test_5_query_kb():
    """Test 5.2: Consultar KB"""
    try:
        response = requests.get(f"{BASE_URL}/catalog/knowledge-base?vendor_name=TestVendor6", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('total_documents', 0) > 0:
                print_pass("5.2: Consultar KB", f"Documentos: {result['total_documents']}")
                return True
        
        print_fail("5.2: Consultar KB")
        return False
    except Exception as e:
        print_fail("5.2", str(e))
        return False

# ==================================================
# MAIN
# ==================================================

def main():
    print(f"""{Color.CYAN}{Color.BOLD}
╔────────────────────────────────────────────────╗
║  🧪 SUITE DE PRUEBAS - 5 FUNCIONALIDADES       ║
║  located in: backed/tests/                    ║
╚────────────────────────────────────────────────╝
{Color.RESET}""")
    
    print(f"\n{Color.CYAN}Configuración:{Color.RESET}")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Test Data: {TEST_DATA_DIR}")
    
    # Verificar conectividad
    print(f"\n{Color.YELLOW}Verificando servidor...{Color.RESET}")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"{Color.GREEN}✅ Servidor accesible{Color.RESET}\n")
    except:
        print(f"{Color.RED}❌ No se puede conectar a {BASE_URL}{Color.RESET}")
        sys.exit(1)
    
    # Ejecutar pruebas
    tests = [
        test_1_valid_upload,
        test_1_missing_columns,
        test_2_upload_storage,
        test_2_preview,
        test_3_normalize,
        test_3_quality_report,
        test_4_save_to_db,
        test_4_query_products,
        test_5_build_kb,
        test_5_query_kb,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_fail(test.__name__, str(e))
            results.append(False)
    
    # Resumen
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print_section("RESUMEN")
    print(f"{Color.CYAN}Total:{Color.RESET}      {total}")
    print(f"{Color.GREEN}Pasadas:{Color.RESET}   {passed}")
    print(f"{Color.RED}Fallidas:{Color.RESET}   {total - passed}")
    print(f"{Color.YELLOW}Éxito:{Color.RESET}    {percentage:.0f}%\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
