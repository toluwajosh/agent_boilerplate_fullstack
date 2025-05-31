import asyncio
import logging
import os
import uuid
from typing import Dict, List, Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

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


class AIService:
    """
    AI Service for handling agent interactions using OpenAI's API.
    """

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = AsyncOpenAI(api_key=api_key)

        # Configuration from environment
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        # self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "150"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

        logger.info("AIService initialized with OpenAI model: %s", self.model)

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
                {"role": "user", "content": message}
            )

            # Generate AI response using OpenAI
            ai_response = await self._generate_openai_response(conversation_id)

            # Add AI response to conversation history
            self.conversations[conversation_id].append(
                {"role": "assistant", "content": ai_response}
            )

            logger.info(
                "Successfully processed message for conversation %s",
                conversation_id,
            )
            return ai_response, conversation_id

        except Exception as e:
            logger.error("Error processing message: %s", str(e))
            # Return a fallback message instead of raising an exception
            fallback_response = "I apologize, but I'm experiencing some technical difficulties right now. Please try again in a moment."
            return fallback_response, conversation_id or str(uuid.uuid4())

    async def _generate_openai_response(self, conversation_id: str) -> str:
        """
        Generate AI response using OpenAI's Chat Completion API.

        Args:
            conversation_id: The conversation ID to get history for

        Returns:
            AI response string
        """
        try:
            # Get conversation history
            messages = self.conversations.get(conversation_id, [])

            # Add system message if this is the start of conversation
            if len(messages) == 1:  # Only user message exists
                system_message = {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Be concise, friendly, and helpful in your responses.",
                }
                messages = [system_message] + messages

            # Call OpenAI API
            logger.info("Calling OpenAI API with %d messages", len(messages))

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                # max_tokens=self.max_tokens,
                temperature=self.temperature,
                # top_p=1.0,
                # frequency_penalty=0.0,
                # presence_penalty=0.0,
            )

            # Extract response content
            ai_response = response.choices[0].message.content.strip()

            logger.info("OpenAI API response received successfully")
            return ai_response

        except Exception as e:
            logger.error("Error calling OpenAI API: %s", str(e))
            raise Exception("Failed to generate AI response") from e

    def get_conversation_history(
        self, conversation_id: str
    ) -> List[Dict[str, str]]:
        """
        Get conversation history for a given conversation ID.

        Args:
            conversation_id: The conversation ID

        Returns:
            List of conversation messages
        """
        return self.conversations.get(conversation_id, [])

    def clear_conversation(self, conversation_id: str) -> bool:
        """
        Clear conversation history for a given conversation ID.

        Args:
            conversation_id: The conversation ID to clear

        Returns:
            True if conversation was cleared, False if it didn't exist
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info("Cleared conversation %s", conversation_id)
            return True
        return False


# Global AI service instance
try:
    ai_service = AIService()
    logger.info("Using OpenAI-powered AIService")
except ValueError as e:
    logger.warning(
        "OpenAI API key not configured, falling back to DummyAIService: %s", e
    )
    ai_service = DummyAIService()
except Exception as e:
    logger.error(
        "Failed to initialize AIService, falling back to DummyAIService: %s", e
    )
    ai_service = DummyAIService()
