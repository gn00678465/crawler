# Implementation Plan: AI-Powered Article Summarization Command

**Branch**: `003-markdown-summary-ai` | **Date**: 2025-10-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-markdown-summary-ai/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature adds a new `crawler summarize` command that crawls web articles and generates AI-powered summaries using LiteLLM for multi-provider AI model integration. The implementation follows the flow: Firecrawl → Markdown → AI Summarization → Output (console or file). Initial phase (P1) focuses on Google Gemini models, with extensibility for other providers (OpenAI, Anthropic, Ollama) in P2. Users can customize system prompts to control summarization behavior.

## Technical Context

**Language/Version**: Python 3.10+  (per Constitution)
**Package Manager**: UV (per Constitution - NON-NEGOTIABLE)
**Primary Dependencies**:
- `litellm` (AI model integration SDK - unified interface for multiple providers)
- `firecrawl-py` (existing - web scraping)
- `typer` (existing - CLI framework)
- `pydantic` (existing - data validation)
- `python-dotenv` (existing - environment configuration)

**Storage**: File system (markdown and summary files)
**Testing**: pytest with pytest-cov (per Constitution)
**Target Platform**: Cross-platform CLI (Windows, Linux, macOS)
**Project Type**: Single project (CLI tool extending existing crawler)
**Performance Goals**:
- Summarize 1000-3000 word articles in <15 seconds (cloud models)
- Support articles up to 50,000 words within AI token limits
- 95% success rate on public articles

**Constraints**:
- P1: Google Gemini models only (extensible architecture for P2)
- AI service rate limits (provider-dependent)
- Network latency for cloud AI services
- API costs (user responsible)

**Scale/Scope**:
- Single CLI command (`crawler summarize`)
- 3 summary length modes (brief, standard, detailed)
- Multi-language support (auto-detect, summarize in source language)
- Customizable system prompts via configuration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Python 3 Development Standard**:
- [x] Python 3.10+ specified in Technical Context
- [x] Type hints planned for all public APIs (Pydantic models, service interfaces, CLI commands)
- [x] PEP 8 compliance tools configured (ruff for linting and formatting)

**II. UV Package Management**:
- [x] UV specified as package manager in Technical Context
- [x] `pyproject.toml` structure planned (add `litellm` dependency)
- [x] No alternative package managers (pip, poetry, pipenv) in plan

**III. Test-Driven Development (NON-NEGOTIABLE)**:
- [x] Test-first workflow explicitly planned in tasks
- [x] Tests will be written BEFORE implementation
- [x] Red-Green-Refactor cycle documented in task ordering

**IV. Integration Testing**:
- [x] Integration test scope identified:
  - LiteLLM API interactions (contract tests with mock responses)
  - Firecrawl integration (reuse existing patterns from scrape command)
  - CLI command end-to-end (invoke summarize, verify output)
  - File output generation (directory vs file path handling)
- [x] `tests/integration/` and `tests/contract/` directories planned
- [x] Integration points documented in contracts/

**V. Code Quality & Documentation**:
- [x] Docstring requirements specified (Google-style for all public functions/classes)
- [x] Type checking (mypy strict mode) planned
- [x] Linting tools (ruff) configured
- [x] Code coverage ≥ 80% target set

## Project Structure

### Documentation (this feature)

```
specs/003-markdown-summary-ai/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── litellm-api.md   # LiteLLM completion() API contract
│   └── cli-summarize.md # CLI command interface contract
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/
├── models/              # Pydantic data models
│   ├── summarize_request.py    # NEW: SummarizeRequest model
│   ├── ai_summary.py            # NEW: AISummary model
│   └── ai_model_config.py       # NEW: AIModelConfiguration model
├── services/
│   ├── firecrawl_service.py    # EXISTING: Reuse for article crawling
│   ├── file_output_service.py  # EXISTING: Reuse for saving summaries
│   ├── ai_service.py            # NEW: AI summarization service (LiteLLM wrapper)
│   └── prompt_service.py        # NEW: System prompt management
├── cli/
│   ├── scrape.py                # EXISTING: scrape command
│   └── summarize.py             # NEW: summarize command
├── config/
│   ├── settings.py              # EXISTING: Extend with AI model settings
│   └── prompts.py               # NEW: Default system prompts for summarization
└── lib/
    ├── validators.py            # EXISTING: Reuse URL validation
    └── exceptions.py            # EXISTING: Extend with AI-specific exceptions

tests/
├── contract/
│   ├── test_litellm_contract.py # NEW: LiteLLM API contract tests
│   └── test_firecrawl_contract.py # EXISTING: Firecrawl API contract tests
├── integration/
│   ├── test_summarize_cli.py    # NEW: End-to-end CLI tests
│   ├── test_ai_service.py       # NEW: AI service integration tests
│   └── test_scrape_cli.py       # EXISTING: Scrape CLI tests
└── unit/
    ├── models/
    │   ├── test_summarize_request.py # NEW: Unit tests for models
    │   ├── test_ai_summary.py
    │   └── test_ai_model_config.py
    ├── services/
    │   ├── test_ai_service.py        # NEW: Unit tests for services
    │   └── test_prompt_service.py
    └── cli/
        └── test_summarize.py         # NEW: Unit tests for CLI command
```

**Structure Decision**: Single project structure (Option 1) is appropriate as this is a CLI tool. The feature extends the existing crawler with a new command, reusing established patterns for file I/O, URL validation, and Firecrawl integration. New components (AI service, prompt management) are added following the existing layered architecture (models → services → CLI).

## Complexity Tracking

*No violations - Constitution Check passed completely*

## Phase 0: Research & Technical Discovery

**Status**: Completed inline (no separate research.md needed - all decisions documented below)

### Decision 1: LiteLLM Integration Strategy

**Decision**: Use LiteLLM's `completion()` API with standard message format (system + user roles)

**Rationale**:
- LiteLLM provides unified interface across 100+ AI providers
- Standard OpenAI-compatible message format: `[{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]`
- Automatic provider routing based on model name (e.g., `gemini/gemini-pro` → Google AI, `openai/gpt-4` → OpenAI)
- Built-in error handling, retry logic, and fallback mechanisms
- Environment variable convention: `GOOGLE_API_KEY`, `OPENAI_API_KEY`, etc.

**Alternatives Considered**:
- **Direct Google Gemini SDK**: Rejected - locks us to single provider, no extensibility
- **LangChain**: Rejected - heavyweight framework with unnecessary abstractions for our use case
- **Custom API clients**: Rejected - reinventing the wheel, maintenance burden

**Implementation Details**:
```python
import litellm

response = litellm.completion(
    model="gemini/gemini-pro",  # P1: Gemini only, P2: expand to openai/gpt-4, etc.
    messages=[
        {"role": "system", "content": "You are a concise summarizer..."},
        {"role": "user", "content": "Article markdown content here"}
    ]
)
summary = response.choices[0].message.content
```

### Decision 2: System Prompt Management

**Decision**: Store default prompts in `src/config/prompts.py`, allow user override via config file or environment variable

**Rationale**:
- Different summary lengths (brief, standard, detailed) require different system prompts
- Users may want domain-specific summarization (technical vs general audience)
- Prompts are configuration, not code - should be easily modifiable without touching source
- Versioning: Track prompt changes separately from code logic

**Prompt Structure** (detailed in `contracts/litellm-api.md`):
- **Brief**: "Summarize in 1-2 sentences, extracting only the core message"
- **Standard**: "Summarize in 3-5 key points, balancing breadth and depth"
- **Detailed**: "Provide comprehensive summary with main sections, arguments, and supporting details"
- **Multi-language**: Include instruction to detect and respond in source language

**Override Mechanism** (P3):
```
.env:
SUMMARIZE_PROMPT_BRIEF="Custom brief prompt..."
SUMMARIZE_PROMPT_STANDARD="Custom standard prompt..."
```

### Decision 3: Error Handling & Startup Validation

**Decision**: Validate AI model configuration at application startup, fail fast with actionable errors

**Rationale**:
- Constitution requirement: startup validation for default model and API keys
- Better UX: Catch config errors before user runs command
- LiteLLM validation: Use `litellm.validate_environment()` (if available) or custom checks

**Validation Checklist**:
1. Check `DEFAULT_AI_MODEL` environment variable exists
2. Parse model string format (`provider/model-name`)
3. Check corresponding API key exists (e.g., `GOOGLE_API_KEY` for `gemini/*`)
4. For P1: If provider is not `gemini`, display error (future support planned)
5. Display clear error with missing variable name and setup instructions

**Error Message Template**:
```
Error: Missing API key for model 'gemini/gemini-pro'
Required environment variable: GOOGLE_API_KEY
Set it in .env file or export it in your shell.
```

### Decision 4: Phased Rollout Strategy

**Decision**: P1 implements Gemini only with architecture ready for P2 multi-provider expansion

**Rationale**:
- User explicitly requested Gemini-first approach
- Reduces initial scope while proving LiteLLM integration pattern
- Architecture (LiteLLM abstraction) inherently supports multi-provider
- P2 expansion is configuration change, not code rewrite

**P1 Scope** (MVP):
- Google Gemini models (`gemini/gemini-pro`, `gemini/gemini-1.5-flash`)
- Validation rejects non-Gemini models with "Coming soon" message
- Full feature set: multi-language, summary lengths, custom prompts

**P2 Scope** (Future):
- Remove Gemini-only validation check
- Add provider-specific API key mapping logic
- Test with OpenAI, Anthropic, Ollama models
- Document provider-specific model names in README

## Phase 1: Data Models & Contracts

### Data Models (`data-model.md`)

See `data-model.md` for complete model specifications with field types, validation rules, and relationships.

**Summary of Key Models**:
1. **SummarizeRequest**: Command parameters (URL, model, summary length, output path, save original flag)
2. **AIModelConfiguration**: Parsed model config (provider, model name, API key name, local vs cloud)
3. **ArticleContent**: Crawled markdown content with metadata (title, URL, language, word count)
4. **AISummary**: Generated summary with metadata (text, language, model used, token usage, timestamp)
5. **OutputFile**: File write result (path, size, format)

### API Contracts (`contracts/`)

#### 1. LiteLLM Completion API (`contracts/litellm-api.md`)

**Purpose**: Document expected behavior of `litellm.completion()` for contract testing

**Request Format**:
```python
{
    "model": "gemini/gemini-pro",  # Format: provider/model-name
    "messages": [
        {"role": "system", "content": "<system prompt>"},
        {"role": "user", "content": "<article markdown>"}
    ],
    "temperature": 0.3,  # Lower temperature for factual summarization
    "max_tokens": <based on summary length>
}
```

**Response Format**:
```python
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "<generated summary>"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 1500,
        "completion_tokens": 200,
        "total_tokens": 1700
    }
}
```

**Error Scenarios**:
- Invalid API key → `AuthenticationError`
- Model not found → `litellm.exceptions.BadRequestError`
- Rate limit exceeded → `litellm.exceptions.RateLimitError`
- Token limit exceeded → `litellm.exceptions.ContextWindowExceededError`

#### 2. CLI Command Interface (`contracts/cli-summarize.md`)

**Command**: `crawler summarize`

**Required Arguments**:
- `--url <URL>`: Article URL to summarize

**Optional Arguments**:
- `--model <provider/model>`: AI model (default: `$DEFAULT_AI_MODEL`)
- `--summary <brief|standard|detailed>`: Summary length (default: `standard`)
- `--output <path>`: Output file or directory (default: print to console)
- `--save-original`: Save both original markdown and summary (P3)

**Exit Codes**:
- 0: Success
- 1: General error (invalid URL, network error)
- 2: Configuration error (missing API key, invalid model)
- 3: AI service error (rate limit, API failure)

**Example Usage**:
```bash
# Basic usage (console output, default model)
crawler summarize --url https://example.com/article

# Custom model and output file
crawler summarize --url https://example.com/article \
  --model gemini/gemini-1.5-flash \
  --output summary.md

# Brief summary to directory (auto-generate filename)
crawler summarize --url https://example.com/article \
  --summary brief \
  --output ./summaries/

# Save both original and summary (P3)
crawler summarize --url https://example.com/article \
  --output ./docs/ \
  --save-original
```

### Quickstart Guide (`quickstart.md`)

See `quickstart.md` for complete setup and usage instructions.

**Quick Setup**:
1. Install dependencies: `uv pip install litellm`
2. Configure `.env`: `DEFAULT_AI_MODEL=gemini/gemini-pro`, `GOOGLE_API_KEY=your_key_here`
3. Run: `crawler summarize --url https://example.com/article`

## Implementation Notes

### Reusable Components from Existing Crawler

- **URL Validation**: `lib/validators.py` - Reuse `validate_url()`
- **Firecrawl Integration**: `services/firecrawl_service.py` - Reuse `scrape()` method
- **File Output**: `services/file_output_service.py` - Reuse `save_to_file()` and `save_to_directory()` logic
- **Error Handling**: `lib/exceptions.py` - Extend with `AIServiceError`, `ConfigurationError`
- **Settings Management**: `config/settings.py` - Extend with `AISettings` section

### New Components

- **AI Service** (`services/ai_service.py`):
  - Wrapper around LiteLLM `completion()` API
  - Prompt template management (load from `config/prompts.py`)
  - Token usage tracking and logging
  - Error translation (LiteLLM exceptions → our custom exceptions)

- **Prompt Service** (`services/prompt_service.py`):
  - Load system prompts based on summary length
  - Support user-defined prompt overrides (P3)
  - Multi-language instruction injection

- **CLI Command** (`cli/summarize.py`):
  - Typer command definition with all parameters
  - Startup validation (check API keys, model format)
  - Orchestrate: crawl → summarize → output
  - Handle all error scenarios with user-friendly messages

### Testing Strategy

**Unit Tests** (`tests/unit/`):
- Models: Pydantic validation rules
- Services: Mocked LiteLLM responses, test error handling
- CLI: Typer command parsing, parameter validation

**Integration Tests** (`tests/integration/`):
- End-to-end CLI invocation (real network, mocked AI)
- File output generation (both file and directory paths)
- Error handling flows (missing API key, invalid URL)

**Contract Tests** (`tests/contract/`):
- LiteLLM API response structure (mock real API responses)
- Verify our code handles all documented error types
- Test multi-language prompt behavior (send Chinese article, expect Chinese summary)

## Next Steps

1. Run `/speckit.tasks` to generate task breakdown from this plan
2. Follow TDD workflow: Write tests → Implement → Refactor
3. Phase 1 (P1): Implement Gemini-only summarization with full feature set
4. Phase 2 (P2): Remove Gemini restriction, test with other providers
5. Phase 3 (P3): Add advanced features (save original, custom prompts via CLI)

---

**Plan Complete** | Ready for `/speckit.tasks` command to generate implementation tasks
