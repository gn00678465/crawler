"""
Pydantic model for AI-generated summaries.

This module defines the AISummary model which represents an AI-generated
article summary with associated metadata.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone


class AISummary(BaseModel):
    """
    Represents an AI-generated article summary.

    This model encapsulates the result of AI summarization, including the generated
    summary text, metadata about the generation process (model used, token usage),
    and references to the source article.

    Attributes:
        summary_text: The generated summary content. This is the main output from
            the AI model, formatted according to the requested length mode.
        output_language: ISO 639-1 language code of the summary (e.g., 'en', 'zh', 'ja').
            Should match the source article language. Optional.
        length_mode: Which summary length mode was used ('brief', 'standard', 'detailed').
        model_used: Full AI model identifier that generated this summary
            (e.g., 'gemini/gemini-pro', 'openai/gpt-4o').
        token_usage: Token count metadata from the AI service. Optional dictionary
            containing 'prompt_tokens', 'completion_tokens', and 'total_tokens'.
        generation_timestamp: UTC timestamp when the summary was generated. Auto-generated.
        source_url: Original article URL that was summarized.
        source_title: Original article title.

    Examples:
        >>> # Create AISummary with minimal fields
        >>> summary = AISummary(
        ...     summary_text="This article introduces Python programming...",
        ...     length_mode="standard",
        ...     model_used="gemini/gemini-pro",
        ...     source_url="https://example.com/article",
        ...     source_title="Introduction to Python"
        ... )
        >>>
        >>> # Create with token usage metadata
        >>> summary = AISummary(
        ...     summary_text="Summary text",
        ...     output_language="en",
        ...     length_mode="brief",
        ...     model_used="gemini/gemini-pro",
        ...     token_usage={
        ...         "prompt_tokens": 1500,
        ...         "completion_tokens": 150,
        ...         "total_tokens": 1650
        ...     },
        ...     source_url="https://example.com/article",
        ...     source_title="Article Title"
        ... )
    """

    summary_text: str = Field(..., description="Generated summary content")

    output_language: Optional[str] = Field(
        default=None, description="ISO 639-1 language code of summary (e.g., 'en', 'zh')"
    )

    length_mode: str = Field(
        ..., description="Summary length mode used ('brief', 'standard', 'detailed')"
    )

    model_used: str = Field(..., description="AI model identifier (e.g., 'gemini/gemini-pro')")

    token_usage: Optional[dict] = Field(
        default=None,
        description="Token usage stats (prompt_tokens, completion_tokens, total_tokens)",
    )

    generation_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the summary was generated (UTC)",
    )

    source_url: str = Field(..., description="Original article URL")

    source_title: str = Field(..., description="Original article title")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "summary_text": "This article introduces Python as a high-level programming language...",
                "output_language": "en",
                "length_mode": "standard",
                "model_used": "gemini/gemini-pro",
                "token_usage": {
                    "prompt_tokens": 1500,
                    "completion_tokens": 150,
                    "total_tokens": 1650,
                },
                "generation_timestamp": "2025-10-12T10:32:15Z",
                "source_url": "https://example.com/article",
                "source_title": "Introduction to Python",
            }
        }
    )
