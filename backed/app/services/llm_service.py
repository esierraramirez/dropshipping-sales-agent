from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.schemas.llm_schema import LLMTestRequest
from app.core.config import settings


def generate_test_response(payload: LLMTestRequest) -> dict:
    adapter = OpenAIAdapter()

    system_prompt = (
        "Eres un asistente de ventas cordial y profesional. "
        "Responde de forma clara, útil y breve."
    )

    output = adapter.generate_reply(
        system_prompt=system_prompt,
        user_message=payload.message,
    )

    return {
        "model": settings.OPENAI_MODEL,
        "input_message": payload.message,
        "output_message": output,
    }
