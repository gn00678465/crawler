# Feature Specification: AI-Powered Article Summarization Command

**Feature Branch**: `003-markdown-summary-ai`
**Created**: 2025-10-12
**Status**: Draft
**Input**: User description: "參考目前的指令並新增一個新的指令，此指令只支援 markdown, 而且新增 --summary 的參數，此參數的主要目的為透過 AI 整理爬回文章的摘要，此指令主要的流程為， firecrawl -> markdown -> summary(新) -> output(or console)。"

## Clarifications

### Session 2025-10-12

- Q: When user does not specify `--model` parameter, how should the system handle it? → A: Read default model from environment variable (e.g., `DEFAULT_AI_MODEL`). If not set, display error. Must also configure corresponding API KEY for the model.
- Q: Which model providers should the `--model` parameter support? → A: Support cloud services (OpenAI, Anthropic Claude, Google Gemini) + local models (Ollama, vLLM, etc.). The `--model` parameter will override the default model in `.env`. Local models do not require API KEY.
- Q: What format should the `--model` parameter use? → A: Use full LiteLLM format (e.g., `openai/gpt-4o`, `ollama/llama3`, `azure/gpt-4-deployment`) supporting all LiteLLM prefixes.
- Q: How should the system handle multiple API KEY configurations for different providers? → A: Users configure all needed API KEYs in `.env` (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`). System automatically selects the corresponding KEY based on `--model`.
- Q: When a model cannot be used (non-existent model or missing API KEY), how should the system handle it? → A: Validate at startup: Check if the default model in `.env` and its API KEY are available. If unavailable, startup fails. Follow LiteLLM usage patterns for validation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Article Summarization (Priority: P1)

As a content researcher, I want to crawl a web article and receive an AI-generated summary, so that I can quickly understand the main points without reading the entire article.

**Why this priority**: This is the core functionality of the feature. It delivers immediate value by enabling users to extract key insights from web content efficiently, saving time and improving information consumption workflows.

**Independent Test**: Can be fully tested by running `crawler summarize --url <URL>` and verifying that a concise summary is displayed in the console, capturing the main points of the article.

**Acceptance Scenarios**:

1. **Given** a valid article URL, **When** user runs `crawler summarize --url https://example.com/article`, **Then** the article is crawled, converted to markdown, summarized by AI, and the summary is displayed in the console
2. **Given** a valid article URL, **When** user runs `crawler summarize --url https://example.com/article --output summary.md`, **Then** the AI-generated summary is saved to the specified file path
3. **Given** a short article (< 500 words), **When** user requests a summary, **Then** the AI generates a concise summary proportional to the content length (e.g., 2-3 sentences)
4. **Given** a long article (> 5000 words), **When** user requests a summary, **Then** the AI generates a comprehensive summary highlighting key sections and main arguments (e.g., 5-8 bullet points)
5. **Given** an invalid URL, **When** user runs the summarize command, **Then** an error message is displayed indicating the URL is invalid

---

### User Story 2 - Customizable Summary Length (Priority: P2)

As a busy professional, I want to control the length of the generated summary, so that I can get either a quick overview or a more detailed summary based on my needs.

**Why this priority**: Different use cases require different summary depths. Quick scanning needs brief summaries, while detailed analysis needs comprehensive ones. This enhances tool flexibility for diverse user needs.

**Independent Test**: Can be tested by running the same URL with different summary length options and verifying the output matches the requested length and detail level.

**Acceptance Scenarios**:

1. **Given** a URL, **When** user specifies `--summary brief`, **Then** the AI generates a 1-2 sentence executive summary
2. **Given** a URL, **When** user specifies `--summary standard`, **Then** the AI generates a balanced summary with 3-5 key points
3. **Given** a URL, **When** user specifies `--summary detailed`, **Then** the AI generates a comprehensive summary with main sections, arguments, and supporting details
4. **Given** no summary length specified, **When** user runs the command, **Then** the system uses standard length as the default

---

### User Story 3 - Multi-Language Article Support (Priority: P2)

As an international researcher, I want to summarize articles in various languages (Chinese, Japanese, Spanish, etc.) and receive summaries in the same language as the original, so that I can work with content in my native language or the language of my research domain.

**Why this priority**: Multi-language support is essential for global users and expands the tool's applicability. This should be part of the core feature set to avoid retrofitting language support later, which would be more complex.

**Independent Test**: Can be tested by crawling articles in different languages and verifying that the summary is generated in the same language as the source article.

**Acceptance Scenarios**:

1. **Given** a Chinese article URL, **When** user runs `crawler summarize --url <Chinese-article-URL>`, **Then** the summary is generated in Chinese
2. **Given** a Japanese article URL, **When** user runs the summarize command, **Then** the summary is generated in Japanese
3. **Given** a Spanish article URL, **When** user runs the summarize command, **Then** the summary is generated in Spanish
4. **Given** a mixed-language article (e.g., English with Chinese quotes), **When** user runs the summarize command, **Then** the system detects the primary language and generates the summary in that language

---

### User Story 4 - Flexible AI Model Selection (Priority: P1)

As a researcher with diverse needs, I want to choose which AI model to use for summarization (cloud services like OpenAI/Anthropic or local models like Ollama), so that I can balance between cost, quality, privacy, and performance based on my specific requirements.

**Why this priority**: Model selection is critical for the feature's viability. Different users have different constraints: some need offline/local processing for privacy, others prioritize quality with cloud models, and some need cost optimization. This flexibility is essential from day one to support diverse use cases.

**Independent Test**: Can be tested by configuring multiple API keys in `.env`, then running the command with different `--model` values and verifying the correct model provider is used.

**Acceptance Scenarios**:

1. **Given** `DEFAULT_AI_MODEL=openai/gpt-4o-mini` in `.env`, **When** user runs `crawler summarize --url <URL>` without `--model`, **Then** the summary is generated using `gpt-4o-mini` from OpenAI
2. **Given** valid API keys configured, **When** user runs `crawler summarize --url <URL> --model anthropic/claude-3-haiku-20240307`, **Then** the summary is generated using Claude 3 Haiku regardless of the default model
3. **Given** Ollama running locally, **When** user runs `crawler summarize --url <URL> --model ollama/llama3`, **Then** the summary is generated using the local Llama3 model without requiring an API key
4. **Given** `DEFAULT_AI_MODEL` not set in `.env`, **When** user runs the command without `--model`, **Then** the system displays an error message indicating the missing default model configuration
5. **Given** an invalid model name, **When** user runs `crawler summarize --url <URL> --model invalid/model`, **Then** the system fails at startup with a clear error message indicating the model is not available
6. **Given** a valid model but missing API key (e.g., `OPENAI_API_KEY` not in `.env`), **When** user runs `crawler summarize --url <URL> --model openai/gpt-4o`, **Then** the system fails at startup with a clear error indicating which API key is missing

---

### User Story 5 - Save Both Original and Summary (Priority: P3)

As a knowledge worker, I want to save both the original markdown content and the AI summary, so that I can reference the full article later while having quick access to the summary.

**Why this priority**: This is a convenience feature that combines archival and summarization. While valuable for documentation workflows, users can achieve this by running two separate commands if needed.

**Independent Test**: Can be tested by running with the `--save-original` flag and verifying that both the full markdown and summary are saved in appropriate files.

**Acceptance Scenarios**:

1. **Given** a URL with `--save-original` flag, **When** user runs `crawler summarize --url https://example.com/article --output ./docs/`, **Then** both the full article (article.md) and summary (article-summary.md) are saved in the docs directory
2. **Given** a custom filename specified, **When** user includes `--save-original`, **Then** the original is saved with the specified name and summary appends "-summary" to the filename
3. **Given** no `--save-original` flag, **When** user saves output, **Then** only the summary is saved

---

### Edge Cases

- What happens when the article is behind a paywall or requires authentication?
- How does the system handle articles with primarily visual content (images, videos) and minimal text?
- What happens when the crawled content is too short to meaningfully summarize (< 100 words)?
- How does the AI handle non-English content (e.g., Chinese, Japanese, Spanish articles)?
- What happens when the AI service is unavailable or returns an error?
- How does the system handle articles with complex formatting (tables, code blocks, mathematical equations)?
- What happens when the network connection is lost during the summarization process?
- How does the system handle very long articles (> 50,000 words) that may exceed AI token limits?
- How does the system detect the language of the source article for multi-language summarization?
- What happens when a user specifies an unsupported model format (e.g., `--model gpt-4o` without provider prefix)?
- What happens when multiple API keys are missing but the user hasn't specified which model to use?
- How does the system handle rate limiting from AI service providers (e.g., OpenAI API rate limits)?
- What happens when a local model service (Ollama) is specified but not running?
- How does the system behave when switching between different model providers in consecutive commands?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a new command `crawler summarize` for AI-powered article summarization
- **FR-002**: System MUST accept a URL via `--url <URL>` argument
- **FR-003**: System MUST crawl the specified URL and convert content to markdown format
- **FR-004**: System MUST send the markdown content to an AI service for summarization
- **FR-005**: System MUST display the generated summary in the console by default
- **FR-006**: System MUST support saving the summary to a file via `--output <path>` argument
- **FR-007**: System MUST support both file paths and directory paths for `--output`. When a directory is provided, generate filename as `<article-name>-summary.md`
- **FR-008**: System MUST validate URL format before attempting to crawl
- **FR-009**: System MUST handle AI service errors gracefully and display appropriate error messages
- **FR-010**: System MUST support summary length options: `brief`, `standard`, and `detailed` via `--summary <length>` parameter
- **FR-011**: System MUST use `standard` summary length as default when not specified
- **FR-012**: System MUST provide a `--save-original` flag to save both full markdown and summary
- **FR-013**: System MUST generate appropriate filenames when output is a directory: `<article-name>.md` for original and `<article-name>-summary.md` for summary
- **FR-014**: System MUST display clear error messages for failed operations (network errors, invalid URLs, AI service failures, access denied)
- **FR-015**: System MUST handle articles with minimal text content (< 100 words) by returning the original content or a message indicating insufficient content for summarization
- **FR-016**: System MUST support multi-language articles and generate summaries in the same language as the source article
- **FR-017**: System MUST detect the language of the source article automatically to ensure summary language matches the original
- **FR-018**: System MUST support a `--model <provider/model-name>` parameter to specify which AI model to use, following LiteLLM format (e.g., `openai/gpt-4o`, `anthropic/claude-3-haiku-20240307`, `ollama/llama3`)
- **FR-019**: System MUST read the default AI model from `DEFAULT_AI_MODEL` environment variable when `--model` is not specified
- **FR-020**: System MUST fail with a clear error message if `DEFAULT_AI_MODEL` is not set and `--model` is not provided
- **FR-021**: System MUST support multiple AI model providers including cloud services (OpenAI, Anthropic Claude, Google Gemini) and local models (Ollama, vLLM)
- **FR-022**: System MUST automatically select the appropriate API key based on the model provider (e.g., `OPENAI_API_KEY` for OpenAI models, `ANTHROPIC_API_KEY` for Anthropic models)
- **FR-023**: System MUST NOT require API keys for local model providers (Ollama, vLLM)
- **FR-024**: System MUST validate at startup that the configured default model and its required API key (if applicable) are available
- **FR-025**: System MUST fail at startup with a clear error message indicating which API key is missing when a cloud model is configured but its API key is not available
- **FR-026**: System MUST display the model being used in verbose mode or when explicitly requested by the user

### Assumptions

- LiteLLM library will be used for unified AI model integration, supporting multiple providers through a consistent interface
- AI service credentials (API keys) are configured in environment variables following provider-specific naming conventions (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- The markdown content extracted by Firecrawl is suitable for AI summarization (clean text, proper structure)
- AI models have reasonable token limits (can handle articles up to 50,000 words or equivalent tokens)
- Summary quality depends on AI model capabilities; no manual verification is performed
- Cloud AI service calls may incur costs; user is responsible for API usage and billing
- Local model services (Ollama, vLLM) must be running and accessible if specified
- Network connectivity is available for both web crawling and cloud AI API calls
- Default summary length is sufficient for most use cases (standard mode)
- The tool respects the same crawling rules as the base crawler (robots.txt, timeouts, redirects)
- AI models support multi-language content and can generate summaries in the same language as the input
- Language detection can be performed either by the AI service or through content analysis
- LiteLLM's model validation and error handling patterns will be followed for startup validation
- Users understand LiteLLM format conventions for specifying models (provider/model-name)

### Key Entities

- **Summarize Request**: Represents a summarization operation with attributes including source URL, selected AI model (or default), summary length preference, output path, save original flag, and timestamp
- **AI Model Configuration**: Represents the AI model to use with attributes including provider name, model name, full LiteLLM identifier (e.g., `openai/gpt-4o`), required API key name, and whether it's a local or cloud model
- **Article Content**: The markdown-formatted article extracted from the web page, including metadata such as title, URL, detected language, word count, and crawl timestamp
- **AI Summary**: The generated summary with attributes including summary text, output language, length mode, model used, generation timestamp, token usage, and source article reference
- **Output File(s)**: The saved result(s) including summary file and optionally the original markdown file, with attributes such as file path, format type, size, and creation timestamp

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully crawl and summarize a standard article (1000-3000 words) in under 15 seconds using cloud AI models
- **SC-002**: AI-generated summaries capture at least 90% of main topics as identified by human evaluation on a test set
- **SC-003**: Summary length modes produce outputs within expected ranges: brief (20-50 words), standard (75-150 words), detailed (200-400 words)
- **SC-004**: The tool successfully processes at least 95% of public articles without errors
- **SC-005**: Error messages clearly indicate failure reasons (network error, AI service error, invalid URL, missing API key, etc.) in 100% of error cases
- **SC-006**: Users can complete a basic summarization workflow (URL to console summary) with a single command in under 30 seconds
- **SC-007**: The summarization feature works seamlessly with the existing crawler architecture without breaking existing commands
- **SC-008**: Users can successfully switch between different AI model providers (OpenAI, Anthropic, Google, Ollama) using the `--model` parameter without errors
- **SC-009**: Startup validation catches missing API keys or invalid model configurations in 100% of cases before attempting summarization
- **SC-010**: The tool correctly identifies which API key is missing and provides actionable error messages in 100% of configuration error cases
