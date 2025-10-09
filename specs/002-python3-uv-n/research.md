# Research Report: Web Crawler CLI Tool

**Branch**: `002-python3-uv-n` | **Date**: 2025-10-10 | **Phase**: 0 (Outline & Research)

## Overview

This document consolidates research findings to resolve all NEEDS CLARIFICATION items from the Technical Context and establish best practices for implementation.

---

## 1. Firecrawl v2 API Integration

### Decision: Use Official firecrawl-py Python SDK

**Rationale**:
- Official Python SDK (`firecrawl-py`) provides a clean, maintained interface to Firecrawl v2 API
- Abstracts away HTTP details (headers, authentication, error handling)
- Includes both synchronous and asynchronous support via `AsyncFirecrawl` class
- Active maintenance and documentation at https://docs.firecrawl.dev/sdks/python

**Alternatives Considered**:
- **Direct HTTP calls with httpx/requests**: Would require manual handling of authentication, retries, and error parsing. Rejected because SDK provides these features out-of-box.
- **Custom API wrapper**: Unnecessary duplication of effort when official SDK exists and is well-maintained.

**Implementation Details**:
- **Installation**: `uv pip install firecrawl-py`
- **API Configuration for Self-Hosted**:
  - Environment variable: `FIRECRAWL_API_URL` (e.g., `http://localhost:3002`)
  - Environment variable: `FIRECRAWL_API_KEY` (optional for self-hosted, default auth disabled)
  - SDK initialization: `Firecrawl(api_key=api_key, api_url=api_url)`
- **Available Methods**:
  - `scrape(url, formats=['markdown', 'html'])` - Primary method for single URL scraping
  - Returns response with `markdown`, `html`, `links`, `metadata` fields

**Sources**:
- https://docs.firecrawl.dev/sdks/python
- https://github.com/mendableai/firecrawl-py
- https://pypi.org/project/firecrawl-py/

---

## 2. Firecrawl API Rate Limits

### Decision: Rate limits are configurable in self-hosted instances

**Rationale**:
- Self-hosted Firecrawl instances use Redis for rate limiting
- `REDIS_RATE_LIMIT_URL` environment variable controls rate limiting backend
- Default configuration in self-hosted setup: `USE_DB_AUTHENTICATION=false` means no API key enforcement
- Rate limit behavior can be customized via Redis configuration

**Handling Strategy**:
- **Error Detection**: SDK will raise exception or return 429 status code when rate limit exceeded
- **User Feedback**: Display clear error message indicating rate limit and suggest retry timing
- **No Automatic Retry**: For initial implementation (P1), let user handle retries manually. Batch processing (P3) will need backoff strategy.

**Self-Hosted Configuration Variables**:
- `REDIS_RATE_LIMIT_URL`: Redis instance for rate limiting
- `NUM_WORKERS_PER_QUEUE`: Controls processing capacity (default: 8)
- `PORT`: API port (default: 3002)
- `HOST`: Bind address (default: 0.0.0.0)

**Sources**:
- https://docs.firecrawl.dev/contributing/self-host
- https://www.genspark.ai/spark/setting-firecrawl-environment-variables/

---

## 3. Async vs Sync Implementation

### Decision: Start with synchronous implementation, add async for batch operations (P3)

**Rationale**:
- **Performance Goal**: < 10 seconds for pages < 1MB (per spec SC-001) is achievable with sync calls
- **Simplicity First**: P1 feature (single URL scraping) doesn't require concurrency
- **Future Scaling**: P3 batch processing (50+ concurrent crawls per SC-007) will benefit from `AsyncFirecrawl`
- **SDK Support**: Both `Firecrawl` (sync) and `AsyncFirecrawl` (async) classes available

**Implementation Plan**:
- **Phase 1 (P1)**: Use synchronous `Firecrawl.scrape()` for single URL operations
- **Phase 2 (P3)**: Refactor to `AsyncFirecrawl` when implementing batch crawling with `asyncio.gather()`
- **Testing**: Use `pytest` for sync tests; add `pytest-asyncio` when async features developed

**Alternatives Considered**:
- **Async from start**: Over-engineering for P1 single-URL use case. Adds complexity without current benefit.
- **Threading instead of async**: Python's asyncio is more efficient for I/O-bound operations like HTTP requests.

**Sources**:
- https://docs.firecrawl.dev/sdks/python (AsyncFirecrawl documentation)
- Constitutional requirement: pytest-asyncio for async test support

---

## 4. Typer CLI Best Practices

### Decision: Use Typer with type hints, structured commands, and Pydantic for config

**Rationale**:
- **Type Safety**: Typer leverages Python type hints for automatic validation and help generation
- **User Experience**: Automatic `--help` generation, clear error messages, shell completion support
- **Maintainability**: Clean separation of CLI interface (Typer) from business logic (services)
- **Integration**: Works seamlessly with Pydantic for configuration management

**Best Practices to Implement**:

1. **Command Structure**:
   ```python
   import typer
   app = typer.Typer()

   @app.command()
   def scrape(
       url: str = typer.Option(..., help="URL to scrape"),
       markdown: bool = typer.Option(True, help="Output as markdown"),
       output: Optional[str] = typer.Option(None, help="Output file path")
   ):
       """Scrape a single web page using Firecrawl."""
       pass
   ```

2. **Exit Codes**:
   - 0 = Success
   - 1 = General error (invalid URL, network failure)
   - 2 = Configuration error (missing API key)
   - 3 = Rate limit exceeded

3. **Error Handling**:
   - Use `typer.echo()` for output (supports color via `typer.style()`)
   - Use `typer.Exit(code)` for graceful exits
   - Provide actionable error messages

4. **Configuration with Pydantic**:
   ```python
   from pydantic_settings import BaseSettings

   class Settings(BaseSettings):
       firecrawl_api_url: str
       firecrawl_api_key: str = ""

       class Config:
           env_file = ".env"
   ```

5. **Testing**:
   - Typer provides `typer.testing.CliRunner` for CLI testing
   - Test both success and error paths
   - Mock external dependencies (Firecrawl API)

**Project Structure Alignment**:
- `src/cli/scrape.py`: Typer command definitions
- `src/config/settings.py`: Pydantic settings with dotenv
- `src/services/firecrawl.py`: Business logic (separated from CLI)

**Sources**:
- https://typer.tiangolo.com/ (Official documentation)
- https://www.projectrules.ai/rules/typer (Best practices)
- https://realpython.com/python-typer-cli/ (Tutorial)

---

## 5. Output Format Handling

### Decision: Firecrawl v2 natively supports markdown and HTML; no conversion needed

**Rationale**:
- **Native Formats**: Firecrawl v2 API returns both `markdown` and `html` fields in response
- **Format Parameter**: SDK accepts `formats=['markdown', 'html']` parameter in `scrape()` method
- **No Processing Required**: Content is returned ready-to-use, reducing complexity

**Implementation Details**:

1. **Format Selection**:
   - `--markdown` flag (default): Use `response.markdown` field
   - `--html` flag: Use `response.html` field
   - Request both formats from API: `formats=['markdown', 'html']` to support future use cases

2. **File Extensions**:
   - Markdown: `.md`
   - HTML: `.html`
   - Auto-detect from format choice when generating default filenames

3. **Additional Formats (Future)**:
   - Firecrawl v2 also supports: `json` (with schema), `links`, `screenshot`, `summary`
   - Can be added in future P2 work (per spec User Story 2)

4. **Output Handling**:
   - If `--output` specified: Write to file with appropriate extension
   - If `--output` omitted: Print to stdout (console) using `typer.echo()`

**Content Preservation**:
- Firecrawl handles preservation of headings, paragraphs, links, images (per FR-012)
- Use `onlyMainContent=true` parameter to extract main content and reduce noise

**Sources**:
- https://docs.firecrawl.dev/api-reference/endpoint/scrape (Response format)
- https://www.firecrawl.dev/blog/mastering-firecrawl-scrape-endpoint (Tutorial)

---

## 6. Environment Variable Management

### Decision: Use python-dotenv with Pydantic Settings for type-safe configuration

**Rationale**:
- **Constitution Requirement**: Project specifies python-dotenv for environment management
- **Type Safety**: Pydantic BaseSettings provides automatic validation and type conversion
- **Developer Experience**: `.env` file for local development, environment variables for production
- **Error Detection**: Missing required variables raise clear validation errors at startup

**Implementation**:

```python
# src/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    firecrawl_api_url: str  # Required
    firecrawl_api_key: Optional[str] = ""  # Optional for self-hosted

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

# Usage
settings = Settings()
```

**Required Environment Variables**:
- `FIRECRAWL_API_URL`: Self-hosted Firecrawl instance URL (e.g., `http://localhost:3002`)
- `FIRECRAWL_API_KEY`: API key (optional if self-hosted instance has `USE_DB_AUTHENTICATION=false`)

**Setup**:
1. Create `.env.example` with template variables
2. User copies to `.env` and fills in values
3. `.env` added to `.gitignore` (security)

**Dependencies**:
- `python-dotenv`: For `.env` file loading
- `pydantic`: For settings validation
- `pydantic-settings`: For BaseSettings class

**Sources**:
- User requirement: "環境變數使用 python-dotenv 管理"
- https://docs.pydantic.dev/latest/concepts/pydantic_settings/

---

## 7. Testing Strategy

### Decision: Pytest with unit, integration, and contract tests following TDD

**Rationale**:
- **Constitution Mandate**: TDD is non-negotiable; tests written before implementation
- **Test Categories**:
  - **Unit Tests**: Individual components (validators, models, output service)
  - **Integration Tests**: CLI commands, file I/O
  - **Contract Tests**: Firecrawl API responses match expectations
- **Coverage Target**: ≥ 80% per constitutional requirement

**Test Organization**:

```
tests/
├── unit/
│   ├── test_models.py         # Pydantic model validation
│   ├── test_validators.py     # URL validation logic
│   ├── test_output.py          # File writing logic
│   └── test_firecrawl.py       # Service logic (mocked API)
├── integration/
│   ├── test_scrape_command.py  # End-to-end CLI execution
│   └── test_file_output.py     # Actual file system operations
└── contract/
    └── test_firecrawl_api.py   # Real API responses (optional)
```

**Testing Tools**:
- `pytest`: Test framework (constitutional requirement)
- `pytest-cov`: Coverage reporting
- `typer.testing.CliRunner`: CLI command testing
- `pytest-mock` or `unittest.mock`: Mocking external dependencies
- `responses` or `httpx-mock`: HTTP mocking for Firecrawl API

**TDD Workflow** (per constitution):
1. Write test for feature (RED phase)
2. Verify test fails
3. Implement minimal code to pass (GREEN phase)
4. Refactor while keeping tests green
5. Commit after complete red-green-refactor cycle

**Sources**:
- Constitutional Principle III: Test-Driven Development (NON-NEGOTIABLE)
- https://docs.pytest.org/

---

## 8. Code Quality Tools

### Decision: Ruff for linting/formatting, mypy for type checking

**Rationale**:
- **Ruff**: Fast, modern linter that replaces flake8 + black + isort
- **Mypy**: Industry-standard static type checker with strict mode support
- **Constitution Compliance**: Meets code quality requirements (Principle V)

**Tool Configuration**:

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

**Pre-commit Integration**:
- Format code with ruff on every commit
- Run mypy type checking
- Run bandit security scan

**CI/CD Checks**:
- All tests pass
- Type checking passes (mypy --strict)
- Linting passes (ruff check)
- Coverage ≥ 80%

**Sources**:
- Constitutional Principle V: Code Quality & Documentation
- https://docs.astral.sh/ruff/

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Firecrawl Integration** | Use firecrawl-py SDK (sync initially) | Official support, clean API, async available for P3 |
| **Rate Limiting** | Handle 429 errors with clear messages | Self-hosted config controls limits; manual retry for P1 |
| **Async/Sync** | Sync for P1, async for P3 batch | Performance goal met with sync; async adds unnecessary complexity initially |
| **CLI Framework** | Typer with type hints | Modern, clean API, auto-generated help, Pydantic integration |
| **Output Formats** | Use native Firecrawl markdown/HTML | No conversion needed, reduces complexity |
| **Configuration** | python-dotenv + Pydantic Settings | Type-safe, validated, meets constitutional requirements |
| **Testing** | Pytest with TDD (unit/integration/contract) | Constitutional mandate, 80% coverage target |
| **Code Quality** | Ruff (lint/format) + mypy (strict typing) | Fast, modern tools meeting constitutional standards |

---

## Next Steps (Phase 1: Design & Contracts)

1. Generate `data-model.md` with Pydantic schemas (ScrapeRequest, ScrapeResponse, Settings)
2. Create API contract in `contracts/firecrawl-v2-scrape.yaml` (OpenAPI format)
3. Generate `quickstart.md` with setup instructions
4. Update agent context with technologies: typer, firecrawl-py, pydantic-settings, ruff, mypy

---

**Research Completed**: 2025-10-10
**Status**: All NEEDS CLARIFICATION items resolved ✅
