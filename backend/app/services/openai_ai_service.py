import logging
import os
import uuid
from typing import Dict, List, Optional

from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIAIService:
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
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
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
                temperature=self.temperature,
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
