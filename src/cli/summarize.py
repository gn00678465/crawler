"""CLI command for AI-powered article summarization."""

import sys
import typer
from typing import Optional
from pathlib import Path

from src.models.ai_model_config import AIModelConfiguration
from src.services.firecrawl import FirecrawlService
from src.services.ai_service import AIService
from src.services.output import OutputService
from src.config.settings import Settings
from src.lib.exceptions import CrawlerError, ConfigurationError, AIServiceError

app = typer.Typer()


@app.command()
def summarize(
    url: str = typer.Option(..., "--url", help="Article URL to summarize"),
    model: Optional[str] = typer.Option(None, "--model", help="AI model (e.g., gemini/gemini-pro)"),
    summary: str = typer.Option(
        "standard", "--summary", help="Summary length: brief, standard, detailed"
    ),
    output: Optional[str] = typer.Option(None, "--output", help="Output file or directory path"),
    save_original: bool = typer.Option(
        False, "--save-original", help="Save original markdown alongside summary"
    ),
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
                details={"missing_env": "DEFAULT_AI_MODEL"},
            )

        # Parse model configuration
        model_config = AIModelConfiguration.from_model_string(selected_model)

        # P1 restriction: Only Gemini models
        if model_config.provider != "gemini":
            raise ConfigurationError(
                f"Only Gemini models are supported in this version. "
                f"Support for {model_config.provider} coming soon in P2.",
                details={"provider": model_config.provider},
            )

        # Validate API key for cloud models
        if not model_config.is_local:
            if model_config.api_key_env_var == "GOOGLE_API_KEY" and not settings.google_api_key:
                raise ConfigurationError(
                    f"Missing API key: {model_config.api_key_env_var} not set in .env file.",
                    details={"missing_env": model_config.api_key_env_var},
                )

        typer.echo(f"Summarizing: {url}")
        typer.echo(f"Using model: {selected_model}")

        # Step 1: Crawl article
        firecrawl_service = FirecrawlService(settings)
        article = firecrawl_service.scrape_to_article_content(url)

        typer.echo(f"Crawled article: {article.title} ({article.word_count} words)")

        # Check if article is too short
        if article.is_minimal:
            typer.echo(
                typer.style(
                    f"Warning: Article is very short ({article.word_count} words). Summary may not be meaningful.",
                    fg=typer.colors.YELLOW,
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
                if (
                    output_path.is_dir()
                    or str(output_path).endswith("/")
                    or str(output_path).endswith("\\")
                ):
                    # Directory: auto-generate filenames
                    base_name = article.title.replace(" ", "-").lower()[:50]
                    original_file = output_service.save(
                        article.markdown, output_path / f"{base_name}.md"
                    )
                    summary_file = output_service.save(
                        summary_result.summary_text, output_path / f"{base_name}-summary.md"
                    )
                    typer.echo(f"\nOriginal saved to: {original_file.file_path}")
                    typer.echo(f"Summary saved to: {summary_file.file_path}")
                else:
                    # File: derive names
                    original_file = output_service.save(article.markdown, output_path)
                    summary_path = (
                        output_path.parent / f"{output_path.stem}-summary{output_path.suffix}"
                    )
                    summary_file = output_service.save(summary_result.summary_text, summary_path)
                    typer.echo(f"\nOriginal saved to: {original_file.file_path}")
                    typer.echo(f"Summary saved to: {summary_file.file_path}")
            else:
                # Save only summary
                result_file = output_service.save(summary_result.summary_text, output_path)
                typer.echo(f"\nSummary saved to: {result_file.file_path}")
        else:
            # Print to console
            typer.echo("\n" + "=" * 60)
            typer.echo("SUMMARY")
            typer.echo("=" * 60)
            typer.echo(summary_result.summary_text)
            typer.echo("=" * 60)

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
