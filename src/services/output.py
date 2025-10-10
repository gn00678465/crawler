"""Output handling service for saving or displaying scraped content."""
from pathlib import Path
import sys
from src.models.scrape import ScrapeResponse
from src.lib.exceptions import OutputError


class OutputService:
    """Service for writing scraped content to files or console."""

    def write_to_file(self, response: ScrapeResponse, file_path: str) -> None:
        """Write scraped content to file.

        Creates parent directories if they don't exist.

        Args:
            response: Scrape response with content
            file_path: Path where content will be saved

        Raises:
            OutputError: If file cannot be written
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(response.content, encoding='utf-8')
        except Exception as e:
            raise OutputError(f"Failed to write output file: {e}") from e

    def print_to_console(self, response: ScrapeResponse) -> None:
        """Print scraped content to stdout.

        Args:
            response: Scrape response with content
        """
        print(response.content)
