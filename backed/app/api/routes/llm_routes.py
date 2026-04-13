from fastapi import APIRouter

from app.schemas.llm_schema import LLMTestRequest, LLMTestResponse
from app.services.llm_service import generate_test_response

router = APIRouter()


@router.post("/llm/test", response_model=LLMTestResponse)
def test_llm(payload: LLMTestRequest):
    return generate_test_response(payload)
