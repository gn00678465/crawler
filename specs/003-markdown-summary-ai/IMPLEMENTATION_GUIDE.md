# Implementation Guide: Remaining Tasks for AI Summarization Feature

**Feature**: `003-markdown-summary-ai`
**Status**: 43% Complete (20/47 tasks)
**Remaining**: 27 tasks for full implementation, 6 tasks for MVP

---

## Quick Start: Complete MVP (6 Tasks)

### T021-T022: Prompt Service

**Files to Create**:
1. `tests/unit/services/test_prompt_service.py`
2. `src/services/prompt_service.py`

**Implementation**:

```python
# tests/unit/services/test_prompt_service.py
import pytest
from src.services.prompt_service import PromptService

def test_get_system_prompt_brief():
    service = PromptService()
    prompt = service.get_system_prompt("brief")
    assert "1-2 sentences" in prompt or "brief" in prompt.lower()

def test_get_system_prompt_standard():
    service = PromptService()
    prompt = service.get_system_prompt("standard")
    assert "3-5" in prompt or "key points" in prompt.lower()

def test_get_system_prompt_detailed():
    service = PromptService()
    prompt = service.get_system_prompt("detailed")
    assert "comprehensive" in prompt.lower() or "detailed" in prompt.lower()

def test_get_system_prompt_invalid_raises_error():
    service = PromptService()
    with pytest.raises(ValueError):
        service.get_system_prompt("invalid")

def test_prompt_includes_language_detection():
    service = PromptService()
    prompt = service.get_system_prompt("standard")
    assert "language" in prompt.lower() or "detect" in prompt.lower()
```

```python
# src/services/prompt_service.py
"""Service for managing AI system prompts."""

from src.config.prompts import BRIEF_PROMPT, STANDARD_PROMPT, DETAILED_PROMPT


class PromptService:
    """Service for retrieving and managing system prompts."""

    def get_system_prompt(self, length: str) -> str:
        """
        Get system prompt for the specified summary length.

        Args:
            length: Summary length ('brief', 'standard', 'detailed')

        Returns:
            System prompt string

        Raises:
            ValueError: If length is invalid
        """
        prompts = {
            "brief": BRIEF_PROMPT,
            "standard": STANDARD_PROMPT,
            "detailed": DETAILED_PROMPT
        }

        if length not in prompts:
            raise ValueError(
                f"Invalid summary length: {length}. "
                f"Must be one of: {', '.join(prompts.keys())}"
            )

        return prompts[length]
```

**Run Tests**:
```bash
uv run pytest tests/unit/services/test_prompt_service.py -v
```

**Mark Complete**: Edit `tasks.md` and add `[X]` to T021 and T022.

---

### T023-T024: CLI Summarize Command

**Files to Create**:
1. `tests/unit/cli/test_summarize.py`
2. `src/cli/summarize.py`

**Implementation**:

```python
# src/cli/summarize.py
"""CLI command for AI-powered article summarization."""

import sys
import typer
from typing import Optional
from pathlib import Path

from src.models.summarize_request import SummarizeRequest
from src.models.ai_model_config import AIModelConfiguration
from src.services.firecrawl import FirecrawlService
from src.services.ai_service import AIService
from src.services.output import OutputService
from src.config.settings import Settings
from src.lib.exceptions import (
    CrawlerError,
    ConfigurationError,
    AIServiceError
)

app = typer.Typer()


@app.command()
def summarize(
    url: str = typer.Option(..., "--url", help="Article URL to summarize"),
    model: Optional[str] = typer.Option(None, "--model", help="AI model (e.g., gemini/gemini-pro)"),
    summary: str = typer.Option("standard", "--summary", help="Summary length: brief, standard, detailed"),
    output: Optional[str] = typer.Option(None, "--output", help="Output file or directory path"),
    save_original: bool = typer.Option(False, "--save-original", help="Save original markdown alongside summary")
):
    """
    Summarize a web article using AI.

    Examples:
        crawler summarize --url https://example.com/article
        crawler summarize --url https://example.com/article --summary brief --output summary.md
        crawler summarize --url https://example.com/article --model gemini/gemini-1.5-flash
    """
    try:
        # Load settings
        settings = Settings()

        # Validate configuration
        selected_model = model or settings.default_ai_model
        if not selected_model:
            raise ConfigurationError(
                "No AI model specified. Either provide --model parameter or set DEFAULT_AI_MODEL in .env file.",
                details={"missing_env": "DEFAULT_AI_MODEL"}
            )

        # Parse model configuration
        model_config = AIModelConfiguration.from_model_string(selected_model)

        # P1 restriction: Only Gemini models
        if model_config.provider != "gemini":
            raise ConfigurationError(
                f"Only Gemini models are supported in this version. "
                f"Support for {model_config.provider} coming soon in P2.",
                details={"provider": model_config.provider}
            )

        # Validate API key for cloud models
        if not model_config.is_local:
            if model_config.api_key_env_var == "GOOGLE_API_KEY" and not settings.google_api_key:
                raise ConfigurationError(
                    f"Missing API key: {model_config.api_key_env_var} not set in .env file.",
                    details={"missing_env": model_config.api_key_env_var}
                )

        typer.echo(f"Summarizing: {url}")
        typer.echo(f"Using model: {selected_model}")

        # Step 1: Crawl article
        firecrawl_service = FirecrawlService(settings.firecrawl_api_url, settings.firecrawl_api_key)
        article = firecrawl_service.scrape_to_article_content(url)

        typer.echo(f"Crawled article: {article.title} ({article.word_count} words)")

        # Check if article is too short
        if article.is_minimal:
            typer.echo(
                typer.style(
                    f"Warning: Article is very short ({article.word_count} words). Summary may not be meaningful.",
                    fg=typer.colors.YELLOW
                )
            )

        # Step 2: Summarize with AI
        ai_service = AIService()
        summary_result = ai_service.summarize(article, model_config, summary_length=summary)

        # Step 3: Output
        if output:
            output_service = OutputService()
            output_path = Path(output)

            if save_original:
                # Save both original and summary
                if output_path.is_dir() or str(output_path).endswith("/") or str(output_path).endswith("\\"):
                    # Directory: auto-generate filenames
                    base_name = article.title.replace(" ", "-").lower()[:50]
                    original_file = output_service.save(article.markdown, output_path / f"{base_name}.md")
                    summary_file = output_service.save(summary_result.summary_text, output_path / f"{base_name}-summary.md")
                    typer.echo(f"\nOriginal saved to: {original_file.file_path}")
                    typer.echo(f"Summary saved to: {summary_file.file_path}")
                else:
                    # File: derive names
                    original_file = output_service.save(article.markdown, output_path)
                    summary_path = output_path.parent / f"{output_path.stem}-summary{output_path.suffix}"
                    summary_file = output_service.save(summary_result.summary_text, summary_path)
                    typer.echo(f"\nOriginal saved to: {original_file.file_path}")
                    typer.echo(f"Summary saved to: {summary_file.file_path}")
            else:
                # Save only summary
                result_file = output_service.save(summary_result.summary_text, output_path)
                typer.echo(f"\nSummary saved to: {result_file.file_path}")
        else:
            # Print to console
            typer.echo("\n" + "="*60)
            typer.echo("SUMMARY")
            typer.echo("="*60)
            typer.echo(summary_result.summary_text)
            typer.echo("="*60)

        # Display metadata
        if summary_result.token_usage:
            typer.echo(
                f"\nTokens used: {summary_result.token_usage['total_tokens']} "
                f"(prompt: {summary_result.token_usage['prompt_tokens']}, "
                f"completion: {summary_result.token_usage['completion_tokens']})"
            )

        sys.exit(0)

    except ConfigurationError as e:
        typer.echo(typer.style(f"Configuration Error: {e.message}", fg=typer.colors.RED), err=True)
        if e.details:
            typer.echo(f"Details: {e.details}", err=True)
        sys.exit(e.code)

    except AIServiceError as e:
        typer.echo(typer.style(f"AI Service Error: {e.message}", fg=typer.colors.RED), err=True)
        if e.details:
            typer.echo(f"Details: {e.details}", err=True)
        sys.exit(e.code)

    except CrawlerError as e:
        typer.echo(typer.style(f"Error: {e.message}", fg=typer.colors.RED), err=True)
        if e.details:
            typer.echo(f"Details: {e.details}", err=True)
        sys.exit(e.code)

    except Exception as e:
        typer.echo(typer.style(f"Unexpected error: {str(e)}", fg=typer.colors.RED), err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
```

**Note**: You'll need to create `FirecrawlService.scrape_to_article_content()` method or adapt existing scrape method to return `ArticleContent`.

**Register in main CLI**:

```python
# src/cli/main.py (add import and command)
from src.cli import summarize

app.add_typer(summarize.app, name="summarize")
```

**Mark Complete**: Edit `tasks.md` and add `[X]` to T023 and T024.

---

### T025-T026: Integration Tests & Validation

**Run Integration Tests**:
```bash
uv run pytest tests/integration/test_summarize_cli.py -v
```

**Test the CLI Manually**:
```bash
# Set environment variables
export DEFAULT_AI_MODEL=gemini/gemini-pro
export GOOGLE_API_KEY=your_actual_api_key

# Test basic summarization
uv run python -m src.cli.summarize --url https://example.com/article

# Test with output file
uv run python -m src.cli.summarize --url https://example.com/article --output summary.md

# Test brief summary
uv run python -m src.cli.summarize --url https://example.com/article --summary brief
```

**Mark Complete**: Edit `tasks.md` and add `[X]` to T025 and T026.

---

### T027: Refactor & Code Quality

**Run Quality Checks**:
```bash
# Format code
uv run ruff format src/

# Check linting
uv run ruff check src/

# Type check
uv run mypy src/ --strict

# Run all tests
uv run pytest tests/ -v

# Check coverage
uv run pytest tests/ --cov=src --cov-report=html
```

**Fix any issues** found by the quality checks.

**Mark Complete**: Edit `tasks.md` and add `[X]` to T027.

---

## Full Feature Implementation (Remaining 21 Tasks)

### Phase 4: User Story 2 - Customizable Summary Length (P2)

**T028-T031**: Already mostly implemented in T020 (AI Service supports summary_length parameter). Just need to:
1. Write integration tests for different lengths
2. Verify token limits work correctly
3. Test word count ranges

### Phase 5: User Story 3 - Multi-Language Support (P2)

**T032-T034**: Already architected:
1. Prompts include language detection instructions
2. `ArticleContent` has `detected_language` field
3. `AISummary` has `output_language` field

Just need integration tests with multilingual articles.

### Phase 6: User Story 4 - Flexible AI Model Selection (P1)

**T035-T038**: Partially complete:
- T036 is done (model parameter override in CLI)
- T038 is done (P1 Gemini-only validation in CLI)
- T035, T037 need integration tests

### Phase 7: User Story 5 - Save Both Original and Summary (P3)

**T039-T041**: Already implemented in T024 CLI command with `--save-original` flag.

Just need tests.

### Final Phase: Polish & Integration

**T042-T047**:
- Edge case tests
- Success criteria validation
- Verbose mode (add `--verbose` flag)
- Documentation updates
- Final integration testing
- Code coverage verification

---

## Helper Scripts

### Create Missing Service Method

If `FirecrawlService.scrape_to_article_content()` doesn't exist, add:

```python
# In src/services/firecrawl.py

from src.models.article_content import ArticleContent

def scrape_to_article_content(self, url: str) -> ArticleContent:
    """
    Scrape URL and return ArticleContent model.

    Args:
        url: URL to scrape

    Returns:
        ArticleContent with markdown and metadata
    """
    result = self.scrape(url, format="markdown")

    # Calculate word count
    word_count = len(result.markdown.split())

    return ArticleContent(
        url=url,
        title=result.metadata.get("title", url.split("/")[-1]),
        markdown=result.markdown,
        word_count=word_count,
        detected_language=result.metadata.get("language"),
        metadata=result.metadata
    )
```

### Quick Test Script

Create `test_summarize.py` in project root:

```python
#!/usr/bin/env python
"""Quick test script for summarize command."""

import sys
from src.cli.summarize import summarize

if __name__ == "__main__":
    # Test with a simple article
    sys.argv = [
        "test",
        "--url", "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "--summary", "brief"
    ]
    summarize()
```

Run with: `uv run python test_summarize.py`

---

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all `__init__.py` files exist in packages
2. **LiteLLM not found**: Run `uv add litellm`
3. **API key errors**: Check `.env` file has `GOOGLE_API_KEY=...`
4. **Type errors**: Run `mypy --strict` and fix annotations
5. **Test failures**: Check mock objects are MagicMock, not dicts

### Testing Without Real API

Mock the AI service in integration tests:

```python
@patch('src.services.ai_service.litellm.completion')
def test_cli_basic_flow(mock_completion):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test summary"
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 50
    mock_response.usage.total_tokens = 150
    mock_completion.return_value = mock_response

    # Test CLI here
```

---

## Success Criteria Checklist

- [ ] T021-T027 complete (MVP)
- [ ] CLI command works end-to-end
- [ ] Tests pass: `pytest tests/ -v`
- [ ] Code quality: `ruff check src/` passes
- [ ] Type safety: `mypy src/ --strict` passes
- [ ] Coverage ≥ 80%: `pytest --cov=src`
- [ ] Manual testing with real API successful
- [ ] Documentation updated
- [ ] README.md updated with usage examples

---

**Estimated Time to Complete MVP**: 4-6 hours

Good luck! 🚀
