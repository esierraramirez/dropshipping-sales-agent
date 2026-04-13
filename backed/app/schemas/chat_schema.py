from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=3000)


class ChatResponse(BaseModel):
    vendor_name: str
    user_message: str
    agent_response: str
    context_used: str
    matches_found: int
