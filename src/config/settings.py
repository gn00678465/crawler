"""Configuration management using environment variables."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        firecrawl_api_url: Base URL of self-hosted Firecrawl API instance
        firecrawl_api_key: Optional API key for authentication
        default_ai_model: Default AI model in LiteLLM format (e.g., 'gemini/gemini-pro')
        google_api_key: Google API key for Gemini models
    """

    # Firecrawl settings
    firecrawl_api_url: str
    firecrawl_api_key: str = ""

    # AI Model settings (P1: Gemini only)
    default_ai_model: Optional[str] = None
    google_api_key: Optional[str] = None

    # P2 providers (will be enabled in future phases)
    # openai_api_key: Optional[str] = None
    # anthropic_api_key: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )
