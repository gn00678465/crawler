# LiteLLM Completion API Contract

**Feature**: `003-markdown-summary-ai`
**API**: `litellm.completion()`
**Purpose**: Document expected LiteLLM API behavior for contract testing

## Request Format

```python
import litellm

response = litellm.completion(
    model="gemini/gemini-pro",  # Format: provider/model-name
    messages=[
        {
            "role": "system",
            "content": "You are a helpful summarizer. Summarize the following article concisely..."
        },
        {
            "role": "user",
            "content": "<article markdown content>"
        }
    ],
    temperature=0.3,  # Lower for factual summarization
    max_tokens=500    # Varies by summary length
)
```

## Response Format

```python
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "<generated summary text>"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 1500,
        "completion_tokens": 200,
        "total_tokens": 1700
    },
    "model": "gemini/gemini-pro"
}
```

## Error Scenarios

| Error Type | Exception | Handling |
|------------|-----------|----------|
| Invalid API Key | `litellm.exceptions.AuthenticationError` | Display "Missing or invalid API key for {provider}" |
| Model Not Found | `litellm.exceptions.BadRequestError` | Display "Model {model} not found or not supported" |
| Rate Limit | `litellm.exceptions.RateLimitError` | Display "Rate limit exceeded, please try again later" |
| Token Limit | `litellm.exceptions.ContextWindowExceededError` | Display "Article too long for model token limit" |
| Network Error | `litellm.exceptions.Timeout` / `APIConnectionError` | Display "Network error connecting to AI service" |

## Test Strategy

**Contract Tests** (`tests/contract/test_litellm_contract.py`):
- Mock litellm.completion() responses
- Verify response structure matches expected format
- Test all error scenarios with appropriate exceptions
- Validate multi-language prompt/response handling

**Example Test**:
```python
@patch('litellm.completion')
def test_litellm_returns_expected_structure(mock_completion):
    mock_completion.return_value = {
        "choices": [{"message": {"role": "assistant", "content": "Summary text"}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}
    }
    # Call AI service and verify structure
```
