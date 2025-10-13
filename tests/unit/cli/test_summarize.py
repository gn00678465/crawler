"""
Unit tests for CLI summarize command.

This module tests the command-line interface for AI-powered
article summarization.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typer.testing import CliRunner
from pathlib import Path

from src.cli.summarize import app
from src.models.article_content import ArticleContent
from src.models.ai_summary import AISummary
from src.models.output_file import OutputFile


@pytest.fixture
def runner():
    """Fixture providing CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_article():
    """Fixture providing mock article content."""
    return ArticleContent(
        url="https://example.com/article",
        title="Test Article",
        markdown="# Test\n\nThis is a test article.",
        word_count=500,
        detected_language="en",
    )


@pytest.fixture
def mock_summary():
    """Fixture providing mock AI summary."""
    return AISummary(
        summary_text="This is a test summary of the article.",
        output_language="en",
        length_mode="standard",
        model_used="gemini/gemini-pro",
        token_usage={"prompt_tokens": 500, "completion_tokens": 50, "total_tokens": 550},
        source_url="https://example.com/article",
        source_title="Test Article",
    )


class TestSummarizeCommandBasicFlow:
    """Test basic execution flow of summarize command."""

    @patch("src.cli.summarize.Settings")
    @patch("src.cli.summarize.FirecrawlService")
    @patch("src.cli.summarize.AIService")
    def test_summarize_prints_to_console_by_default(
        self,
        mock_ai_service_class,
        mock_firecrawl_service_class,
        mock_settings_class,
        runner,
        mock_article,
        mock_summary,
    ):
        """Test that summary is printed to console when no output specified."""
        # Setup mocks
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings.google_api_key = "test-key"
        mock_settings_class.return_value = mock_settings

        mock_firecrawl = MagicMock()
        mock_firecrawl.scrape_to_article_content.return_value = mock_article
        mock_firecrawl_service_class.return_value = mock_firecrawl

        mock_ai = MagicMock()
        mock_ai.summarize.return_value = mock_summary
        mock_ai_service_class.return_value = mock_ai

        # Run command
        result = runner.invoke(app, ["--url", "https://example.com/article"])

        # Assertions
        assert result.exit_code == 0
        assert "This is a test summary" in result.stdout
        assert "Tokens used: 550" in result.stdout

    @patch("src.cli.summarize.Settings")
    @patch("src.cli.summarize.FirecrawlService")
    @patch("src.cli.summarize.AIService")
    @patch("src.cli.summarize.OutputService")
    def test_summarize_saves_to_file_when_output_specified(
        self,
        mock_output_service_class,
        mock_ai_service_class,
        mock_firecrawl_service_class,
        mock_settings_class,
        runner,
        mock_article,
        mock_summary,
    ):
        """Test that summary is saved to file when --output is specified."""
        # Setup mocks
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings.google_api_key = "test-key"
        mock_settings_class.return_value = mock_settings

        mock_firecrawl = MagicMock()
        mock_firecrawl.scrape_to_article_content.return_value = mock_article
        mock_firecrawl_service_class.return_value = mock_firecrawl

        mock_ai = MagicMock()
        mock_ai.summarize.return_value = mock_summary
        mock_ai_service_class.return_value = mock_ai

        mock_output = MagicMock()
        mock_output_file = OutputFile(file_path="summary.md", format="markdown", file_size=100)
        mock_output.save.return_value = mock_output_file
        mock_output_service_class.return_value = mock_output

        # Run command
        result = runner.invoke(
            app, ["--url", "https://example.com/article", "--output", "summary.md"]
        )

        # Assertions
        assert result.exit_code == 0
        assert "Summary saved to:" in result.stdout
        mock_output.save.assert_called_once()


class TestSummarizeCommandParameters:
    """Test command parameter handling."""

    @patch("src.cli.summarize.Settings")
    @patch("src.cli.summarize.FirecrawlService")
    @patch("src.cli.summarize.AIService")
    def test_summarize_uses_custom_model_when_specified(
        self,
        mock_ai_service_class,
        mock_firecrawl_service_class,
        mock_settings_class,
        runner,
        mock_article,
        mock_summary,
    ):
        """Test that --model parameter overrides default model."""
        # Setup mocks
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings.google_api_key = "test-key"
        mock_settings_class.return_value = mock_settings

        mock_firecrawl = MagicMock()
        mock_firecrawl.scrape_to_article_content.return_value = mock_article
        mock_firecrawl_service_class.return_value = mock_firecrawl

        mock_ai = MagicMock()
        mock_ai.summarize.return_value = mock_summary
        mock_ai_service_class.return_value = mock_ai

        # Run command with custom model
        result = runner.invoke(
            app, ["--url", "https://example.com/article", "--model", "gemini/gemini-1.5-flash"]
        )

        # Assertions
        assert result.exit_code == 0
        assert "Using model: gemini/gemini-1.5-flash" in result.stdout

    @patch("src.cli.summarize.Settings")
    @patch("src.cli.summarize.FirecrawlService")
    @patch("src.cli.summarize.AIService")
    def test_summarize_uses_custom_summary_length(
        self,
        mock_ai_service_class,
        mock_firecrawl_service_class,
        mock_settings_class,
        runner,
        mock_article,
        mock_summary,
    ):
        """Test that --summary parameter is passed to AI service."""
        # Setup mocks
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings.google_api_key = "test-key"
        mock_settings_class.return_value = mock_settings

        mock_firecrawl = MagicMock()
        mock_firecrawl.scrape_to_article_content.return_value = mock_article
        mock_firecrawl_service_class.return_value = mock_firecrawl

        mock_ai = MagicMock()
        mock_ai.summarize.return_value = mock_summary
        mock_ai_service_class.return_value = mock_ai

        # Run command with brief summary
        result = runner.invoke(app, ["--url", "https://example.com/article", "--summary", "brief"])

        # Assertions
        assert result.exit_code == 0
        mock_ai.summarize.assert_called_once()
        call_args = mock_ai.summarize.call_args
        assert call_args[1]["summary_length"] == "brief"


class TestSummarizeCommandErrorHandling:
    """Test error handling in summarize command."""

    @patch("src.cli.summarize.Settings")
    def test_summarize_fails_when_no_model_configured(self, mock_settings_class, runner):
        """Test that command fails when no AI model is configured."""
        # Setup mock with no model
        mock_settings = MagicMock()
        mock_settings.default_ai_model = None
        mock_settings_class.return_value = mock_settings

        # Run command
        result = runner.invoke(app, ["--url", "https://example.com/article"])

        # Assertions
        # Configuration errors should fail (typer sends errors to stderr which isn't captured by default)
        assert result.exit_code != 0  # Should fail

    @patch("src.cli.summarize.Settings")
    def test_summarize_fails_when_non_gemini_model_used(self, mock_settings_class, runner):
        """Test that command fails for non-Gemini models in P1."""
        # Setup mock
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings_class.return_value = mock_settings

        # Run command with OpenAI model
        result = runner.invoke(
            app, ["--url", "https://example.com/article", "--model", "openai/gpt-4"]
        )

        # Assertions
        assert result.exit_code != 0  # Should fail

    @patch("src.cli.summarize.Settings")
    def test_summarize_fails_when_api_key_missing(self, mock_settings_class, runner):
        """Test that command fails when API key is missing."""
        # Setup mock with no API key
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings.google_api_key = None
        mock_settings_class.return_value = mock_settings

        # Run command
        result = runner.invoke(app, ["--url", "https://example.com/article"])

        # Assertions
        assert result.exit_code != 0  # Should fail


class TestSummarizeCommandWarnings:
    """Test warning messages in summarize command."""

    @patch("src.cli.summarize.Settings")
    @patch("src.cli.summarize.FirecrawlService")
    @patch("src.cli.summarize.AIService")
    def test_summarize_warns_for_minimal_articles(
        self,
        mock_ai_service_class,
        mock_firecrawl_service_class,
        mock_settings_class,
        runner,
        mock_summary,
    ):
        """Test that command warns when article is very short."""
        # Setup mocks
        mock_settings = MagicMock()
        mock_settings.default_ai_model = "gemini/gemini-pro"
        mock_settings.google_api_key = "test-key"
        mock_settings_class.return_value = mock_settings

        # Create minimal article
        minimal_article = ArticleContent(
            url="https://example.com/short",
            title="Short",
            markdown="Short content.",
            word_count=50,  # Less than 100 words
            detected_language="en",
        )

        mock_firecrawl = MagicMock()
        mock_firecrawl.scrape_to_article_content.return_value = minimal_article
        mock_firecrawl_service_class.return_value = mock_firecrawl

        mock_ai = MagicMock()
        mock_ai.summarize.return_value = mock_summary
        mock_ai_service_class.return_value = mock_ai

        # Run command
        result = runner.invoke(app, ["--url", "https://example.com/short"])

        # Assertions
        assert result.exit_code == 0
        assert "Warning: Article is very short" in result.stdout or "50 words" in result.stdout
