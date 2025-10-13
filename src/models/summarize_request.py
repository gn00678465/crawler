"""
Pydantic model for article summarization requests.

This module defines the SummarizeRequest model which represents user input
for the `crawler summarize` command.
"""

from typing import Optional, Literal
from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime, timezone


class SummarizeRequest(BaseModel):
    """
    Represents a request to summarize a web article.

    This model captures all parameters needed to crawl a web page and generate
    an AI-powered summary, including the target URL, AI model selection,
    summary verbosity level, and output options.

    Attributes:
        url: The web page URL to crawl and summarize. Must be a valid HTTP or HTTPS URL.
        model: AI model identifier in LiteLLM format (e.g., 'gemini/gemini-pro',
            'openai/gpt-4o'). If None, the default model from environment variable
            DEFAULT_AI_MODEL will be used.
        summary_length: Desired summary verbosity level. Must be one of:
            - 'brief': 1-2 sentence executive summary
            - 'standard': 3-5 key points (default)
            - 'detailed': Comprehensive summary with sections and details
        output_path: Optional file or directory path for saving summary. If None,
            summary is displayed to console. Can be:
            - File path: './summary.md' - saves to specific file
            - Directory path: './summaries/' - auto-generates filename
        save_original: Whether to save original markdown content alongside summary.
            Only applicable when output_path is provided. Default is False.
        timestamp: Request creation timestamp in UTC. Auto-generated.

    Examples:
        >>> # Basic request with minimal fields
        >>> request = SummarizeRequest(url="https://example.com/article")
        >>>
        >>> # Request with custom model and output
        >>> request = SummarizeRequest(
        ...     url="https://example.com/article",
        ...     model="gemini/gemini-1.5-flash",
        ...     summary_length="brief",
        ...     output_path="./summaries/"
        ... )
        >>>
        >>> # Request to save both original and summary
        >>> request = SummarizeRequest(
        ...     url="https://example.com/article",
        ...     output_path="./docs/",
        ...     save_original=True
        ... )
    """

    url: HttpUrl = Field(..., description="URL of article to summarize (HTTP/HTTPS only)")

    model: Optional[str] = Field(
        default=None,
        description="AI model in format 'provider/model-name' (e.g., 'gemini/gemini-pro'). "
        "If not specified, uses DEFAULT_AI_MODEL from environment.",
    )

    summary_length: Literal["brief", "standard", "detailed"] = Field(
        default="standard",
        description="Summary verbosity level: brief (1-2 sentences), "
        "standard (3-5 points), detailed (comprehensive)",
    )

    output_path: Optional[str] = Field(
        default=None,
        description="Output file or directory path. If None, prints to console. "
        "Directory paths (ending in /) auto-generate filenames.",
    )

    save_original: bool = Field(
        default=False,
        description="Save original markdown content alongside summary. "
        "Only used when output_path is provided.",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Request creation timestamp (UTC)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com/article",
                "model": "gemini/gemini-pro",
                "summary_length": "standard",
                "output_path": "./summaries/",
                "save_original": False,
            }
        }
    )
