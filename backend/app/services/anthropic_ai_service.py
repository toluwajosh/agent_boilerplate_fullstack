import logging
import os
import uuid
from typing import Dict, List, Optional

from anthropic import AsyncAnthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnthropicAIService:
    """
    AI Service for handling agent interactions using Anthropic's Claude API.
    """

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required"
            )

        self.client = AsyncAnthropic(api_key=api_key)

        # Configuration from environment
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        self.temperature = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "150"))

        logger.info(
            "AIService initialized with Anthropic model: %s", self.model
        )

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

            # Generate AI response using Anthropic
            ai_response = await self._generate_anthropic_response(
                conversation_id
            )

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

    async def _generate_anthropic_response(self, conversation_id: str) -> str:
        """
        Generate AI response using Anthropic's Claude API.

        Args:
            conversation_id: The conversation ID to get history for

        Returns:
            AI response string
        """
        try:
            # Get conversation history
            messages = self.conversations.get(conversation_id, [])

            # Anthropic uses system parameter separately from messages
            system_message = "You are a helpful AI assistant. Be concise, friendly, and helpful in your responses."

            # Call Anthropic API
            logger.info(
                "Calling Anthropic API with %d messages", len(messages)
            )

            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_message,
                messages=messages,
            )

            # Extract response content
            ai_response = response.content[0].text.strip()

            logger.info("Anthropic API response received successfully")
            return ai_response

        except Exception as e:
            logger.error("Error calling Anthropic API: %s", str(e))
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
