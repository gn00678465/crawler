# Implementation Plan: Web Crawler CLI Tool

**Branch**: `002-python3-uv-n` | **Date**: 2025-10-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-python3-uv-n/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

A Python 3 command-line tool for web scraping using Typer for CLI interface and Firecrawl v2 API for content extraction. The tool accepts a URL, scrapes content via self-hosted Firecrawl service, and outputs results in markdown or HTML format to a specified file or console. Environment variables (Firecrawl API URL and key) are managed using python-dotenv. Initial implementation focuses on the `scrape` command with `--url`, `--markdown` (format selection), and `--output` options.

## Technical Context

**Language/Version**: Python 3.10+ (per Constitution)
**Package Manager**: UV (per Constitution - NON-NEGOTIABLE)
**Primary Dependencies**:
- typer (CLI framework)
- python-dotenv (environment variable management)
- firecrawl-py (Firecrawl v2 API client) or httpx/requests (if direct API calls needed)
- pydantic (data validation and settings management)
**Storage**: File system (markdown and HTML output files)
**Testing**: pytest with pytest-cov (per Constitution); pytest-asyncio if async operations needed
**Target Platform**: Cross-platform CLI (Windows, Linux, macOS)
**Project Type**: Single project (CLI tool)
**Performance Goals**:
- Web page scraping completion < 10 seconds for pages < 1MB (per spec SC-001)
- Batch processing of 100+ URLs without manual intervention (per spec SC-006)
**Constraints**:
- Dependent on self-hosted Firecrawl API availability
- Firecrawl API rate limits (NEEDS CLARIFICATION - to be researched)
- Network connectivity required during operation
- User requires write permissions to output directory
**Scale/Scope**:
- Support for 50+ concurrent URL crawls in batch mode (per spec SC-007)
- Handle standard web pages with 95% success rate (per spec SC-002)
- Single-user CLI tool (not multi-tenant service)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Python 3 Development Standard**:
- [x] Python 3.10+ specified in Technical Context
- [x] Type hints planned for all public APIs (typer supports type hints natively; will use for all functions)
- [x] PEP 8 compliance tools configured (ruff planned for linting and formatting)

**II. UV Package Management**:
- [x] UV specified as package manager in Technical Context
- [x] `pyproject.toml` structure planned (will include project metadata, dependencies, and tool configurations)
- [x] No alternative package managers (pip, poetry, pipenv) in plan

**III. Test-Driven Development (NON-NEGOTIABLE)**:
- [x] Test-first workflow explicitly planned in tasks
- [x] Tests will be written BEFORE implementation
- [x] Red-Green-Refactor cycle documented in task ordering (tasks.md will enforce this via ordering)

**IV. Integration Testing**:
- [x] Integration test scope identified:
  - Firecrawl API integration (scrape endpoint)
  - File system I/O (output file creation)
  - Environment variable loading (.env configuration)
  - CLI argument parsing and validation
- [x] `tests/integration/` and `tests/contract/` directories planned
- [x] Integration points documented in contracts/ (will include Firecrawl API contract)

**V. Code Quality & Documentation**:
- [x] Docstring requirements specified (Google-style docstrings for all public functions and classes)
- [x] Type checking (mypy strict mode) planned
- [x] Linting tools (ruff for linting and formatting) configured
- [x] Code coverage ≥ 80% target set

**Gate Result**: ✅ PASS - All constitutional requirements satisfied. No violations to justify.

---

### Post-Design Re-Evaluation (Phase 1 Complete)

**Re-evaluation Date**: 2025-10-10

All design artifacts have been generated and reviewed against constitutional requirements:

**I. Python 3 Development Standard**:
- ✅ data-model.md specifies type hints for all Pydantic models
- ✅ CLI interface documented with proper type annotations
- ✅ PEP 8 compliance enforced via ruff configuration

**II. UV Package Management**:
- ✅ Dependencies identified: typer, firecrawl-py, python-dotenv, pydantic, pydantic-settings
- ✅ Test dependencies: pytest, pytest-cov, pytest-mock
- ✅ Quality tools: ruff, mypy, bandit
- ✅ All dependencies will be managed via UV in pyproject.toml

**III. Test-Driven Development**:
- ✅ Test structure designed: unit/, integration/, contract/ directories
- ✅ Test cases identified for all models and services
- ✅ CLI testing via typer.testing.CliRunner planned
- ✅ TDD workflow will be enforced in tasks.md ordering

**IV. Integration Testing**:
- ✅ Firecrawl API contract documented (contracts/firecrawl-v2-scrape-api.yaml)
- ✅ CLI interface contract documented (contracts/cli-interface.md)
- ✅ Integration points clearly defined in data-model.md
- ✅ Contract test cases specified

**V. Code Quality & Documentation**:
- ✅ Google-style docstrings specified for all models
- ✅ mypy strict mode planned in research.md
- ✅ ruff configuration planned for linting/formatting
- ✅ 80% coverage target established
- ✅ Comprehensive documentation: spec.md, plan.md, research.md, data-model.md, quickstart.md

**Design Artifacts Generated**:
- ✅ research.md: All NEEDS CLARIFICATION items resolved
- ✅ data-model.md: Complete entity definitions with validation rules
- ✅ contracts/firecrawl-v2-scrape-api.yaml: OpenAPI specification for Firecrawl integration
- ✅ contracts/cli-interface.md: CLI contract with examples and test cases
- ✅ quickstart.md: User-facing setup and usage guide
- ✅ CLAUDE.md: Agent context file updated with technology stack

**Final Gate Result**: ✅✅ PASS - All constitutional requirements satisfied post-design. Ready for task generation (/speckit.tasks).

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/
├── models/          # Data models (Pydantic schemas for requests/responses)
│   ├── __init__.py
│   └── scrape.py    # ScrapeRequest, ScrapeResponse, OutputFormat
├── services/        # Business logic and external integrations
│   ├── __init__.py
│   ├── firecrawl.py # Firecrawl API client wrapper
│   └── output.py    # File output handling (markdown/HTML)
├── cli/             # CLI commands and interface
│   ├── __init__.py
│   └── scrape.py    # Typer CLI command for scrape
├── config/          # Configuration management
│   ├── __init__.py
│   └── settings.py  # Environment variable loading (dotenv)
└── lib/             # Shared utilities
    ├── __init__.py
    └── validators.py # URL validation, path validation

tests/
├── contract/        # Contract tests for external services
│   ├── __init__.py
│   └── test_firecrawl_api.py # Firecrawl API v2 contract tests
├── integration/     # Integration tests
│   ├── __init__.py
│   ├── test_scrape_command.py # End-to-end CLI command tests
│   └── test_file_output.py    # File I/O integration tests
└── unit/            # Unit tests
    ├── __init__.py
    ├── test_models.py         # Model validation tests
    ├── test_firecrawl.py      # Firecrawl service unit tests
    ├── test_output.py         # Output service unit tests
    └── test_validators.py     # Validator unit tests

pyproject.toml       # Project metadata, dependencies, tool configs
uv.lock              # UV lock file for reproducible builds
.env.example         # Example environment variables
.gitignore           # Git ignore patterns
README.md            # Project documentation
```

**Structure Decision**: Single project structure (Option 1) is appropriate because this is a standalone CLI tool without separate frontend/backend or mobile components. The structure organizes code by responsibility (models, services, cli, config, lib) which aligns with the constitution's requirement for structured directories (per user input: "service 相關的放在 services 內, cli 相關的放在 cli 內").

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

N/A - No constitutional violations. All gates passed.
