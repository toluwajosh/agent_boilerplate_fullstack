import uuid
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(
        ..., min_length=1, max_length=5000, description="User message"
    )
    conversation_id: Optional[str] = Field(
        None, description="Optional conversation ID"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you?",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="AI agent response")
    conversation_id: str = Field(..., description="Conversation ID")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Hello! I'm doing well, thank you for asking.",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(
        None, description="Detailed error information"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "Message cannot be empty",
            }
        }
