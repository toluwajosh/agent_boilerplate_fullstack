import logging
import os
import uuid
from typing import Dict, List, Optional

import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiAIService:
    """
    AI Service for handling agent interactions using Google Gemini's API.
    """

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=api_key)

        # Configuration from environment
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        self.max_output_tokens = int(
            os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "150")
        )

        # Initialize the model
        generation_config = genai.types.GenerationConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
        )

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
        )

        logger.info(
            "AIService initialized with Gemini model: %s", self.model_name
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

            # Generate AI response using Gemini
            ai_response = await self._generate_gemini_response(conversation_id)

            # Add AI response to conversation history
            self.conversations[conversation_id].append(
                {"role": "model", "content": ai_response}
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

    async def _generate_gemini_response(self, conversation_id: str) -> str:
        """
        Generate AI response using Google Gemini's API.

        Args:
            conversation_id: The conversation ID to get history for

        Returns:
            AI response string
        """
        try:
            # Get conversation history
            messages = self.conversations.get(conversation_id, [])

            # Build conversation context for Gemini
            if len(messages) == 1:  # Only user message exists
                # Add system context for first message
                context = "You are a helpful AI assistant. Be concise, friendly, and helpful in your responses."
                prompt = (
                    f"{context}\n\nUser: {messages[0]['content']}\nAssistant:"
                )
            else:
                # Build conversation history
                prompt_parts = [
                    "You are a helpful AI assistant. Be concise, friendly, and helpful in your responses.\n"
                ]

                for msg in messages[:-1]:  # All except the last message
                    if msg["role"] == "user":
                        prompt_parts.append(f"User: {msg['content']}")
                    elif msg["role"] == "model":
                        prompt_parts.append(f"Assistant: {msg['content']}")

                # Add the current user message
                prompt_parts.append(f"User: {messages[-1]['content']}")
                prompt_parts.append("Assistant:")

                prompt = "\n".join(prompt_parts)

            # Call Gemini API
            logger.info("Calling Gemini API with conversation history")

            response = self.model.generate_content(prompt)

            # Extract response content
            ai_response = response.text.strip()

            logger.info("Gemini API response received successfully")
            return ai_response

        except Exception as e:
            logger.error("Error calling Gemini API: %s", str(e))
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
