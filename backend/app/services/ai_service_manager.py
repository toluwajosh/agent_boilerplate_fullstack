import logging
import os
from typing import Optional, Union

from dotenv import load_dotenv

from .anthropic_ai_service import AnthropicAIService
from .dummy_ai_service import DummyAIService
from .gemini_ai_service import GeminiAIService
from .openai_ai_service import OpenAIAIService

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type alias for AI services
AIServiceType = Union[
    OpenAIAIService, GeminiAIService, AnthropicAIService, DummyAIService
]


class AIServiceManager:
    """
    Manager class for dynamically selecting and initializing AI services.
    """

    def __init__(self):
        self._service: Optional[AIServiceType] = None
        self._service_name: str = ""

    def get_service(self) -> AIServiceType:
        """
        Get the currently active AI service, initializing if necessary.
        """
        if self._service is None:
            self._service = self._initialize_service()
        return self._service

    def _initialize_service(self) -> AIServiceType:
        """
        Initialize the appropriate AI service based on configuration and availability.
        """
        # Get preferred service from environment
        preferred_service = os.getenv("AI_SERVICE", "openai").lower()

        # Try to initialize services in order of preference
        services_to_try = [preferred_service]

        # Add fallback services if the preferred one fails
        if preferred_service != "openai":
            services_to_try.append("openai")
        if preferred_service != "gemini":
            services_to_try.append("gemini")
        if preferred_service != "anthropic":
            services_to_try.append("anthropic")

        # Always add dummy as final fallback
        services_to_try.append("dummy")

        for service_name in services_to_try:
            try:
                service = self._create_service(service_name)
                if service:
                    self._service_name = service_name
                    logger.info(
                        "Successfully initialized %s AI service",
                        service_name.upper(),
                    )
                    return service
            except Exception as e:
                logger.warning(
                    "Failed to initialize %s service: %s",
                    service_name.upper(),
                    e,
                )
                continue

        # This should never happen since dummy service should always work
        raise RuntimeError("Failed to initialize any AI service")

    def _create_service(self, service_name: str) -> Optional[AIServiceType]:
        """
        Create a specific AI service instance.
        """
        if service_name == "openai":
            return OpenAIAIService()
        elif service_name == "gemini":
            return GeminiAIService()
        elif service_name == "anthropic":
            return AnthropicAIService()
        elif service_name == "dummy":
            return DummyAIService()
        else:
            logger.warning("Unknown AI service: %s", service_name)
            return None

    def get_service_name(self) -> str:
        """
        Get the name of the currently active service.
        """
        if self._service is None:
            self.get_service()  # Initialize if needed
        return self._service_name

    def switch_service(self, service_name: str) -> bool:
        """
        Switch to a different AI service.

        Args:
            service_name: Name of the service to switch to

        Returns:
            True if switch was successful, False otherwise
        """
        try:
            new_service = self._create_service(service_name.lower())
            if new_service:
                self._service = new_service
                self._service_name = service_name.lower()
                logger.info("Switched to %s AI service", service_name.upper())
                return True
        except Exception as e:
            logger.error(
                "Failed to switch to %s service: %s", service_name.upper(), e
            )

        return False

    def get_available_services(self) -> list[str]:
        """
        Get list of available AI services based on API key configuration.
        """
        available = []

        # Check which API keys are configured
        if os.getenv("OPENAI_API_KEY"):
            available.append("openai")
        if os.getenv("GEMINI_API_KEY"):
            available.append("gemini")
        if os.getenv("ANTHROPIC_API_KEY"):
            available.append("anthropic")

        # Dummy is always available
        available.append("dummy")

        return available


# Global AI service manager instance
ai_service_manager = AIServiceManager()

# For backward compatibility, provide a direct service instance
ai_service = ai_service_manager.get_service()
