# Implementation Tasks: AI-Powered Article Summarization

**Feature**: `003-markdown-summary-ai`
**Branch**: `003-markdown-summary-ai`
**Generated**: 2025-10-12

**Total Tasks**: 47
**Parallel Opportunities**: 18 tasks can run in parallel (marked with [P])

---

## Phase 1: Setup & Configuration (3 tasks)

### T001: Install LiteLLM Dependency
**Type**: Setup
**TDD Phase**: N/A (setup task)
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Add LiteLLM library to project dependencies and verify installation.

**Steps**:
1. Run `uv pip install litellm`
2. Verify installation with `python -c "import litellm; print('LiteLLM installed successfully')"`
3. Update `pyproject.toml` if needed

**Acceptance**:
- LiteLLM can be imported in Python
- No dependency conflicts

---

### T002: Create Environment Configuration Template
**Type**: Setup
**TDD Phase**: N/A (setup task)
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Add AI model configuration variables to `.env.example` template.

**Steps**:
1. Update `.env.example` with:
   ```ini
   # AI Model Configuration
   DEFAULT_AI_MODEL=gemini/gemini-pro
   GOOGLE_API_KEY=your_gemini_api_key_here

   # Optional: Other AI providers (P2)
   # OPENAI_API_KEY=your_openai_key
   # ANTHROPIC_API_KEY=your_anthropic_key
   ```

**Acceptance**:
- `.env.example` contains all required AI configuration variables
- Comments explain each variable's purpose

---

### T003: Create Default System Prompts Configuration
**Type**: Setup
**TDD Phase**: N/A (configuration)
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Create `src/config/prompts.py` with default system prompts for each summary length.

**Steps**:
1. Create `src/config/prompts.py`
2. Define three prompt templates:
   - `BRIEF_PROMPT`: "Summarize in 1-2 sentences..."
   - `STANDARD_PROMPT`: "Summarize in 3-5 key points..."
   - `DETAILED_PROMPT`: "Provide comprehensive summary..."
3. Include multi-language instruction in all prompts

**Acceptance**:
- `prompts.py` exists with three prompt constants
- Prompts include language-matching instructions
- Code passes `ruff check`

---

## Phase 2: Data Models (TDD) (15 tasks)

### T004: Write Tests for SummarizeRequest Model
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Write comprehensive unit tests for `SummarizeRequest` Pydantic model covering validation rules.

**Steps**:
1. Create `tests/unit/models/test_summarize_request.py`
2. Test valid instantiation with all fields
3. Test URL validation (valid HTTP/HTTPS, reject invalid URLs)
4. Test `summary_length` validation (only "brief", "standard", "detailed")
5. Test optional fields (`model`, `output_path`, `save_original`)
6. Test timestamp auto-generation
7. Test Pydantic JSON serialization/deserialization

**Acceptance**:
- All test cases written and failing (RED phase)
- Test coverage plan for edge cases documented
- Tests follow pytest conventions

---

### T005: Implement SummarizeRequest Model
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T004
**Can Parallelize**: No

**Description**:
Implement `SummarizeRequest` Pydantic model to pass all tests.

**Steps**:
1. Create `src/models/summarize_request.py`
2. Define Pydantic model with fields per `data-model.md`:
   - `url: HttpUrl`
   - `model: Optional[str]`
   - `summary_length: Literal["brief", "standard", "detailed"]`
   - `output_path: Optional[str]`
   - `save_original: bool`
   - `timestamp: datetime`
3. Add docstrings and type hints
4. Run tests until all pass (GREEN phase)

**Acceptance**:
- All T004 tests pass
- Model matches specification in `data-model.md`
- `mypy --strict` passes
- `ruff check` passes

---

### T006: Write Tests for AIModelConfiguration Model
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Write unit tests for `AIModelConfiguration` model including factory method.

**Steps**:
1. Create `tests/unit/models/test_ai_model_config.py`
2. Test `from_model_string()` factory method with various formats:
   - `gemini/gemini-pro` → provider="gemini", api_key_env_var="GOOGLE_API_KEY"
   - `openai/gpt-4o` → provider="openai", api_key_env_var="OPENAI_API_KEY"
   - `ollama/llama3` → provider="ollama", is_local=True, api_key_env_var=None
3. Test validation rejects invalid formats (no "/", empty parts)
4. Test `is_local` property for cloud vs local models

**Acceptance**:
- Tests fail initially (RED phase)
- Factory method test cases cover all providers
- Validation error tests included

---

### T007: Implement AIModelConfiguration Model
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T006
**Can Parallelize**: No

**Description**:
Implement `AIModelConfiguration` model with parsing logic.

**Steps**:
1. Create `src/models/ai_model_config.py`
2. Implement model fields per `data-model.md`
3. Implement `from_model_string()` classmethod with provider mapping
4. Add validator for `full_name` format
5. Run tests until all pass

**Acceptance**:
- All T006 tests pass
- Model matches specification
- `mypy --strict` passes

---

### T008: Write Tests for ArticleContent Model
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Write tests for `ArticleContent` model including computed properties.

**Steps**:
1. Create `tests/unit/models/test_article_content.py`
2. Test valid instantiation with required fields
3. Test `is_minimal` property (True when word_count < 100)
4. Test optional fields (`detected_language`, `metadata`)
5. Test URL validation
6. Test timestamp auto-generation

**Acceptance**:
- Tests written and failing (RED)
- Computed property tests included

---

### T009: Implement ArticleContent Model
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T008
**Can Parallelize**: No

**Description**:
Implement `ArticleContent` model to pass tests.

**Steps**:
1. Create `src/models/article_content.py`
2. Implement fields per `data-model.md`
3. Implement `is_minimal` property
4. Add docstrings
5. Run tests until all pass

**Acceptance**:
- All T008 tests pass
- Model matches specification
- `mypy --strict` passes

---

### T010: Write Tests for AISummary Model
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Write tests for `AISummary` model including metadata fields.

**Steps**:
1. Create `tests/unit/models/test_ai_summary.py`
2. Test valid instantiation with all required fields
3. Test optional `token_usage` dictionary structure
4. Test `output_language` validation
5. Test timestamp generation
6. Test JSON serialization with nested dict

**Acceptance**:
- Tests written and failing (RED)
- Token usage structure validated

---

### T011: Implement AISummary Model
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T010
**Can Parallelize**: No

**Description**:
Implement `AISummary` model to pass tests.

**Steps**:
1. Create `src/models/ai_summary.py`
2. Implement fields per `data-model.md`
3. Add docstrings
4. Run tests until all pass

**Acceptance**:
- All T010 tests pass
- Model matches specification
- `mypy --strict` passes

---

### T012: Write Tests for OutputFile Model Extension
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Write tests for `OutputFile` model (may already exist, verify/extend).

**Steps**:
1. Check if `src/models/output_file.py` exists
2. Create or extend `tests/unit/models/test_output_file.py`
3. Test `path_obj` property returns `pathlib.Path`
4. Test validation for `file_path`, `file_size`, `format`

**Acceptance**:
- Tests written (new or extended)
- Tests fail if model needs updates

---

### T013: Implement/Extend OutputFile Model
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T012
**Can Parallelize**: No

**Description**:
Implement or extend `OutputFile` model to pass tests.

**Steps**:
1. Create or update `src/models/output_file.py`
2. Add fields per `data-model.md` if not present
3. Implement `path_obj` property
4. Run tests until all pass

**Acceptance**:
- All T012 tests pass
- Model matches specification
- `mypy --strict` passes

---

### T014: Refactor All Models (Code Quality)
**Type**: Refactor
**TDD Phase**: REFACTOR
**Depends On**: T005, T007, T009, T011, T013
**Can Parallelize**: No

**Description**:
Refactor all models for code quality while keeping tests green.

**Steps**:
1. Add comprehensive docstrings to all models
2. Add JSON schema examples via `Config.json_schema_extra`
3. Ensure consistent code style
4. Run `ruff format src/models/`
5. Verify all model tests still pass

**Acceptance**:
- All model tests remain passing
- `ruff check src/models/` passes
- Docstrings follow Google style
- Code coverage ≥ 90% for models

---

### T015: Write Contract Tests for LiteLLM API
**Type**: Test (Contract)
**TDD Phase**: RED
**Depends On**: T007 (needs AIModelConfiguration)
**Can Parallelize**: [P]

**Description**:
Write contract tests verifying LiteLLM API response structure per `contracts/litellm-api.md`.

**Steps**:
1. Create `tests/contract/test_litellm_contract.py`
2. Mock `litellm.completion()` responses
3. Test expected response structure (choices, usage, model fields)
4. Test error scenarios:
   - `AuthenticationError` for invalid API key
   - `BadRequestError` for invalid model
   - `RateLimitError` for rate limits
   - `ContextWindowExceededError` for token limits
5. Test multi-language prompt/response

**Acceptance**:
- Tests written and failing (RED)
- All error types covered
- Mock responses match documented structure

---

### T016: Write Contract Tests for CLI Summarize Command
**Type**: Test (Contract)
**TDD Phase**: RED
**Depends On**: T005 (needs SummarizeRequest)
**Can Parallelize**: [P]

**Description**:
Write contract tests for CLI command interface per `contracts/cli-summarize.md`.

**Steps**:
1. Create `tests/integration/test_summarize_cli.py`
2. Use `typer.testing.CliRunner` for CLI invocation
3. Test all parameter combinations:
   - Required: `--url`
   - Optional: `--model`, `--summary`, `--output`, `--save-original`
4. Test exit codes (0=success, 1=error, 2=config error, 3=AI error)
5. Test console output format
6. Test file creation when `--output` specified

**Acceptance**:
- Tests written and failing (RED)
- All parameter combinations covered
- Exit code tests included

---

### T017: Extend Custom Exceptions for AI Errors
**Type**: Implementation
**TDD Phase**: N/A (infrastructure)
**Depends On**: None
**Can Parallelize**: [P]

**Description**:
Extend `src/lib/exceptions.py` with AI-specific exceptions.

**Steps**:
1. Add `AIServiceError(CrawlerError)` base class
2. Add `ConfigurationError(CrawlerError)` for missing keys/invalid models
3. Add `ModelNotFoundError(AIServiceError)`
4. Add `RateLimitExceededError(AIServiceError)`
5. Add `TokenLimitExceededError(AIServiceError)`
6. Map to exit codes per contract

**Acceptance**:
- All AI exception classes defined
- Docstrings explain when each is raised
- Exit code mapping documented

---

### T018: Update Settings for AI Configuration
**Type**: Implementation
**TDD Phase**: N/A (configuration)
**Depends On**: T007
**Can Parallelize**: [P]

**Description**:
Extend `src/config/settings.py` with AI model settings section.

**Steps**:
1. Add `AISettings` class with Pydantic BaseSettings:
   - `default_ai_model: Optional[str]` (from `DEFAULT_AI_MODEL` env var)
   - `google_api_key: Optional[str]` (from `GOOGLE_API_KEY`)
   - `openai_api_key: Optional[str]` (P2 - commented)
   - `anthropic_api_key: Optional[str]` (P2 - commented)
2. Add validation method for P1 (Gemini-only check)
3. Integrate into existing settings structure

**Acceptance**:
- Settings load from `.env` correctly
- Type hints and docstrings complete
- `mypy --strict` passes

---

## Phase 3: User Story 1 - Basic Article Summarization (P1) (8 tasks)

### T019: Write Unit Tests for AI Service (Core Functionality)
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: T011, T015, T017
**Can Parallelize**: No

**Description**:
Write unit tests for `AIService` core summarization logic.

**Steps**:
1. Create `tests/unit/services/test_ai_service.py`
2. Mock `litellm.completion()` responses
3. Test `summarize(article_content: ArticleContent, config: AIModelConfiguration) -> AISummary`:
   - Success case with valid response
   - Token usage extraction
   - Model identifier tracking
4. Test error translation:
   - LiteLLM exceptions → our custom exceptions
   - Error messages contain actionable info
5. Test multi-language article handling

**Acceptance**:
- Tests written and failing (RED)
- All error paths covered
- Mocked responses realistic

---

### T020: Implement AI Service Core
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T019
**Can Parallelize**: No

**Description**:
Implement `AIService` class with LiteLLM integration.

**Steps**:
1. Create `src/services/ai_service.py`
2. Implement `summarize()` method:
   - Load system prompt from `config/prompts.py` (standard length for now)
   - Call `litellm.completion()` with message format
   - Extract summary text from response
   - Build `AISummary` object with metadata
3. Implement error handling with custom exceptions
4. Add logging for API calls and token usage
5. Run tests until all pass

**Acceptance**:
- All T019 tests pass
- Error translation works correctly
- Logging provides debugging info
- `mypy --strict` passes

---

### T021: Write Unit Tests for Prompt Service
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: T003
**Can Parallelize**: [P]

**Description**:
Write tests for `PromptService` loading system prompts.

**Steps**:
1. Create `tests/unit/services/test_prompt_service.py`
2. Test `get_system_prompt(length: str) -> str`:
   - Returns correct prompt for each length ("brief", "standard", "detailed")
   - Raises error for invalid length
3. Test prompt content includes multi-language instruction
4. Test environment variable override (P3 feature, skip for now)

**Acceptance**:
- Tests written and failing (RED)
- All summary lengths covered

---

### T022: Implement Prompt Service
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T021
**Can Parallelize**: No

**Description**:
Implement `PromptService` for managing system prompts.

**Steps**:
1. Create `src/services/prompt_service.py`
2. Implement `get_system_prompt(length: str) -> str`:
   - Import prompts from `config/prompts.py`
   - Return appropriate prompt based on length
   - Raise `ValueError` for invalid length
3. Add docstrings
4. Run tests until all pass

**Acceptance**:
- All T021 tests pass
- Code follows project conventions
- `mypy --strict` passes

---

### T023: Write Unit Tests for CLI Summarize Command (Basic Flow)
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: T016, T020, T022
**Can Parallelize**: No

**Description**:
Write unit tests for `summarize` CLI command orchestration logic.

**Steps**:
1. Create `tests/unit/cli/test_summarize.py`
2. Mock all service dependencies (firecrawl, AI service, file output)
3. Test basic flow:
   - Parse CLI arguments → `SummarizeRequest`
   - Call firecrawl service → `ArticleContent`
   - Call AI service → `AISummary`
   - Display to console (default) or save to file
4. Test error handling for each service call
5. Test console output format

**Acceptance**:
- Tests written and failing (RED)
- All dependencies mocked
- Flow coverage complete

---

### T024: Implement CLI Summarize Command (Basic Flow)
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T023
**Can Parallelize**: No

**Description**:
Implement `crawler summarize` CLI command with basic orchestration.

**Steps**:
1. Create `src/cli/summarize.py`
2. Define Typer command with parameters:
   - `--url` (required)
   - `--model` (optional, uses `DEFAULT_AI_MODEL` if not set)
   - `--summary` (optional, default="standard")
   - `--output` (optional, default=console)
3. Implement orchestration:
   - Validate URL
   - Create `SummarizeRequest`
   - Call firecrawl service (reuse existing)
   - Build `AIModelConfiguration`
   - Call AI service
   - Output to console or file
4. Add error handling with appropriate exit codes
5. Run tests until all pass

**Acceptance**:
- All T023 tests pass
- CLI can be invoked via `crawler summarize`
- Error messages user-friendly
- `mypy --strict` passes

---

### T025: Write Integration Tests for End-to-End Flow
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T024
**Can Parallelize**: No

**Description**:
Write integration tests for complete summarize workflow.

**Steps**:
1. Update `tests/integration/test_summarize_cli.py`
2. Test with mocked LiteLLM but real CLI runner:
   - Basic: `crawler summarize --url <URL>` → console output
   - File output: `--output summary.md` → file created
   - Directory output: `--output ./summaries/` → auto-filename
3. Test error scenarios:
   - Invalid URL → exit code 1
   - Missing API key → exit code 2
   - AI service error → exit code 3
4. Verify console output format matches contract

**Acceptance**:
- Integration tests written
- All scenarios covered
- Tests can run with mocked AI service

---

### T026: Implement Startup Validation for AI Configuration
**Type**: Implementation
**TDD Phase**: GREEN (extends T024)
**Depends On**: T018, T024
**Can Parallelize**: No

**Description**:
Add startup validation for AI model configuration per FR-024, FR-025.

**Steps**:
1. In `src/cli/summarize.py`, add validation before executing command:
   - Check `DEFAULT_AI_MODEL` exists (if `--model` not provided)
   - Parse model string into `AIModelConfiguration`
   - Check required API key exists (skip for local models)
   - For P1: Verify model is Gemini (reject others with "Coming soon")
2. Display clear error with missing variable name
3. Add tests in T025 for validation scenarios

**Acceptance**:
- Validation runs at startup
- Missing API key → clear error message with env var name
- Invalid model → actionable error
- P1 restriction enforced (Gemini-only)
- All T025 tests pass

---

### T027: Refactor User Story 1 Implementation
**Type**: Refactor
**TDD Phase**: REFACTOR
**Depends On**: T026
**Can Parallelize**: No

**Description**:
Refactor all User Story 1 code for quality while keeping tests green.

**Steps**:
1. Extract duplicated logic into helper functions
2. Improve error messages for clarity
3. Add comprehensive docstrings
4. Optimize imports
5. Run `ruff format` on all modified files
6. Verify all tests still pass

**Acceptance**:
- All User Story 1 tests pass (unit + integration)
- Code coverage ≥ 80%
- `ruff check` passes
- `mypy --strict` passes
- Docstrings complete

---

## Phase 4: User Story 2 - Customizable Summary Length (P2) (4 tasks)

### T028: Write Tests for Summary Length Parameter
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T027
**Can Parallelize**: No

**Description**:
Write tests verifying different summary lengths produce appropriate outputs.

**Steps**:
1. Extend `tests/integration/test_summarize_cli.py`
2. Test `--summary brief` → short output (mock response ~30 words)
3. Test `--summary standard` → medium output (mock response ~100 words)
4. Test `--summary detailed` → long output (mock response ~300 words)
5. Test default (no `--summary`) → uses "standard"
6. Test invalid length → error message

**Acceptance**:
- Tests written and failing (RED)
- All length options covered
- Mock responses realistic for each length

---

### T029: Implement Summary Length Support in AI Service
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T028
**Can Parallelize**: No

**Description**:
Update `AIService` to use different prompts based on summary length.

**Steps**:
1. Modify `AIService.summarize()` signature to accept `summary_length: str`
2. Call `PromptService.get_system_prompt(summary_length)` instead of hardcoded "standard"
3. Adjust `max_tokens` parameter based on length:
   - brief: 100 tokens
   - standard: 300 tokens
   - detailed: 600 tokens
4. Update tests to pass length parameter
5. Run tests until all pass

**Acceptance**:
- All T028 tests pass
- Correct prompt selected for each length
- Token limits appropriate
- Existing tests still pass

---

### T030: Update CLI to Pass Summary Length to AI Service
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T029
**Can Parallelize**: No

**Description**:
Wire up `--summary` parameter from CLI to AI service.

**Steps**:
1. Update `src/cli/summarize.py` to pass `summary_length` to AI service
2. Validate `--summary` accepts only ["brief", "standard", "detailed"]
3. Update help text to explain each option
4. Run integration tests

**Acceptance**:
- CLI accepts `--summary` parameter
- Validation rejects invalid values
- Help text clear and accurate
- All T028 tests pass

---

### T031: Write Success Criteria Tests for Summary Length
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T030
**Can Parallelize**: No

**Description**:
Write tests verifying SC-003 (summary length ranges).

**Steps**:
1. Create `tests/integration/test_summary_length_criteria.py`
2. Test with real LiteLLM (or high-fidelity mocks):
   - brief → 20-50 words
   - standard → 75-150 words
   - detailed → 200-400 words
3. Use word count validation
4. Test across multiple sample articles

**Acceptance**:
- Tests verify word count ranges
- Multiple articles tested
- Tests pass with real/high-fidelity AI responses

---

## Phase 5: User Story 3 - Multi-Language Support (P2) (3 tasks)

### T032: Write Tests for Multi-Language Detection
**Type**: Test (Unit)
**TDD Phase**: RED
**Depends On**: T009
**Can Parallelize**: [P]

**Description**:
Write tests for language detection in `ArticleContent`.

**Steps**:
1. Extend `tests/unit/models/test_article_content.py`
2. Test `detected_language` field populated correctly:
   - Chinese article → "zh"
   - Japanese article → "ja"
   - Spanish article → "es"
   - English article → "en"
3. Test mixed-language articles (primary language detection)

**Acceptance**:
- Tests written for common languages
- Detection logic testable (may need helper function)

---

### T033: Implement Language Detection Logic
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T032
**Can Parallelize**: No

**Description**:
Implement language detection for article content (simple approach).

**Steps**:
1. Option A: Rely on AI to detect language (include in system prompt)
2. Option B: Use library like `langdetect` (add dependency if needed)
3. For MVP, implement Option A (AI-based detection):
   - Update system prompts to include: "Detect the article language and respond in the same language"
   - Store detected language in `AISummary.output_language`
4. Run tests

**Acceptance**:
- Language detection works for test cases
- No additional dependencies (P1)
- AI responds in source language
- All T032 tests pass

---

### T034: Write Integration Tests for Multi-Language Summarization
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T033
**Can Parallelize**: No

**Description**:
Write integration tests for multi-language article summarization per User Story 3 acceptance scenarios.

**Steps**:
1. Create `tests/integration/test_multilingual_summarization.py`
2. Test scenarios from spec:
   - Chinese article → Chinese summary
   - Japanese article → Japanese summary
   - Spanish article → Spanish summary
   - Mixed-language article → primary language summary
3. Mock realistic LiteLLM responses in different languages
4. Verify `AISummary.output_language` matches source

**Acceptance**:
- All language scenarios covered
- Mocked responses realistic
- Tests verify language matching
- Tests pass with current implementation

---

## Phase 6: User Story 4 - Flexible AI Model Selection (P1) (4 tasks)

### T035: Write Tests for Model Parameter Override
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T026
**Can Parallelize**: No

**Description**:
Write tests verifying `--model` parameter overrides default model.

**Steps**:
1. Extend `tests/integration/test_summarize_cli.py`
2. Test scenarios from User Story 4:
   - Default model from `.env` used when `--model` not specified
   - `--model gemini/gemini-1.5-flash` overrides default
   - `--model ollama/llama3` uses local model (no API key required)
   - Missing `DEFAULT_AI_MODEL` → error at startup
   - Invalid model format → error at startup
   - Valid model but missing API key → error at startup
3. Mock environment variables for different scenarios

**Acceptance**:
- Tests written for all scenarios
- Environment variable mocking works
- Tests fail initially (RED)

---

### T036: Implement Model Parameter Override Logic
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T035
**Can Parallelize**: No

**Description**:
Implement `--model` parameter handling in CLI command.

**Steps**:
1. Update `src/cli/summarize.py`:
   - If `--model` provided, use it
   - Else, read from `DEFAULT_AI_MODEL` env var
   - If neither, raise `ConfigurationError`
2. Build `AIModelConfiguration` from model string
3. Validate API key for cloud models
4. Skip API key check for local models (is_local=True)
5. Run tests until all pass

**Acceptance**:
- All T035 tests pass
- `--model` parameter works correctly
- Default model fallback works
- Validation errors clear and actionable

---

### T037: Write Tests for P1 Gemini-Only Restriction
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T036
**Can Parallelize**: No

**Description**:
Write tests verifying P1 restriction (Gemini models only).

**Steps**:
1. Create `tests/integration/test_model_provider_restriction.py`
2. Test Gemini models pass validation:
   - `gemini/gemini-pro`
   - `gemini/gemini-1.5-flash`
3. Test non-Gemini models rejected with "Coming soon" message:
   - `openai/gpt-4o` → error
   - `anthropic/claude-3-haiku` → error
   - `ollama/llama3` → error (P1 restriction)
4. Verify error message explains P2 expansion

**Acceptance**:
- Tests written for P1 restriction
- Error message helpful
- Tests fail initially

---

### T038: Implement P1 Gemini-Only Validation
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T037
**Can Parallelize**: No

**Description**:
Add P1 restriction validation for Gemini-only models.

**Steps**:
1. In `src/config/settings.py`, add validation method:
   - Check if provider is "gemini"
   - If not, raise `ConfigurationError`: "Only Gemini models supported in P1. Support for {provider} coming in P2."
2. Call validation in CLI startup (T026)
3. Run tests until all pass

**Acceptance**:
- All T037 tests pass
- Non-Gemini models blocked
- Error message references P2
- Gemini models work correctly

---

## Phase 7: User Story 5 - Save Both Original and Summary (P3) (3 tasks)

### T039: Write Tests for --save-original Flag
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T027
**Can Parallelize**: No

**Description**:
Write tests for `--save-original` flag per User Story 5 acceptance scenarios.

**Steps**:
1. Extend `tests/integration/test_summarize_cli.py`
2. Test scenarios:
   - `--output ./docs/ --save-original` → saves both files:
     - `article.md` (original)
     - `article-summary.md` (summary)
   - `--output custom.md --save-original` → saves:
     - `custom.md` (original)
     - `custom-summary.md` (summary)
   - No `--save-original` → only summary saved
3. Verify file contents correct
4. Test directory creation if needed

**Acceptance**:
- Tests written for all scenarios
- File naming logic tested
- Tests fail initially (RED)

---

### T040: Implement --save-original Flag
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T039
**Can Parallelize**: No

**Description**:
Implement `--save-original` flag functionality.

**Steps**:
1. Update `src/cli/summarize.py`:
   - Add `--save-original` boolean parameter
   - When True and `--output` provided:
     - Save original markdown to base filename
     - Save summary to `{base}-summary.md`
   - Reuse existing file output service
2. Handle directory vs file path logic
3. Run tests until all pass

**Acceptance**:
- All T039 tests pass
- Both files saved with correct names
- File contents correct
- Existing functionality unaffected

---

### T041: Refactor File Output Logic
**Type**: Refactor
**TDD Phase**: REFACTOR
**Depends On**: T040
**Can Parallelize**: No

**Description**:
Refactor file output logic for clarity and DRY principles.

**Steps**:
1. Extract filename generation logic into helper function
2. Consolidate duplicate file writing code
3. Add comprehensive docstrings
4. Run `ruff format`
5. Verify all tests still pass

**Acceptance**:
- All file output tests pass
- No code duplication
- Helper functions well-documented
- `ruff check` passes

---

## Final Phase: Polish & Integration (6 tasks)

### T042: Write Tests for Edge Cases
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T027, T031, T034, T038, T041
**Can Parallelize**: No

**Description**:
Write tests for edge cases listed in spec.

**Steps**:
1. Create `tests/integration/test_edge_cases.py`
2. Test key edge cases:
   - Article behind paywall → crawl error
   - Minimal text content (< 100 words) → handled gracefully
   - Very long article (> 50,000 words) → token limit error
   - Network error during crawl → clear error message
   - AI service unavailable → clear error message
   - Rate limit exceeded → clear error message with retry suggestion
3. Verify error messages actionable

**Acceptance**:
- Edge cases covered
- Error handling comprehensive
- Tests document expected behavior

---

### T043: Implement Edge Case Handling
**Type**: Implementation
**TDD Phase**: GREEN
**Depends On**: T042
**Can Parallelize**: No

**Description**:
Implement handling for documented edge cases.

**Steps**:
1. Update error handling in all services:
   - Catch `ContextWindowExceededError` → suggest shorter article or summary mode
   - Catch network errors → suggest checking connection
   - Catch rate limit errors → suggest waiting or using different model
2. For minimal content (< 100 words):
   - Use `ArticleContent.is_minimal` property
   - Either skip AI call and return content, or use brief mode
3. Run tests until all pass

**Acceptance**:
- All T042 tests pass
- Edge cases handled gracefully
- Error messages helpful
- User experience smooth

---

### T044: Write Success Criteria Validation Tests
**Type**: Test (Integration)
**TDD Phase**: RED
**Depends On**: T043
**Can Parallelize**: No

**Description**:
Write tests validating success criteria SC-001 through SC-010.

**Steps**:
1. Create `tests/integration/test_success_criteria.py`
2. Test measurable outcomes:
   - SC-001: Timing test (< 15 seconds for standard article)
   - SC-004: Success rate test (95% of public URLs)
   - SC-005: Error message clarity (100% have actionable info)
   - SC-006: Workflow speed (< 30 seconds end-to-end)
   - SC-008: Model switching test (no errors)
   - SC-009: Startup validation catches 100% of config errors
   - SC-010: Error messages identify missing API keys 100%
3. Use realistic test data

**Acceptance**:
- All success criteria testable
- Tests document requirements
- Baseline performance measured

---

### T045: Add Verbose Mode and Logging
**Type**: Implementation
**TDD Phase**: GREEN (extends existing)
**Depends On**: T044
**Can Parallelize**: No

**Description**:
Add verbose mode to display model usage and token stats per FR-026.

**Steps**:
1. Add `--verbose` flag to CLI command
2. When enabled, display:
   - Model being used
   - Token usage (prompt, completion, total)
   - Processing time
   - Detected language
3. Add structured logging to all services
4. Configure log levels (INFO, DEBUG, ERROR)
5. Run tests

**Acceptance**:
- `--verbose` displays additional info
- Logging configuration flexible
- No breaking changes to existing tests
- Helpful for debugging

---

### T046: Update Documentation and README
**Type**: Documentation
**TDD Phase**: N/A
**Depends On**: T045
**Can Parallelize**: No

**Description**:
Update project documentation to reflect new feature.

**Steps**:
1. Update main README.md:
   - Add `crawler summarize` to command list
   - Add quickstart example
   - Link to feature quickstart guide
2. Verify `specs/003-markdown-summary-ai/quickstart.md` accurate
3. Update CLAUDE.md if needed (should be done via script)
4. Add usage examples to CLI help text
5. Create troubleshooting section in README

**Acceptance**:
- Documentation complete and accurate
- Examples tested and working
- Links valid
- Markdown formatted correctly

---

### T047: Final Integration Testing and Code Coverage
**Type**: Test (Integration)
**TDD Phase**: REFACTOR
**Depends On**: T046
**Can Parallelize**: No

**Description**:
Run full test suite and ensure code coverage meets requirements.

**Steps**:
1. Run full test suite: `pytest tests/`
2. Generate coverage report: `pytest --cov=src --cov-report=html`
3. Verify coverage ≥ 80% (Constitution requirement)
4. Fix any failing tests
5. Address coverage gaps if needed
6. Run `ruff check` and `mypy --strict` on entire codebase
7. Fix any linting or type errors

**Acceptance**:
- All tests pass (unit + integration + contract)
- Code coverage ≥ 80%
- `ruff check` passes with zero errors
- `mypy --strict` passes with zero errors
- No regressions in existing features
- Feature ready for merge

---

## Task Summary

**Total Tasks**: 47

**By Type**:
- Setup: 3 tasks (T001-T003)
- Tests (RED phase): 18 tasks
- Implementation (GREEN phase): 19 tasks
- Refactor: 4 tasks (T014, T027, T041, T047)
- Documentation: 1 task (T046)
- Configuration: 2 tasks (T017, T018)

**By Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Data Models): 15 tasks
- Phase 3 (User Story 1 - P1): 8 tasks
- Phase 4 (User Story 2 - P2): 4 tasks
- Phase 5 (User Story 3 - P2): 3 tasks
- Phase 6 (User Story 4 - P1): 4 tasks
- Phase 7 (User Story 5 - P3): 3 tasks
- Final (Polish): 6 tasks

**Parallelizable Tasks**: 18 tasks marked with [P]

**Estimated MVP Scope** (User Story 1 + User Story 4):
- Phases 1-3 + Phase 6 = 26 tasks
- Delivers: Basic summarization with flexible model selection
- Excludes: Custom summary lengths (P2), multi-language (P2), save-original (P3)

**Dependencies**:
- Critical path: T001 → T004-T005 → T019-T020 → T023-T024 → T025-T026 → T027
- Parallel opportunities in model development (T004-T013 can partially overlap)
- Integration tests depend on implementation completion

---

## Next Steps

1. **Review this task plan** with team/stakeholders
2. **Decide on MVP scope**:
   - Option A: Full P1 (Phases 1-3 + Phase 6) = 26 tasks
   - Option B: All user stories (all phases) = 47 tasks
3. **Run `/speckit.implement`** to execute tasks in TDD workflow
4. **Track progress** via todo list and task completion
5. **Iterate** based on test feedback and discoveries

---

**Plan Complete** | Ready for implementation via `/speckit.implement` command
