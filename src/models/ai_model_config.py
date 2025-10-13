"""
Pydantic model for AI model configuration.

This module defines the AIModelConfiguration model which parses AI model strings
and maps providers to their required API keys and configuration.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class AIModelConfiguration(BaseModel):
    """
    Represents a parsed AI model configuration.

    This model parses LiteLLM model identifiers and provides provider-specific
    configuration including API key requirements and local vs cloud model detection.

    Attributes:
        full_name: Complete model identifier in LiteLLM format (e.g., 'gemini/gemini-pro').
            Must follow 'provider/model-name' format with exactly one '/' separator.
        provider: Provider name extracted from full_name (e.g., 'gemini', 'openai', 'ollama').
        model_name: Model name without provider prefix (e.g., 'gemini-pro', 'gpt-4o').
        api_key_env_var: Environment variable name for API key (e.g., 'GOOGLE_API_KEY').
            None for local models (Ollama, vLLM) which don't require API keys.
        is_local: Whether this is a local model requiring no API key. True for
            Ollama and vLLM providers, False for cloud providers.

    Examples:
        >>> # Parse a Gemini model string
        >>> config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
        >>> config.provider
        'gemini'
        >>> config.api_key_env_var
        'GOOGLE_API_KEY'
        >>> config.is_local
        False
        >>>
        >>> # Parse a local Ollama model string
        >>> config = AIModelConfiguration.from_model_string("ollama/llama3")
        >>> config.provider
        'ollama'
        >>> config.api_key_env_var
        None
        >>> config.is_local
        True
    """

    full_name: str = Field(
        ..., description="Full LiteLLM model identifier (e.g., 'gemini/gemini-pro')"
    )

    provider: str = Field(..., description="Model provider (e.g., 'gemini', 'openai', 'ollama')")

    model_name: str = Field(
        ..., description="Model name without provider prefix (e.g., 'gemini-pro')"
    )

    api_key_env_var: Optional[str] = Field(
        default=None,
        description="Environment variable name for API key (e.g., 'GOOGLE_API_KEY'). "
        "None for local models.",
    )

    is_local: bool = Field(
        default=False, description="Whether this is a local model (no API key required)"
    )

    @field_validator("full_name")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """
        Ensure model name follows 'provider/model' format.

        Args:
            v: The full_name value to validate

        Returns:
            The validated full_name

        Raises:
            ValueError: If format is invalid
        """
        if "/" not in v:
            raise ValueError(f"Model name must be in format 'provider/model-name', got: {v}")

        parts = v.split("/")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f"Invalid model format. Expected 'provider/model-name', got: {v}")

        return v

    @classmethod
    def from_model_string(cls, model_string: str) -> "AIModelConfiguration":
        """
        Factory method to parse model string into configuration.

        This method parses a LiteLLM model identifier and automatically maps
        the provider to its corresponding API key environment variable.

        Args:
            model_string: LiteLLM model identifier (e.g., 'gemini/gemini-pro',
                'openai/gpt-4o', 'ollama/llama3')

        Returns:
            AIModelConfiguration instance with parsed provider, model name,
            API key variable name, and local model flag

        Examples:
            >>> config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
            >>> config.provider
            'gemini'
            >>> config.api_key_env_var
            'GOOGLE_API_KEY'
            >>>
            >>> config = AIModelConfiguration.from_model_string("ollama/llama3")
            >>> config.is_local
            True
            >>> config.api_key_env_var
            None
        """
        provider, model_name = model_string.split("/", 1)

        # Map provider to API key environment variable
        # This mapping follows LiteLLM conventions and common provider patterns
        api_key_map = {
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "ollama": None,  # Local, no API key
            "vllm": None,  # Local, no API key
        }

        is_local = provider in ["ollama", "vllm"]
        api_key_env_var = api_key_map.get(provider)

        return cls(
            full_name=model_string,
            provider=provider,
            model_name=model_name,
            api_key_env_var=api_key_env_var,
            is_local=is_local,
        )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "gemini/gemini-pro",
                "provider": "gemini",
                "model_name": "gemini-pro",
                "api_key_env_var": "GOOGLE_API_KEY",
                "is_local": False,
            }
        }
    )
