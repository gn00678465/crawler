# CLI Summarize Command Contract

**Feature**: `003-markdown-summary-ai`
**Command**: `crawler summarize`
**Module**: `src/cli/summarize.py`

## Command Signature

```bash
crawler summarize --url <URL> [OPTIONS]
```

## Required Arguments

- `--url <URL>`: Article URL to summarize (HTTP/HTTPS)

## Optional Arguments

- `--model <provider/model>`: AI model (default: `$DEFAULT_AI_MODEL` from `.env`)
- `--summary <brief|standard|detailed>`: Summary length (default: `standard`)
- `--output <path>`: Output file or directory (default: print to console)
- `--save-original`: Save both original markdown and summary (P3 feature)

## Exit Codes

- `0`: Success
- `1`: General error (invalid URL, network error, crawl failure)
- `2`: Configuration error (missing API key, invalid model, missing DEFAULT_AI_MODEL)
- `3`: AI service error (rate limit, API failure, token limit exceeded)

## Example Usage

```bash
# Basic: console output with default model
crawler summarize --url https://example.com/article

# Custom model and file output
crawler summarize --url https://example.com/article \
  --model gemini/gemini-1.5-flash \
  --output summary.md

# Brief summary to directory (auto-filename)
crawler summarize --url https://example.com/article \
  --summary brief \
  --output ./summaries/

# P3: Save both original and summary
crawler summarize --url https://example.com/article \
  --output ./docs/ \
  --save-original
```

## Test Strategy

**Integration Tests** (`tests/integration/test_summarize_cli.py`):
- Invoke CLI with typer.testing.CliRunner
- Test all parameter combinations
- Verify exit codes for error scenarios
- Check console output format
- Validate file creation when --output specified
