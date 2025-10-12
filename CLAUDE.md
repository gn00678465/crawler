# Claude Code Context File

This file provides context for Claude Code to understand the project's technology stack, architecture, and conventions.

## Project Overview

**Name**: Web Crawler CLI Tool
**Type**: Command-line application for web scraping
**Current Feature**: 002-python3-uv-n (Initial scrape command implementation)

## Technology Stack

<!-- BEGIN SPECKIT MANAGED: Do not manually edit between markers -->
### Language & Runtime
- **Python**: 3.10+ (per Constitution - NON-NEGOTIABLE)
- **Package Manager**: UV (per Constitution - NON-NEGOTIABLE)

### Primary Dependencies
- **typer**: CLI framework for command-line interface
- **firecrawl-py**: Official Firecrawl v2 API client for web scraping
- **python-dotenv**: Environment variable management from .env files
- **pydantic**: Data validation and settings management
- **pydantic-settings**: Settings management with environment variable support

### Testing Framework
- **pytest**: Unit and integration testing (per Constitution)
- **pytest-cov**: Code coverage reporting (≥80% required)
- **pytest-mock**: Mocking for unit tests
- **typer.testing.CliRunner**: CLI command testing

### Code Quality Tools
- **ruff**: Fast linting and formatting (replaces flake8 + black)
- **mypy**: Static type checking in strict mode
- **bandit**: Security vulnerability scanning

### Storage
- **File System**: Markdown (.md) and HTML (.html) output files

### External Services
- **Firecrawl API**: Self-hosted instance for web content extraction
  - Default URL: http://localhost:3002
  - Configuration via `FIRECRAWL_API_URL` environment variable

### Project Type
- Single project structure (CLI tool)
- No frontend/backend separation
<!-- END SPECKIT MANAGED -->

## Project Structure

```
src/
├── models/          # Pydantic data models
├── services/        # Business logic (Firecrawl API, file output)
├── cli/             # Typer CLI commands
├── config/          # Settings and configuration
└── lib/             # Shared utilities (validators, exceptions)

tests/
├── unit/            # Unit tests (mocked dependencies)
├── integration/     # Integration tests (CLI, file I/O)
└── contract/        # Contract tests (Firecrawl API)
```

## Development Conventions

### Test-Driven Development (NON-NEGOTIABLE)
1. Write tests FIRST (before implementation)
2. Ensure tests FAIL initially (red phase)
3. Implement minimal code to pass (green phase)
4. Refactor while keeping tests green
5. Commit after complete red-green-refactor cycle

### Code Quality Standards
- **Type Hints**: Required for all function signatures and class attributes
- **Docstrings**: Google-style docstrings for all public functions/classes
- **PEP 8**: Follow Python style guidelines
- **Code Coverage**: Minimum 80% for all new code
- **Linting**: All code must pass `ruff check`
- **Type Checking**: All code must pass `mypy --strict`

### Package Management
- Use `uv pip install` for installing packages
- All dependencies declared in `pyproject.toml`
- `uv.lock` committed to version control
- NO other package managers (pip, poetry, pipenv) allowed

## Environment Configuration

Required environment variables (`.env` file):
```ini
FIRECRAWL_API_URL=http://localhost:3002  # Required
FIRECRAWL_API_KEY=                       # Optional for self-hosted
```

## Key Architectural Decisions

### Synchronous vs Asynchronous
- **Phase 1 (P1)**: Synchronous implementation using `Firecrawl.scrape()`
- **Phase 2 (P3)**: Async for batch operations using `AsyncFirecrawl`

### Output Formats
- Markdown (default): Native from Firecrawl API
- HTML: Native from Firecrawl API
- No format conversion needed (Firecrawl handles it)

### Error Handling
- Custom exception hierarchy (CrawlerError base class)
- Exit codes: 0 (success), 1 (general error), 2 (config error), 3 (rate limit)
- Error messages to stderr, content to stdout

### CLI Interface
- Primary command: `crawler scrape`
- Arguments: `--url` (required), `--markdown`/`--html` (format), `--output` (file path)
- Help generated automatically by Typer

## Documentation

- **Feature Spec**: `specs/002-python3-uv-n/spec.md`
- **Implementation Plan**: `specs/002-python3-uv-n/plan.md`
- **Research Findings**: `specs/002-python3-uv-n/research.md`
- **Data Models**: `specs/002-python3-uv-n/data-model.md`
- **API Contracts**: `specs/002-python3-uv-n/contracts/`
- **Quickstart**: `specs/002-python3-uv-n/quickstart.md`

## Constitution

See `.specify/memory/constitution.md` for project principles:
- I. Python 3 Development Standard
- II. UV Package Management (NON-NEGOTIABLE)
- III. Test-Driven Development (NON-NEGOTIABLE)
- IV. Integration Testing
- V. Code Quality & Documentation

All development must comply with constitutional requirements.

---

**Last Updated**: 2025-10-12 (Feature 002-python3-uv-n)
**Next**: Implementation via `/speckit.tasks` and `/speckit.implement`
