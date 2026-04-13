from openai import OpenAI
from fastapi import HTTPException

from app.core.config import settings


class OpenAIAdapter:
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada en variables de entorno.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate_reply(self, system_prompt: str, user_message: str) -> str:
        """
        Genera una respuesta usando la Responses API de OpenAI.
        """
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )

            return response.output_text.strip()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar respuesta con OpenAI: {str(e)}",
            )
