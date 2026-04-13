from typing import List, Optional
from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=10)


class RetrievedDocument(BaseModel):
    product_id: str
    name: Optional[str] = None
    category: Optional[str] = None
    score: int
    content: str


class RetrievalResponse(BaseModel):
    vendor_name: str
    query: str
    top_k: int
    total_matches: int
    results: List[RetrievedDocument]
