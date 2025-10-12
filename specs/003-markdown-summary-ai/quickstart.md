# Quickstart: AI-Powered Article Summarization

**Feature**: `003-markdown-summary-ai`
**Date**: 2025-10-12

## Prerequisites

- Python 3.10+
- UV package manager installed
- Existing crawler project set up
- Google Gemini API key (for P1)

## Setup

### 1. Install Dependencies

```bash
# Add LiteLLM to project
uv pip install litellm

# Verify installation
python -c "import litellm; print('LiteLLM installed successfully')"
```

### 2. Configure Environment

Create or update `.env` file in project root:

```ini
# Required: Default AI model
DEFAULT_AI_MODEL=gemini/gemini-pro

# Required: Google API key for Gemini models
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Other model providers (P2)
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key

# Existing Firecrawl configuration
FIRECRAWL_API_URL=http://localhost:3002
```

**Get Gemini API Key**:
1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy key to `.env` file

### 3. Verify Setup

```bash
# Test configuration (will fail if API key missing)
crawler summarize --url https://example.com

# If successful, you'll see an error like:
# "Error: DEFAULT_AI_MODEL not set in .env"
# This confirms validation is working!
```

## Basic Usage

### Simple Summary (Console Output)

```bash
crawler summarize --url https://example.com/article
```

Output:
```
Summarizing: https://example.com/article
Using model: gemini/gemini-pro

Summary:
--------
[Generated summary appears here in 3-5 key points]

Word count: 120 words
Tokens used: 1,750 (prompt: 1,500, completion: 250)
```

### Save Summary to File

```bash
crawler summarize --url https://example.com/article --output summary.md
```

Output:
```
Summary saved to: /path/to/summary.md
```

### Custom Summary Length

```bash
# Brief (1-2 sentences)
crawler summarize --url https://example.com/article --summary brief

# Standard (3-5 points) - default
crawler summarize --url https://example.com/article --summary standard

# Detailed (comprehensive)
crawler summarize --url https://example.com/article --summary detailed
```

### Save to Directory (Auto-Filename)

```bash
crawler summarize --url https://example.com/prompting-guide \
  --output ./summaries/

# Creates: ./summaries/prompting-guide-summary.md
```

## Troubleshooting

### Error: "Missing API key for model 'gemini/gemini-pro'"

**Solution**: Add `GOOGLE_API_KEY` to `.env` file

```bash
echo "GOOGLE_API_KEY=your_key_here" >> .env
```

### Error: "DEFAULT_AI_MODEL not set"

**Solution**: Add default model to `.env`

```bash
echo "DEFAULT_AI_MODEL=gemini/gemini-pro" >> .env
```

### Error: "Rate limit exceeded"

**Solution**: Wait and retry, or use a different model with higher rate limits

```bash
crawler summarize --url https://example.com/article \
  --model gemini/gemini-1.5-flash  # Faster model with higher limits
```

## Next Steps

- Read [plan.md](./plan.md) for architecture details
- Read [data-model.md](./data-model.md) for data structures
- Run `/speckit.tasks` to generate implementation tasks
- Follow TDD workflow: Write tests → Implement → Refactor

## P2 Features (Future)

- Multi-provider support (OpenAI, Anthropic, Ollama)
- Custom system prompts via CLI
- Batch summarization from URL list
