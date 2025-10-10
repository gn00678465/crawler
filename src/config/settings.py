"""Configuration management using environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        firecrawl_api_url: Base URL of self-hosted Firecrawl API instance
        firecrawl_api_key: Optional API key for authentication
    """
    firecrawl_api_url: str
    firecrawl_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
