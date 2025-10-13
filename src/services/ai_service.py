"""
AI summarization service using LiteLLM.

This module provides the AIService class which wraps LiteLLM for generating
article summaries using various AI models.
"""

import logging
from typing import Optional
import litellm
from litellm.exceptions import (
    AuthenticationError as LiteLLMAuthError,
    BadRequestError as LiteLLMBadRequestError,
    RateLimitError as LiteLLMRateLimitError,
    ContextWindowExceededError as LiteLLMContextError,
    Timeout as LiteLLMTimeout,
    APIConnectionError as LiteLLMConnectionError,
)

from src.models.article_content import ArticleContent
from src.models.ai_model_config import AIModelConfiguration
from src.models.ai_summary import AISummary
from src.config.prompts import BRIEF_PROMPT, STANDARD_PROMPT, DETAILED_PROMPT
from src.lib.exceptions import (
    AIServiceError,
    RateLimitExceededError,
    TokenLimitExceededError,
    ModelNotFoundError,
)

logger = logging.getLogger(__name__)


class AIService:
    """
    Service for AI-powered article summarization using LiteLLM.

    This service wraps LiteLLM's completion API to generate summaries of articles.
    It handles prompt construction, API calls, error translation, and response parsing.

    Examples:
        >>> service = AIService()
        >>> article = ArticleContent(...)
        >>> config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
        >>> summary = service.summarize(article, config)
    """

    def __init__(self):
        """Initialize AIService."""
        # Configure LiteLLM logging if needed
        litellm.suppress_debug_info = True

    def summarize(
        self,
        article: ArticleContent,
        config: AIModelConfiguration,
        summary_length: str = "standard",
    ) -> AISummary:
        """
        Generate AI summary of article content.

        Args:
            article: Article content to summarize
            config: AI model configuration
            summary_length: Summary length mode ('brief', 'standard', 'detailed')

        Returns:
            AISummary object with generated summary and metadata

        Raises:
            AIServiceError: Generic AI service error
            RateLimitExceededError: Rate limit exceeded
            TokenLimitExceededError: Article too long for model
            ModelNotFoundError: Model not found or invalid

        Examples:
            >>> service = AIService()
            >>> article = ArticleContent(
            ...     url="https://example.com/article",
            ...     title="Test",
            ...     markdown="# Article\\n\\nContent...",
            ...     word_count=1000
            ... )
            >>> config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
            >>> summary = service.summarize(article, config, "brief")
        """
        try:
            # Get system prompt based on length
            system_prompt = self._get_system_prompt(summary_length)

            # Construct messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": article.markdown},
            ]

            # Set max_tokens based on length
            max_tokens = self._get_max_tokens(summary_length)

            logger.info(
                f"Calling AI service: model={config.full_name}, "
                f"length={summary_length}, article_words={article.word_count}"
            )

            # Call LiteLLM
            response = litellm.completion(
                model=config.full_name,
                messages=messages,
                temperature=0.3,  # Low temperature for factual summarization
                max_tokens=max_tokens,
            )

            # Extract summary and metadata
            summary_text = response.choices[0].message.content
            token_usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

            logger.info(
                f"AI summary generated: tokens={token_usage['total_tokens']}, "
                f"model={config.full_name}"
            )

            # Create AISummary object
            return AISummary(
                summary_text=summary_text,
                output_language=article.detected_language,
                length_mode=summary_length,
                model_used=config.full_name,
                token_usage=token_usage,
                source_url=str(article.url),
                source_title=article.title,
            )

        except LiteLLMAuthError as e:
            logger.error(f"Authentication error: {e}")
            raise AIServiceError(
                f"Missing or invalid API key for {config.provider}. "
                f"Please set {config.api_key_env_var} in your .env file.",
                code=2,
                details={"provider": config.provider, "model": config.full_name},
            )

        except LiteLLMRateLimitError as e:
            logger.warning(f"Rate limit exceeded: {e}")
            raise RateLimitExceededError(
                f"Rate limit exceeded for {config.provider}. Please try again later.",
                details={"provider": config.provider, "model": config.full_name},
            )

        except LiteLLMContextError as e:
            logger.warning(f"Context window exceeded: {e}")
            raise TokenLimitExceededError(
                f"Article is too long for {config.full_name} context window. "
                f"Try using 'brief' summary mode or a model with larger context.",
                details={"model": config.full_name, "article_word_count": article.word_count},
            )

        except LiteLLMBadRequestError as e:
            logger.error(f"Bad request error: {e}")
            # Check if it's a model not found error
            if "model" in str(e).lower() or "not found" in str(e).lower():
                raise ModelNotFoundError(
                    f"Model '{config.full_name}' not found or not supported.",
                    details={"model": config.full_name, "provider": config.provider},
                )
            raise AIServiceError(
                f"Invalid request to AI service: {str(e)}", details={"model": config.full_name}
            )

        except (LiteLLMTimeout, LiteLLMConnectionError) as e:
            logger.error(f"Network error: {e}")
            raise AIServiceError(
                f"Network error connecting to {config.provider}. Please check your connection.",
                details={"provider": config.provider, "error": str(e)},
            )

        except Exception as e:
            logger.error(f"Unexpected error in AI service: {e}")
            raise AIServiceError(
                f"Unexpected error during summarization: {str(e)}",
                details={"model": config.full_name, "error_type": type(e).__name__},
            )

    def _get_system_prompt(self, length: str) -> str:
        """Get system prompt based on summary length."""
        prompts = {"brief": BRIEF_PROMPT, "standard": STANDARD_PROMPT, "detailed": DETAILED_PROMPT}
        return prompts.get(length, STANDARD_PROMPT)

    def _get_max_tokens(self, length: str) -> int:
        """Get max tokens based on summary length."""
        token_limits = {"brief": 100, "standard": 300, "detailed": 600}
        return token_limits.get(length, 300)
