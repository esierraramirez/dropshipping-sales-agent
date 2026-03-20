from typing import List, Dict, Any
from pydantic import BaseModel


class CatalogNormalizationResponse(BaseModel):
    message: str
    vendor_name: str
    source_file: str
    processed_csv_path: str
    processed_jsonl_path: str
    quality_report_path: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    preview_rows: List[Dict[str, Any]]