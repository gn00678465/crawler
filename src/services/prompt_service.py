"""
Service for managing AI system prompts.

This module provides the PromptService class which manages
system prompts for different summary lengths.
"""

from src.config.prompts import BRIEF_PROMPT, STANDARD_PROMPT, DETAILED_PROMPT


class PromptService:
    """
    Service for retrieving and managing system prompts.

    This service provides access to pre-configured system prompts
    for different summary length modes. It ensures consistent
    prompt usage across the application.

    Examples:
        >>> service = PromptService()
        >>> prompt = service.get_system_prompt("standard")
        >>> print(prompt[:50])
        You are a helpful summarizer. Summarize the fol...
    """

    def get_system_prompt(self, length: str) -> str:
        """
        Get system prompt for the specified summary length.

        Args:
            length: Summary length mode ('brief', 'standard', 'detailed')

        Returns:
            System prompt string

        Raises:
            ValueError: If length is invalid or not supported

        Examples:
            >>> service = PromptService()
            >>> brief = service.get_system_prompt("brief")
            >>> assert "1-2" in brief
            >>> standard = service.get_system_prompt("standard")
            >>> assert "3-5" in standard
        """
        prompts = {"brief": BRIEF_PROMPT, "standard": STANDARD_PROMPT, "detailed": DETAILED_PROMPT}

        if length not in prompts:
            raise ValueError(
                f"Invalid summary length: {length}. Must be one of: {', '.join(prompts.keys())}"
            )

        return prompts[length]
