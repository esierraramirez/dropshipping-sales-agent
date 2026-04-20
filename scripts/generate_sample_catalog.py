"""
Script para generar un Excel de ejemplo con productos válidos
para probar el sistema de catálogos.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime

# Crear directorio si no existe
output_dir = Path(__file__).parent.parent / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

# Datos de ejemplo
sample_products = [
    {
        "product_id": "PROD001",
        "name": "Laptop Dell XPS 13",
        "category": "Electronics",
        "price": 999.99,
        "currency": "COP",
        "stock_status": "in_stock",
        "min_shipping_days": 2,
        "max_shipping_days": 5,
        "short_description": "Laptop ultraligera de 13 pulgadas",
        "full_description": "Laptop Dell XPS 13 pulgadas, procesador Intel i7, RAM 16GB, SSD 512GB, pantalla FHD",
        "brand": "Dell",
        "shipping_cost": 50000,
        "shipping_regions": "Colombia",
        "warranty_policy": "Garantía de 1 año",
        "specs": "Intel i7, 16GB RAM",
        "variants": "Gris, Plata"
    },
    {
        "product_id": "PROD002",
        "name": "iPhone 15 Pro",
        "category": "Electronics",
        "price": 1299.99,
        "currency": "COP",
        "stock_status": "in_stock",
        "min_shipping_days": 1,
        "max_shipping_days": 3,
        "short_description": "Smartphone Apple de última generación",
        "full_description": "iPhone 15 Pro con procesador A17 Pro, cámara de 48MP, pantalla OLED 6.1 pulgadas",
        "brand": "Apple",
        "shipping_cost": 45000,
        "shipping_regions": "Colombia, Venezuela",
        "warranty_policy": "Garantía de 1 año",
        "specs": "A17 Pro, 128GB",
        "variants": "Negro, Titanio matizado"
    },
    {
        "product_id": "PROD003",
        "name": "AirPods Pro Max",
        "category": "Electronics",
        "price": 549.99,
        "currency": "COP",
        "stock_status": "in_stock",
        "min_shipping_days": 3,
        "max_shipping_days": 7,
        "short_description": "Audífonos inalámbricos premium",
        "full_description": "AirPods Pro Max con cancelación de ruido activa, audio espacial, batería de 30 horas",
        "brand": "Apple",
        "shipping_cost": 35000,
        "shipping_regions": "Colombia",
        "warranty_policy": "Garantía de 1 año",
        "specs": "Bluetooth 5.3, cancelación activa",
        "variants": "Plateado, Negro, Azul"
    },
    {
        "product_id": "PROD004",
        "name": "Samsung Galaxy Watch 6",
        "category": "Electronics",
        "price": 399.99,
        "currency": "COP",
        "stock_status": "low_stock",
        "min_shipping_days": 2,
        "max_shipping_days": 4,
        "short_description": "Reloj inteligente con monitoreo de salud",
        "full_description": "Samsung Galaxy Watch 6 con pantalla AMOLED, medidor de oxígeno, ECG, resistente al agua",
        "brand": "Samsung",
        "shipping_cost": 25000,
        "shipping_regions": "Colombia",
        "warranty_policy": "Garantía de 1 año",
        "specs": "AMOLED 1.3\", Exynos W930",
        "variants": "Gris, Negro, Oro"
    },
    {
        "product_id": "PROD005",
        "name": "Sony WH-1000XM5",
        "category": "Electronics",
        "price": 449.99,
        "currency": "COP",
        "stock_status": "in_stock",
        "min_shipping_days": 1,
        "max_shipping_days": 2,
        "short_description": "Audífonos profesionales con cancelación de ruido",
        "full_description": "Audífonos Sony WH-1000XM5 con procesador de ruido de doble micrófono, batería 30 horas",
        "brand": "Sony",
        "shipping_cost": 30000,
        "shipping_regions": "Colombia, Ecuador",
        "warranty_policy": "Garantía de 2 años",
        "specs": "40Hz-40kHz, Cancelación activa",
        "variants": "Negro, Plata"
    },
    {
        "product_id": "PROD006",
        "name": "Tablet iPad Air",
        "category": "Electronics",
        "price": 599.99,
        "currency": "COP",
        "stock_status": "in_stock",
        "min_shipping_days": 3,
        "max_shipping_days": 5,
        "short_description": "Tablet potente para trabajo y entretenimiento",
        "full_description": "iPad Air con chip M1, pantalla Liquid Retina de 11 pulgadas, 256GB almacenamiento",
        "brand": "Apple",
        "shipping_cost": 40000,
        "shipping_regions": "Colombia",
        "warranty_policy": "Garantía de 1 año",
        "specs": "M1, 8GB RAM, 256GB",
        "variants": "Azul, Púrpura, Plateado"
    },
    {
        "product_id": "PROD007",
        "name": "Camera Canon EOS R5",
        "category": "Electronics",
        "price": 3999.99,
        "currency": "COP",
        "stock_status": "low_stock",
        "min_shipping_days": 5,
        "max_shipping_days": 10,
        "short_description": "Cámara profesional sin espejo de alta resolución",
        "full_description": "Canon EOS R5 con sensor full-frame de 45MP, grabación en 8K, autofoco con IA",
        "brand": "Canon",
        "shipping_cost": 80000,
        "shipping_regions": "Colombia",
        "warranty_policy": "Garantía de 2 años",
        "specs": "45MP, 8K 60fps, RF mount",
        "variants": "Negro"
    },
    {
        "product_id": "PROD008",
        "name": "Google Pixel 8",
        "category": "Electronics",
        "price": 799.99,
        "currency": "COP",
        "stock_status": "in_stock",
        "min_shipping_days": 2,
        "max_shipping_days": 4,
        "short_description": "Smartphone con IA y cámara inteligente",
        "full_description": "Google Pixel 8 con Tensor G3, cámara avanzada con IA, batería de 24 horas",
        "brand": "Google",
        "shipping_cost": 45000,
        "shipping_regions": "Colombia",
        "warranty_policy": "Garantía de 1 año",
        "specs": "Tensor G3, 8GB RAM, 128GB",
        "variants": "Negro, Blanco, Verde"
    },
]

# Crear DataFrame
df = pd.DataFrame(sample_products)

# Guardar en Excel
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"sample_catalog_{timestamp}.xlsx"
filepath = output_dir / filename

df.to_excel(filepath, index=False, sheet_name="Productos")

print(f"✅ Archivo generado exitosamente:")
print(f"📁 Ubicación: {filepath}")
print(f"📊 Productos: {len(df)}")
print(f"\nPuedes subirlo en la aplicación web:")
print(f"1. Ir a: http://localhost:5173/catalog")
print(f"2. Subir el archivo: {filename}")
print(f"3. Normalizar catálogo")
print(f"4. Guardar en base de datos")
