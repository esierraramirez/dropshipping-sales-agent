from typing import Dict, Any


def product_to_document(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte un producto estructurado en un documento textual
    que servirá como base de conocimiento del agente.
    """
    content = f"""
    
Producto: {product.get('name', '')}
ID del producto: {product.get('product_id', '')}
Categoría: {product.get('category', '')}
Precio: {product.get('price', '')} {product.get('currency', '')}
Estado de stock: {product.get('stock_status', '')}
Tiempo de envío: {product.get('min_shipping_days', '')} a {product.get('max_shipping_days', '')} días
Descripción corta: {product.get('short_description', '')}
Descripción completa: {product.get('full_description', '')}
Marca: {product.get('brand', '')}
Costo de envío: {product.get('shipping_cost', '')}
Regiones de envío: {product.get('shipping_regions', '')}
Política de devoluciones: {product.get('returns_policy', '')}
Política de garantía: {product.get('warranty_policy', '')}
Especificaciones: {product.get('specs', '')}
Variantes: {product.get('variants', '')}
Proveedor: {product.get('source', '')}
""".strip()

    return {
        "product_id": product.get("product_id"),
        "vendor_id": product.get("vendor_id"),
        "name": product.get("name"),
        "category": product.get("category"),
        "content": content
    }