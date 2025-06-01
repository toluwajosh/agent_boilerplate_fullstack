import asyncio
import logging
import uuid
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DummyAIService:
    """
    AI Service for handling agent interactions.
    This is a mock implementation that can be extended with real AI services.
    """

    def __init__(self):
        self.conversations: Dict[str, list] = {}

    async def process_message(
        self, message: str, conversation_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Process a user message and return AI response with conversation ID.

        Args:
            message: User message to process
            conversation_id: Optional conversation ID

        Returns:
            Tuple of (ai_response, conversation_id)
        """
        try:
            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = str(uuid.uuid4())

            # Initialize conversation history if new
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []

            # Add user message to conversation history
            self.conversations[conversation_id].append(
                {"role": "user", "message": message}
            )

            # Simulate AI processing time
            await asyncio.sleep(0.5)

            # Generate mock AI response
            ai_response = await self._generate_response(
                message, conversation_id
            )

            # Add AI response to conversation history
            self.conversations[conversation_id].append(
                {"role": "assistant", "message": ai_response}
            )

            logger.info(
                "Successfully processed message for conversation %s",
                conversation_id,
            )
            return ai_response, conversation_id

        except Exception as e:
            logger.error("Error processing message: %s", str(e))
            raise Exception("Failed to process message") from e

    async def _generate_response(
        self, message: str, conversation_id: str
    ) -> str:
        """
        Generate AI response. This is a mock implementation.
        Replace this method with actual AI service integration.
        """
        # Simple mock responses based on message content
        message_lower = message.lower()

        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! How can I assist you today?"

        elif "how are you" in message_lower:
            return "I'm doing well, thank you for asking! How can I help you?"

        elif "goodbye" in message_lower or "bye" in message_lower:
            return "Goodbye! Feel free to chat with me anytime."

        elif "help" in message_lower:
            return "I'm here to help! You can ask me questions or just have a conversation. What would you like to know?"

        elif "name" in message_lower:
            return "I'm an AI assistant created to help answer questions and have conversations. What's your name?"

        else:
            # Generic response for other messages
            conversation_length = len(
                self.conversations.get(conversation_id, [])
            )
            responses = [
                f"That's interesting! I understand you said: '{message}'. Could you tell me more about that?",
                f"Thanks for sharing that with me. I find your message about '{message[:50]}...' quite engaging.",
                f"I appreciate your message. As an AI assistant, I'm here to help with any questions you might have.",
                f"That's a thoughtful message. Is there anything specific you'd like to know or discuss further?",
                f"Thank you for the conversation! I'm enjoying our chat. What else would you like to talk about?",
            ]

            # Rotate responses based on conversation length
            return responses[conversation_length % len(responses)]
