from pydantic import BaseModel, Field


class LLMTestRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class LLMTestResponse(BaseModel):
    model: str
    input_message: str
    output_message: str
