"""
Unit tests for AISummary Pydantic model.

This module tests the validation rules and behavior of the AISummary model,
which represents an AI-generated article summary with metadata.
"""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from src.models.ai_summary import AISummary


class TestAISummaryValidation:
    """Test AISummary model validation rules."""

    def test_valid_instantiation_with_all_required_fields(self):
        """Test creating AISummary with all required fields."""
        summary = AISummary(
            summary_text="This article introduces Python as a high-level programming language.",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Introduction to Python",
        )

        assert summary.summary_text.startswith("This article")
        assert summary.length_mode == "standard"
        assert summary.model_used == "gemini/gemini-pro"
        assert summary.source_url == "https://example.com/article"
        assert summary.source_title == "Introduction to Python"
        assert summary.output_language is None
        assert summary.token_usage is None
        assert isinstance(summary.generation_timestamp, datetime)

    def test_valid_instantiation_with_all_fields(self):
        """Test creating AISummary with all optional fields."""
        token_usage = {"prompt_tokens": 1500, "completion_tokens": 150, "total_tokens": 1650}
        summary = AISummary(
            summary_text="Summary text",
            output_language="en",
            length_mode="brief",
            model_used="gemini/gemini-pro",
            token_usage=token_usage,
            source_url="https://example.com/article",
            source_title="Test Article",
        )

        assert summary.output_language == "en"
        assert summary.token_usage == token_usage

    def test_summary_text_required(self):
        """Test that summary_text is required."""
        with pytest.raises(ValidationError) as exc_info:
            AISummary(
                length_mode="standard",
                model_used="gemini/gemini-pro",
                source_url="https://example.com/article",
                source_title="Test",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("summary_text",) for error in errors)

    def test_length_mode_required(self):
        """Test that length_mode is required."""
        with pytest.raises(ValidationError) as exc_info:
            AISummary(
                summary_text="Summary",
                model_used="gemini/gemini-pro",
                source_url="https://example.com/article",
                source_title="Test",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("length_mode",) for error in errors)

    def test_model_used_required(self):
        """Test that model_used is required."""
        with pytest.raises(ValidationError) as exc_info:
            AISummary(
                summary_text="Summary",
                length_mode="standard",
                source_url="https://example.com/article",
                source_title="Test",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("model_used",) for error in errors)

    def test_source_url_required(self):
        """Test that source_url is required."""
        with pytest.raises(ValidationError) as exc_info:
            AISummary(
                summary_text="Summary",
                length_mode="standard",
                model_used="gemini/gemini-pro",
                source_title="Test",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("source_url",) for error in errors)

    def test_source_title_required(self):
        """Test that source_title is required."""
        with pytest.raises(ValidationError) as exc_info:
            AISummary(
                summary_text="Summary",
                length_mode="standard",
                model_used="gemini/gemini-pro",
                source_url="https://example.com/article",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("source_title",) for error in errors)

    def test_output_language_optional(self):
        """Test that output_language is optional."""
        summary = AISummary(
            summary_text="Summary",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.output_language is None

    def test_output_language_accepts_iso_codes(self):
        """Test that output_language accepts ISO 639-1 codes."""
        for lang in ["en", "zh", "ja", "es", "fr"]:
            summary = AISummary(
                summary_text="Summary",
                output_language=lang,
                length_mode="standard",
                model_used="gemini/gemini-pro",
                source_url="https://example.com/article",
                source_title="Test",
            )
            assert summary.output_language == lang

    def test_token_usage_optional(self):
        """Test that token_usage is optional."""
        summary = AISummary(
            summary_text="Summary",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.token_usage is None

    def test_token_usage_accepts_dict(self):
        """Test that token_usage accepts dictionary with token counts."""
        token_usage = {"prompt_tokens": 1500, "completion_tokens": 200, "total_tokens": 1700}
        summary = AISummary(
            summary_text="Summary",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            token_usage=token_usage,
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.token_usage["prompt_tokens"] == 1500
        assert summary.token_usage["completion_tokens"] == 200
        assert summary.token_usage["total_tokens"] == 1700

    def test_generation_timestamp_auto_generation(self):
        """Test that generation_timestamp is automatically generated."""
        before = datetime.now(timezone.utc)
        summary = AISummary(
            summary_text="Summary",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test",
        )
        after = datetime.now(timezone.utc)

        assert isinstance(summary.generation_timestamp, datetime)
        assert before <= summary.generation_timestamp <= after


class TestAISummaryLengthModes:
    """Test different summary length modes."""

    def test_brief_length_mode(self):
        """Test that brief length mode is accepted."""
        summary = AISummary(
            summary_text="Brief summary.",
            length_mode="brief",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.length_mode == "brief"

    def test_standard_length_mode(self):
        """Test that standard length mode is accepted."""
        summary = AISummary(
            summary_text="Standard summary with key points.",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.length_mode == "standard"

    def test_detailed_length_mode(self):
        """Test that detailed length mode is accepted."""
        summary = AISummary(
            summary_text="Detailed comprehensive summary.",
            length_mode="detailed",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.length_mode == "detailed"


class TestAISummarySerialization:
    """Test AISummary JSON serialization and deserialization."""

    def test_model_can_be_serialized_to_json(self):
        """Test that AISummary can be serialized to JSON."""
        summary = AISummary(
            summary_text="This is a summary",
            output_language="en",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Test Article",
        )

        json_data = summary.model_dump_json()
        assert isinstance(json_data, str)
        assert "summary" in json_data.lower()
        assert "gemini" in json_data

    def test_model_can_be_deserialized_from_dict(self):
        """Test that AISummary can be created from dict."""
        data = {
            "summary_text": "Summary text",
            "output_language": "en",
            "length_mode": "standard",
            "model_used": "gemini/gemini-pro",
            "token_usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            "generation_timestamp": "2025-10-12T10:32:15Z",
            "source_url": "https://example.com/article",
            "source_title": "Test Article",
        }

        summary = AISummary(**data)
        assert summary.summary_text == "Summary text"
        assert summary.output_language == "en"

    def test_model_round_trip_serialization(self):
        """Test that AISummary can be serialized and deserialized."""
        original = AISummary(
            summary_text="Original summary",
            output_language="en",
            length_mode="standard",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Original Title",
        )

        data = original.model_dump()
        reconstructed = AISummary(**data)

        assert reconstructed.summary_text == original.summary_text
        assert reconstructed.output_language == original.output_language
        assert reconstructed.length_mode == original.length_mode
        assert reconstructed.model_used == original.model_used


class TestAISummaryEdgeCases:
    """Test edge cases and special scenarios."""

    def test_summary_with_unicode_characters(self):
        """Test that summaries with Unicode characters are accepted."""
        summary = AISummary(
            summary_text="この記事はPythonについて説明しています。",
            output_language="ja",
            length_mode="brief",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Python入門",
        )
        assert "Python" in summary.summary_text

    def test_very_long_summary_text(self):
        """Test that very long summaries are accepted."""
        long_summary = "Summary. " * 1000
        summary = AISummary(
            summary_text=long_summary,
            length_mode="detailed",
            model_used="gemini/gemini-pro",
            source_url="https://example.com/article",
            source_title="Long Article",
        )
        assert len(summary.summary_text) > 5000

    def test_token_usage_with_large_numbers(self):
        """Test that token_usage handles large token counts."""
        token_usage = {"prompt_tokens": 50000, "completion_tokens": 10000, "total_tokens": 60000}
        summary = AISummary(
            summary_text="Summary",
            length_mode="detailed",
            model_used="gemini/gemini-pro",
            token_usage=token_usage,
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.token_usage["total_tokens"] == 60000

    def test_model_used_with_version_numbers(self):
        """Test that model_used accepts complex model identifiers."""
        summary = AISummary(
            summary_text="Summary",
            length_mode="standard",
            model_used="anthropic/claude-3-haiku-20240307",
            source_url="https://example.com/article",
            source_title="Test",
        )
        assert summary.model_used == "anthropic/claude-3-haiku-20240307"
