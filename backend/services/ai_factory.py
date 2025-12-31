"""
AI Provider Factory
Creates the appropriate AI provider based on environment configuration
"""

import os
from typing import Optional
from dotenv import load_dotenv
from .ai_provider import BaseAIProvider
from .claude_provider import ClaudeProvider
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class AIProviderFactory:
    """
    Factory for creating AI provider instances.

    This class uses the singleton pattern to ensure only one AI provider
    instance exists throughout the application lifecycle.
    """

    _instance: Optional[BaseAIProvider] = None

    @classmethod
    def get_provider(cls) -> BaseAIProvider:
        """
        Get AI provider instance (singleton pattern).

        The provider is determined by the AI_PROVIDER environment variable.
        Supported providers: 'claude', 'openai'

        Returns:
            AI provider instance

        Raises:
            ValueError: If required environment variables are missing or provider is unknown
        """
        if cls._instance is None:
            cls._instance = cls._create_provider()
        return cls._instance

    @classmethod
    def _create_provider(cls) -> BaseAIProvider:
        """
        Create provider instance based on environment configuration.

        Returns:
            AI provider instance

        Raises:
            ValueError: If configuration is invalid
        """
        provider_name = os.getenv("AI_PROVIDER", "claude").lower()

        logger.info(f"Creating AI provider: {provider_name}")

        if provider_name == "claude":
            return cls._create_claude_provider()
        elif provider_name == "openai":
            return cls._create_openai_provider()
        else:
            raise ValueError(
                f"Unknown AI provider: {provider_name}. "
                f"Supported providers: 'claude', 'openai'"
            )

    @classmethod
    def _create_claude_provider(cls) -> BaseAIProvider:
        """Create Anthropic Claude provider"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your-anthropic-api-key-here":
            raise ValueError(
                "ANTHROPIC_API_KEY not found or not configured in environment. "
                "Please set a valid Anthropic API key in your .env file."
            )

        model = os.getenv("CLAUDE_MODEL", ClaudeProvider.DEFAULT_MODEL)
        logger.info(f"Using Claude model: {model}")

        return ClaudeProvider(api_key=api_key, model=model)

    @classmethod
    def _create_openai_provider(cls) -> BaseAIProvider:
        """Create OpenAI provider"""
        # Import here to avoid circular dependency and allow lazy loading
        from .openai_provider import OpenAIProvider

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
            raise ValueError(
                "OPENAI_API_KEY not found or not configured in environment. "
                "Please set a valid OpenAI API key in your .env file."
            )

        model = os.getenv("OPENAI_MODEL", OpenAIProvider.DEFAULT_MODEL)
        logger.info(f"Using OpenAI model: {model}")

        return OpenAIProvider(api_key=api_key, model=model)

    @classmethod
    async def validate_provider(cls) -> bool:
        """
        Validate provider configuration at startup.

        This method attempts to create and health-check the configured AI provider.

        Returns:
            True if provider is valid and accessible, False otherwise
        """
        try:
            provider = cls.get_provider()
            is_healthy = await provider.health_check()

            if is_healthy:
                logger.info(f"✓ AI provider validation successful: {provider.__class__.__name__}")
                return True
            else:
                logger.warning(f"⚠ AI provider health check failed: {provider.__class__.__name__}")
                return False

        except Exception as e:
            logger.error(f"✗ AI provider validation failed: {str(e)}")
            return False

    @classmethod
    def reset(cls):
        """
        Reset the singleton instance.

        This is primarily useful for testing when you need to switch providers
        or reload configuration.
        """
        cls._instance = None
        logger.info("AI provider instance reset")
