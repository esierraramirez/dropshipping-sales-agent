from typing import List, Dict, Any
from pydantic import BaseModel


class CatalogUploadResponse(BaseModel):
    message: str
    vendor_name: str
    original_filename: str
    saved_path: str
    detected_columns: List[str]
    missing_required_columns: List[str]
    preview_rows: List[Dict[str, Any]]
    total_rows: int
    is_valid: bool