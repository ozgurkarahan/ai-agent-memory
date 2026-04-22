---
title: Recipe Chatbot
category: projects
tags: [python, fastapi, azure-openai, chatbot, sqlite]
source_docs: []
date_created: 2026-04-05
date_updated: 2026-04-10
---

# Recipe Chatbot

## Summary

An AI-powered recipe recommendation chatbot that suggests recipes based on user preferences, available ingredients, and dietary restrictions. Built with [[fastapi]] and Azure OpenAI GPT-4o, with conversation history stored in SQLite.

## Architecture

```
User → FastAPI (WebSocket + REST) → Conversation Manager → Azure OpenAI GPT-4o
                                          ↕
                                    SQLite (conversations, user preferences)
```

- **Framework**: [[fastapi]] with WebSocket support for real-time chat
- **LLM**: Azure OpenAI GPT-4o (chat completions API)
- **Storage**: SQLite for conversation history and user preference profiles
- **Prompt Engineering**: System prompt with recipe domain knowledge, user context injection

## Technical Reference

| Component | Detail |
|-----------|--------|
| Python | 3.11 |
| Framework | FastAPI 0.110+ |
| LLM | Azure OpenAI GPT-4o (2024-05-13) |
| Database | SQLite 3 |
| SDK | openai 1.x (Azure configuration) |

### Key Files

- `app/main.py` — FastAPI app with REST and WebSocket routes
- `app/chat.py` — Conversation manager, context window handling
- `app/prompts/` — System prompts and few-shot examples
- `app/models.py` — SQLAlchemy models for conversations and preferences
- `app/openai_client.py` — Azure OpenAI client with retry logic

## Lessons Learned

### 2026-04-10 — Token limit exceeded on long conversations

Users who had extended recipe discussions (20+ messages) hit the GPT-4o context window limit, causing `InvalidRequestError: max context length exceeded`.

**Root cause**: The full conversation history was sent with every request. A 30-message conversation with recipe details easily exceeded 8K tokens.

**Fix**: Implemented a sliding window with summarization:
1. Keep the last 10 messages verbatim
2. Summarize older messages into a compact context block using a cheaper model (GPT-4o-mini)
3. Inject the summary as a system message prefix

**Lesson**: Always design for conversation length limits from the start. Budget tokens: system prompt (~500), context summary (~500), recent messages (~3000), response (~1000).

## Cross-References

Reused the retry pattern from [[weather-api]] for Azure OpenAI rate limiting — see [[retry-with-backoff]]. The `tenacity` retry decorator handles HTTP 429 responses from Azure OpenAI with exponential backoff, which was critical during peak usage.

## Related

- [[fastapi]] — framework deep-dive, shared patterns with [[weather-api]]
- [[weather-api]] — sibling project, source of the retry pattern
- [[retry-with-backoff]] — resilience pattern used for Azure OpenAI calls

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
