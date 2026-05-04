from pathlib import Path
import unicodedata

from app.models.vendor import Vendor
from app.rag.retriever import load_knowledge_base, retrieve_documents


BROAD_CATALOG_PHRASES = (
    "catalogo",
    "catalog",
    "menu",
    "que venden",
    "que productos",
    "productos tienen",
    "productos manejan",
    "que tienen",
    "que opciones",
    "opciones tienen",
    "muestrame productos",
    "recomiendame algo",
)


def build_vendor_index_paths(vendor: Vendor) -> tuple[str, str]:
    vendor_slug = vendor.slug
    base_dir = Path("data/index") / vendor_slug

    kb_path = base_dir / "knowledge_base.jsonl"
    index_path = base_dir / "keyword_index.json"

    return str(kb_path), str(index_path)


def retrieve_vendor_context(vendor: Vendor, query: str, top_k: int = 3) -> dict:
    kb_path, index_path = build_vendor_index_paths(vendor)

    if not Path(kb_path).exists() or not Path(index_path).exists():
        return {
            "vendor_name": vendor.name,
            "query": query,
            "top_k": top_k,
            "total_matches": 0,
            "results": [],
            "knowledge_base_ready": False,
        }

    results = retrieve_documents(
        query=query,
        kb_path=kb_path,
        index_path=index_path,
        top_k=top_k,
    )

    # Si no hay resultados, siempre intenta cargar el preview del catálogo
    # porque es mejor mostrar algo que "no tengo información"
    if not results:
        results = _load_catalog_preview(kb_path=kb_path, top_k=top_k)

    if results:
        results = _augment_with_related_products(kb_path=kb_path, results=results, top_k=top_k)

    return {
        "vendor_name": vendor.name,
        "query": query,
        "top_k": top_k,
        "total_matches": len(results),
        "results": results,
        "knowledge_base_ready": True,
    }


def _is_broad_catalog_query(query: str) -> bool:
    query_normalized = _normalize_text(query)
    return any(phrase in query_normalized for phrase in BROAD_CATALOG_PHRASES)


def _contains_product_keywords(query: str) -> bool:
    """Detecta si la query menciona nombres de categorías de productos comunes"""
    product_keywords = {
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
        "suéter",
        "suéter",
        "abrigo",
        "abrigos",
        "chaqueta",
        "chaquetas",
        "zapato",
        "zapatos",
        "tenis",
        "camisa",
        "ropa",
        "prenda",
        "prendas",
        "outfit",
        "traje",
        "trajes",
        "sweater",
        "hoodie",
        "chaquetilla",
        "corbata",
        "interesado",
        "interesada",
    }
    query_normalized = _normalize_text(query)
    query_words = set(query_normalized.split())
    return bool(query_words & product_keywords)


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _load_catalog_preview(kb_path: str, top_k: int) -> list[dict]:
    documents = load_knowledge_base(kb_path)
    preview = []
    for document in documents[:top_k]:
        preview.append(
            {
                "product_id": document.get("product_id"),
                "name": document.get("name"),
                "category": document.get("category"),
                "score": 0,
                "content": document.get("content", ""),
            }
        )
    return preview


def _augment_with_related_products(
    kb_path: str,
    results: list[dict],
    top_k: int,
) -> list[dict]:
    if len(results) >= top_k:
        return results[:top_k]

    documents = load_knowledge_base(kb_path)
    selected_ids = {item.get("product_id") for item in results}
    categories = {item.get("category") for item in results if item.get("category")}

    augmented = list(results)
    for document in documents:
        if len(augmented) >= top_k:
            break
        if document.get("product_id") in selected_ids:
            continue
        if document.get("category") not in categories:
            continue

        augmented.append(
            {
                "product_id": document.get("product_id"),
                "name": document.get("name"),
                "category": document.get("category"),
                "score": 0,
                "content": document.get("content", ""),
            }
        )
        selected_ids.add(document.get("product_id"))

    return augmented[:top_k]


def build_context_block(results: list[dict]) -> str:
    """
    Convierte resultados recuperados en un bloque de contexto
    reutilizable por el orquestador.
    """
    if not results:
        return "No se encontraron productos relevantes en el catalogo."

    context_parts = []
    for idx, item in enumerate(results, start=1):
        context_parts.append(
            f"[Resultado {idx}]\n"
            f"Producto: {item.get('name', '')}\n"
            f"Categoria: {item.get('category', '')}\n"
            f"Contenido: {item.get('content', '')}\n"
        )

    return "\n".join(context_parts)
