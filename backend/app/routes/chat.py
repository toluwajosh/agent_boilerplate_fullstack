import logging

from fastapi import APIRouter, HTTPException, status

from ..models import ChatRequest, ChatResponse, ErrorResponse
from ..services.ai_service import ai_service

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Send message to AI agent",
    description="Send a message to the AI agent and receive a response. Optionally include a conversation ID to maintain context.",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for AI agent interactions.

    Args:
        request: ChatRequest containing message and optional conversation_id

    Returns:
        ChatResponse with AI response and conversation_id

    Raises:
        HTTPException: For various error conditions
    """
    try:
        # Validate message content
        if not request.message or request.message.strip() == "":
            logger.warning("Empty message received")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty",
            )

        # Process message through AI service
        logger.info(
            "Processing chat message for conversation: %s",
            request.conversation_id,
        )

        ai_response, conversation_id = await ai_service.process_message(
            message=request.message.strip(),
            conversation_id=request.conversation_id,
        )

        # Return successful response
        response = ChatResponse(
            response=ai_response, conversation_id=conversation_id
        )

        logger.info("Successfully processed chat request")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Handle unexpected errors
        logger.error("Unexpected error in chat endpoint: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while processing your request",
        ) from e


@router.get(
    "/health",
    summary="Health check for chat service",
    description="Check if the chat service is healthy and responsive",
)
async def health_check():
    """Health check endpoint for the chat service."""
    return {"status": "healthy", "service": "chat"}
