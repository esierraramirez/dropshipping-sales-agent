from typing import List, Dict, Any
from pydantic import BaseModel


class KnowledgeBaseBuildResponse(BaseModel):
    message: str
    vendor_name: str
    total_products: int
    documents_created: int
    knowledge_base_path: str
    index_path: str
    preview_documents: List[Dict[str, Any]]