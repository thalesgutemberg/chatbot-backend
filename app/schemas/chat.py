"""Chat API schemas."""

from pydantic import BaseModel, Field


class ChatInput(BaseModel):
    """Input schema for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=2000)
    thread_id: str = Field(..., min_length=1, max_length=100)


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str
    thread_id: str
