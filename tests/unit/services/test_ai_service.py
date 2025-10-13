"""
Unit tests for AIService.

This module tests the AI summarization service that wraps LiteLLM.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

from src.services.ai_service import AIService
from src.models.article_content import ArticleContent
from src.models.ai_model_config import AIModelConfiguration
from src.models.ai_summary import AISummary
from src.lib.exceptions import (
    AIServiceError,
    RateLimitExceededError,
    TokenLimitExceededError,
    ModelNotFoundError,
)


@pytest.fixture
def sample_article():
    """Fixture providing sample article content."""
    return ArticleContent(
        url="https://example.com/article",
        title="Introduction to Python",
        markdown="# Python\n\nPython is a high-level programming language...",
        word_count=1500,
        detected_language="en",
    )


@pytest.fixture
def gemini_config():
    """Fixture providing Gemini model configuration."""
    return AIModelConfiguration.from_model_string("gemini/gemini-pro")


@pytest.fixture
def mock_litellm_response():
    """Fixture providing mock LiteLLM response."""
    # Create mock objects that behave like LiteLLM response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[
        0
    ].message.content = "This article introduces Python as a high-level programming language."
    mock_response.usage.prompt_tokens = 1500
    mock_response.usage.completion_tokens = 150
    mock_response.usage.total_tokens = 1650
    mock_response.model = "gemini/gemini-pro"
    return mock_response


class TestAIServiceSummarize:
    """Test AIService.summarize() core functionality."""

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_returns_ai_summary(
        self, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that summarize returns AISummary object."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        result = service.summarize(sample_article, gemini_config)

        assert isinstance(result, AISummary)
        assert (
            result.summary_text
            == "This article introduces Python as a high-level programming language."
        )
        assert result.model_used == "gemini/gemini-pro"
        assert result.source_url == str(sample_article.url)
        assert result.source_title == sample_article.title

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_uses_standard_length_by_default(
        self, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that summarize uses standard length prompt by default."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        service.summarize(sample_article, gemini_config)

        # Verify completion was called
        assert mock_completion.called
        call_args = mock_completion.call_args
        messages = call_args[1]["messages"]

        # Check system message contains standard prompt
        system_msg = messages[0]["content"]
        assert "3-5 key points" in system_msg

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_extracts_token_usage(
        self, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that summarize extracts token usage metadata."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        result = service.summarize(sample_article, gemini_config)

        assert result.token_usage is not None
        assert result.token_usage["prompt_tokens"] == 1500
        assert result.token_usage["completion_tokens"] == 150
        assert result.token_usage["total_tokens"] == 1650

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_includes_article_content_in_prompt(
        self, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that article markdown is included in user message."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        service.summarize(sample_article, gemini_config)

        call_args = mock_completion.call_args
        messages = call_args[1]["messages"]
        user_msg = messages[1]["content"]

        assert "Python is a high-level programming language" in user_msg

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_sets_model_in_request(
        self, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that correct model is specified in LiteLLM request."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        service.summarize(sample_article, gemini_config)

        call_args = mock_completion.call_args
        assert call_args[1]["model"] == "gemini/gemini-pro"

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_sets_temperature_for_factual_output(
        self, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that low temperature is used for factual summarization."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        service.summarize(sample_article, gemini_config)

        call_args = mock_completion.call_args
        # Temperature should be low (0.3 or similar) for factual output
        assert call_args[1]["temperature"] <= 0.5


class TestAIServiceErrorHandling:
    """Test AIService error handling and exception translation."""

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_authentication_error(
        self, mock_completion, sample_article, gemini_config
    ):
        """Test that AuthenticationError is translated correctly."""
        from litellm.exceptions import AuthenticationError as LiteLLMAuthError

        mock_completion.side_effect = LiteLLMAuthError("Invalid API key")

        service = AIService()
        with pytest.raises(AIServiceError) as exc_info:
            service.summarize(sample_article, gemini_config)

        assert "API key" in str(exc_info.value.message).lower()

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_rate_limit_error(
        self, mock_completion, sample_article, gemini_config
    ):
        """Test that RateLimitError is translated correctly."""
        from litellm.exceptions import RateLimitError as LiteLLMRateLimitError

        mock_completion.side_effect = LiteLLMRateLimitError("Rate limit exceeded")

        service = AIService()
        with pytest.raises(RateLimitExceededError) as exc_info:
            service.summarize(sample_article, gemini_config)

        assert exc_info.value.code == 3

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_token_limit_error(
        self, mock_completion, sample_article, gemini_config
    ):
        """Test that ContextWindowExceededError is translated."""
        from litellm.exceptions import ContextWindowExceededError as LiteLLMContextError

        mock_completion.side_effect = LiteLLMContextError("Context window exceeded")

        service = AIService()
        with pytest.raises(TokenLimitExceededError) as exc_info:
            service.summarize(sample_article, gemini_config)

        assert exc_info.value.code == 3
        assert "token limit" in str(exc_info.value.message).lower()

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_bad_request_error(
        self, mock_completion, sample_article, gemini_config
    ):
        """Test that BadRequestError for invalid model is translated."""
        from litellm.exceptions import BadRequestError as LiteLLMBadRequestError

        mock_completion.side_effect = LiteLLMBadRequestError(
            "Model not found", llm_provider="gemini", model="invalid-model"
        )

        service = AIService()
        with pytest.raises(ModelNotFoundError) as exc_info:
            service.summarize(sample_article, gemini_config)

        assert exc_info.value.code == 2

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_generic_api_error(
        self, mock_completion, sample_article, gemini_config
    ):
        """Test that generic API errors are wrapped in AIServiceError."""
        mock_completion.side_effect = Exception("Network error")

        service = AIService()
        with pytest.raises(AIServiceError) as exc_info:
            service.summarize(sample_article, gemini_config)

        assert "error" in str(exc_info.value.message).lower()


class TestAIServiceMultiLanguage:
    """Test multi-language article handling."""

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_chinese_article(self, mock_completion, gemini_config):
        """Test summarization of Chinese article."""
        chinese_article = ArticleContent(
            url="https://example.com/chinese",
            title="Python 入門",
            markdown="# Python\n\nPython 是一種高級編程語言...",
            word_count=1000,
            detected_language="zh",
        )

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "本文介紹了 Python 編程語言..."
        mock_response.usage.prompt_tokens = 1000
        mock_response.usage.completion_tokens = 100
        mock_response.usage.total_tokens = 1100
        mock_completion.return_value = mock_response

        service = AIService()
        result = service.summarize(chinese_article, gemini_config)

        assert result.summary_text == "本文介紹了 Python 編程語言..."
        # Verify system prompt instructs AI to respond in same language
        call_args = mock_completion.call_args
        system_msg = call_args[1]["messages"][0]["content"]
        assert "same language" in system_msg.lower() or "detect" in system_msg.lower()

    @patch("src.services.ai_service.litellm.completion")
    def test_summarize_handles_japanese_article(self, mock_completion, gemini_config):
        """Test summarization of Japanese article."""
        japanese_article = ArticleContent(
            url="https://example.com/japanese",
            title="Pythonの紹介",
            markdown="# Python\n\nPythonは高級プログラミング言語です...",
            word_count=1000,
            detected_language="ja",
        )

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "この記事はPythonを紹介しています..."
        mock_response.usage.prompt_tokens = 1000
        mock_response.usage.completion_tokens = 100
        mock_response.usage.total_tokens = 1100
        mock_completion.return_value = mock_response

        service = AIService()
        result = service.summarize(japanese_article, gemini_config)

        assert "Python" in result.summary_text


class TestAIServiceLogging:
    """Test AIService logging functionality."""

    @patch("src.services.ai_service.litellm.completion")
    @patch("src.services.ai_service.logger")
    def test_summarize_logs_api_call(
        self, mock_logger, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that API calls are logged."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        service.summarize(sample_article, gemini_config)

        # Verify logger was called
        assert mock_logger.info.called or mock_logger.debug.called

    @patch("src.services.ai_service.litellm.completion")
    @patch("src.services.ai_service.logger")
    def test_summarize_logs_token_usage(
        self, mock_logger, mock_completion, sample_article, gemini_config, mock_litellm_response
    ):
        """Test that token usage is logged."""
        mock_completion.return_value = mock_litellm_response

        service = AIService()
        service.summarize(sample_article, gemini_config)

        # Check if token usage was logged
        log_calls = [str(call) for call in mock_logger.info.call_args_list]
        assert any("token" in str(call).lower() for call in log_calls)
