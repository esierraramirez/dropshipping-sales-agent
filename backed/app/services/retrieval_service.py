from pathlib import Path

from fastapi import HTTPException

from app.models.vendor import Vendor
from app.rag.retriever import retrieve_documents


def build_vendor_index_paths(vendor: Vendor) -> tuple[str, str]:
    vendor_slug = vendor.slug
    base_dir = Path("data/index") / vendor_slug

    kb_path = base_dir / "knowledge_base.jsonl"
    index_path = base_dir / "keyword_index.json"

    return str(kb_path), str(index_path)


def retrieve_vendor_context(vendor: Vendor, query: str, top_k: int = 3) -> dict:
    kb_path, index_path = build_vendor_index_paths(vendor)

    if not Path(kb_path).exists() or not Path(index_path).exists():
        raise HTTPException(
            status_code=404,
            detail="La base de conocimiento de esta empresa aún no ha sido construida."
        )

    results = retrieve_documents(
        query=query,
        kb_path=kb_path,
        index_path=index_path,
        top_k=top_k
    )

    return {
        "vendor_name": vendor.name,
        "query": query,
        "top_k": top_k,
        "total_matches": len(results),
        "results": results
    }


def build_context_block(results: list[dict]) -> str:
    """
    Convierte resultados recuperados en un bloque de contexto
    reutilizable por el orquestador.
    """
    if not results:
        return "No se encontraron productos relevantes en el catálogo."

    context_parts = []
    for idx, item in enumerate(results, start=1):
        context_parts.append(
            f"[Resultado {idx}]\n"
            f"Producto: {item.get('name', '')}\n"
            f"Categoría: {item.get('category', '')}\n"
            f"Contenido: {item.get('content', '')}\n"
        )

    return "\n".join(context_parts)
