import json
from pathlib import Path
from typing import List, Dict, Any


def save_knowledge_base_jsonl(documents: List[Dict[str, Any]], output_path: str) -> str:
    """
    Guarda los documentos en formato JSONL.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    return str(output)


def build_basic_keyword_index(documents: List[Dict[str, Any]], output_path: str) -> str:
    """
    Crea un índice simple por palabras clave.
    No es vectorial todavía, pero deja lista la estructura para búsqueda posterior.
    """
    index = []

    for doc in documents:
        keywords = set()
        text = doc.get("content", "").lower()

        for token in text.replace(",", " ").replace(".", " ").split():
            token = token.strip()
            if len(token) > 2:
                keywords.add(token)

        index.append({
            "product_id": doc.get("product_id"),
            "vendor_id": doc.get("vendor_id"),
            "name": doc.get("name"),
            "keywords": sorted(list(keywords))
        })

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return str(output)