---
title: Retry with Exponential Backoff
category: patterns
tags: [resilience, retry, api, python]
source_docs: []
date_created: 2026-04-01
date_updated: 2026-04-10
---

# Retry with Exponential Backoff

## Summary

A resilience pattern for API calls and connection attempts that retries failed operations with exponentially increasing delays. Prevents thundering-herd problems and respects rate limits.

## The Pattern

Using the `tenacity` library (Python):

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import httpx

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry {retry_state.attempt_number}/5 after {retry_state.outcome.exception()}"
    ),
)
async def call_weather_provider(url: str, params: dict) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
```

### Key Parameters

| Parameter | Recommendation | Why |
|-----------|---------------|-----|
| `stop_after_attempt` | 3–5 | Enough to survive transient failures, not so many to delay errors |
| `wait_exponential` min | 1s | Avoids hammering the server immediately |
| `wait_exponential` max | 30–60s | Caps the maximum wait to keep total time reasonable |
| `retry_if_exception_type` | Specific exceptions | Never retry on 4xx client errors (except 429) |

## When to Use

- **External API calls** — third-party providers with rate limits or occasional downtime
- **Database/cache connections** — transient connection failures (e.g., Redis pool exhaustion)
- **Distributed systems** — inter-service calls that may fail during deployments

## When NOT to Use

- **Client errors (4xx except 429)** — retrying a 400 Bad Request will never succeed
- **Authentication failures (401/403)** — indicates a config problem, not a transient issue (see [[api-auth-debugging]])
- **CPU-bound operations** — retrying a computation that failed due to bad input
- **Idempotency not guaranteed** — if the operation has side effects and you can't safely re-execute it

## Real Example

Discovered during [[weather-api]] Redis connection pool exhaustion (2026-04-01). The Redis client was running out of connections under load, causing transient `ConnectionError` exceptions. Adding retry-with-backoff gave the pool time to recycle connections:

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=5),
    retry=retry_if_exception_type(redis.exceptions.ConnectionError),
)
async def get_cached_weather(redis: Redis, key: str) -> Optional[dict]:
    data = await redis.get(key)
    return json.loads(data) if data else None
```

Later reused in [[recipe-chatbot]] for Azure OpenAI rate limiting. The Azure OpenAI API returns HTTP 429 with a `Retry-After` header during peak usage. The same tenacity pattern handles this gracefully:

```python
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception_type(openai.RateLimitError),
)
async def chat_completion(messages: list[dict]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content
```

## Related

- [[weather-api]] — origin project for this pattern
- [[recipe-chatbot]] — reused for Azure OpenAI rate limiting
- [[api-auth-debugging]] — complementary pattern for non-retryable auth failures

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
