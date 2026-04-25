import json
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Any


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in text if not unicodedata.combining(char))


def tokenize(text: str) -> List[str]:
    """
    Convierte la consulta en tokens simples:
    - minúsculas
    - sin signos
    - elimina palabras muy cortas
    """
    text = normalize_text(text)
    text = re.sub(r"[^a-zA-Z0-9ñü\s]", " ", text)
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
        product_keywords = {normalize_text(keyword) for keyword in entry.get("keywords", [])}
        score = 0

        for token in query_tokens:
            if token in product_keywords:
                score += 1

        if score > 0:
            product_id = entry.get("product_id")
            document = doc_map.get(product_id)

            if document:
                searchable_name = normalize_text(document.get("name") or "")
                searchable_category = normalize_text(document.get("category") or "")
                searchable_product_id = normalize_text(product_id or "")

                for token in query_tokens:
                    if token in searchable_name:
                        score += 5
                    if token in searchable_category:
                        score += 3
                    if token in searchable_product_id:
                        score += 2

                matches.append({
                    "product_id": product_id,
                    "name": document.get("name"),
                    "category": document.get("category"),
                    "score": score,
                    "content": document.get("content", "")
                })

    # Ordenar por score descendente
    matches.sort(key=lambda item: item["score"], reverse=True)

    strong_matches = [item for item in matches if item["score"] >= 4]
    if strong_matches:
        return strong_matches[:top_k]

    return matches[:top_k]
