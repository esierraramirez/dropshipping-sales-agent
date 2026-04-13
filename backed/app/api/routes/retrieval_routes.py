from fastapi import APIRouter, Depends

from app.api.deps import get_current_vendor
from app.models.vendor import Vendor
from app.schemas.retrieval_schema import RetrievalRequest, RetrievalResponse
from app.services.retrieval_service import retrieve_vendor_context

router = APIRouter()


@router.post("/retrieval/search", response_model=RetrievalResponse)
def retrieval_search(
    payload: RetrievalRequest,
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return retrieve_vendor_context(
        vendor=current_vendor,
        query=payload.query,
        top_k=payload.top_k
    )
