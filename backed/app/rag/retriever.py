import json
import re
from pathlib import Path
from typing import List, Dict, Any


def tokenize(text: str) -> List[str]:
    """
    Convierte la consulta en tokens simples:
    - minúsculas
    - sin signos
    - elimina palabras muy cortas
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9áéíóúñüÁÉÍÓÚÑÜ\s]", " ", text)
    tokens = [token.strip() for token in text.split() if len(token.strip()) > 2]
    return tokens


def load_keyword_index(index_path: str) -> List[Dict[str, Any]]:
    path = Path(index_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el índice: {index_path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_knowledge_base(kb_path: str) -> List[Dict[str, Any]]:
    path = Path(kb_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe la base de conocimiento: {kb_path}")

    documents = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            documents.append(json.loads(line))
    return documents


def retrieve_documents(
    query: str,
    kb_path: str,
    index_path: str,
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Recupera documentos relevantes usando coincidencia por palabras clave.
    """
    query_tokens = tokenize(query)
    index_entries = load_keyword_index(index_path)
    kb_documents = load_knowledge_base(kb_path)

    # Mapa de product_id -> documento
    doc_map = {doc["product_id"]: doc for doc in kb_documents}

    matches: List[Dict[str, Any]] = []

    for entry in index_entries:
        product_keywords = set(entry.get("keywords", []))
        score = 0

        for token in query_tokens:
            if token in product_keywords:
                score += 1

        if score > 0:
            product_id = entry.get("product_id")
            document = doc_map.get(product_id)

            if document:
                matches.append({
                    "product_id": product_id,
                    "name": document.get("name"),
                    "category": document.get("category"),
                    "score": score,
                    "content": document.get("content", "")
                })

    # Ordenar por score descendente
    matches.sort(key=lambda item: item["score"], reverse=True)

    return matches[:top_k]
