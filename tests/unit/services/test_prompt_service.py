"""
Unit tests for PromptService.

This module tests the prompt management service that provides
system prompts for different summary lengths.
"""

import pytest

from src.services.prompt_service import PromptService
from src.config.prompts import BRIEF_PROMPT, STANDARD_PROMPT, DETAILED_PROMPT


class TestPromptServiceGetSystemPrompt:
    """Test PromptService.get_system_prompt() method."""

    def test_get_system_prompt_brief(self):
        """Test that brief prompt is returned correctly."""
        service = PromptService()
        prompt = service.get_system_prompt("brief")

        assert prompt == BRIEF_PROMPT
        assert "1-2" in prompt or "brief" in prompt.lower()
        assert "concise" in prompt.lower() or "sentence" in prompt.lower()

    def test_get_system_prompt_standard(self):
        """Test that standard prompt is returned correctly."""
        service = PromptService()
        prompt = service.get_system_prompt("standard")

        assert prompt == STANDARD_PROMPT
        assert "3-5" in prompt or "key points" in prompt.lower()

    def test_get_system_prompt_detailed(self):
        """Test that detailed prompt is returned correctly."""
        service = PromptService()
        prompt = service.get_system_prompt("detailed")

        assert prompt == DETAILED_PROMPT
        assert "comprehensive" in prompt.lower() or "detailed" in prompt.lower()

    def test_get_system_prompt_invalid_raises_error(self):
        """Test that invalid length raises ValueError."""
        service = PromptService()

        with pytest.raises(ValueError) as exc_info:
            service.get_system_prompt("invalid")

        assert "invalid" in str(exc_info.value).lower()
        assert "brief" in str(exc_info.value)
        assert "standard" in str(exc_info.value)
        assert "detailed" in str(exc_info.value)

    def test_prompt_includes_language_detection(self):
        """Test that all prompts include language detection instructions."""
        service = PromptService()

        for length in ["brief", "standard", "detailed"]:
            prompt = service.get_system_prompt(length)
            # Check for language-related keywords
            assert "language" in prompt.lower() or "detect" in prompt.lower()


class TestPromptServiceValidation:
    """Test PromptService validation and edge cases."""

    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        service = PromptService()

        with pytest.raises(ValueError):
            service.get_system_prompt("")

    def test_none_raises_error(self):
        """Test that None raises appropriate error."""
        service = PromptService()

        with pytest.raises((ValueError, TypeError)):
            service.get_system_prompt(None)

    def test_case_sensitivity(self):
        """Test that length parameter is case-sensitive."""
        service = PromptService()

        # Should raise error for incorrect case
        with pytest.raises(ValueError):
            service.get_system_prompt("BRIEF")

        with pytest.raises(ValueError):
            service.get_system_prompt("Standard")

    def test_whitespace_not_trimmed(self):
        """Test that whitespace is not automatically trimmed."""
        service = PromptService()

        with pytest.raises(ValueError):
            service.get_system_prompt(" brief ")

        with pytest.raises(ValueError):
            service.get_system_prompt("brief ")


class TestPromptServiceConsistency:
    """Test PromptService consistency and determinism."""

    def test_same_prompt_returned_multiple_times(self):
        """Test that same prompt is returned on multiple calls."""
        service = PromptService()

        prompt1 = service.get_system_prompt("standard")
        prompt2 = service.get_system_prompt("standard")
        prompt3 = service.get_system_prompt("standard")

        assert prompt1 == prompt2 == prompt3

    def test_different_prompts_for_different_lengths(self):
        """Test that different lengths return different prompts."""
        service = PromptService()

        brief_prompt = service.get_system_prompt("brief")
        standard_prompt = service.get_system_prompt("standard")
        detailed_prompt = service.get_system_prompt("detailed")

        # All should be different
        assert brief_prompt != standard_prompt
        assert brief_prompt != detailed_prompt
        assert standard_prompt != detailed_prompt

    def test_prompts_are_non_empty(self):
        """Test that all prompts are non-empty strings."""
        service = PromptService()

        for length in ["brief", "standard", "detailed"]:
            prompt = service.get_system_prompt(length)
            assert isinstance(prompt, str)
            assert len(prompt) > 0
            assert prompt.strip() != ""

    def test_prompts_have_reasonable_length(self):
        """Test that prompts have reasonable length (not too short)."""
        service = PromptService()

        for length in ["brief", "standard", "detailed"]:
            prompt = service.get_system_prompt(length)
            # Prompts should be at least 50 characters
            assert len(prompt) >= 50


class TestPromptServiceMultipleInstances:
    """Test PromptService with multiple instances."""

    def test_multiple_instances_return_same_prompts(self):
        """Test that multiple instances return identical prompts."""
        service1 = PromptService()
        service2 = PromptService()

        assert service1.get_system_prompt("brief") == service2.get_system_prompt("brief")
        assert service1.get_system_prompt("standard") == service2.get_system_prompt("standard")
        assert service1.get_system_prompt("detailed") == service2.get_system_prompt("detailed")

    def test_instance_has_no_state(self):
        """Test that PromptService has no mutable state."""
        service = PromptService()

        # Call methods multiple times
        prompt1 = service.get_system_prompt("brief")
        prompt2 = service.get_system_prompt("standard")
        prompt3 = service.get_system_prompt("brief")

        # First and third should be identical
        assert prompt1 == prompt3
