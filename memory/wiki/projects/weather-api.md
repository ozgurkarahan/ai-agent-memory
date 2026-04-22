---
title: Weather API
category: projects
tags: [python, fastapi, redis, api, docker]
source_docs: []
date_created: 2026-03-15
date_updated: 2026-04-01
---

# Weather API

## Summary

A FastAPI service that aggregates weather data from multiple providers (OpenWeatherMap, WeatherAPI) and serves a unified REST API. Uses Redis for caching to reduce provider API calls and improve response times.

## Architecture

```
Client → FastAPI (uvicorn) → Provider Adapter Layer → OpenWeatherMap API
                                                    → WeatherAPI
         ↕
       Redis Cache (TTL-based, per-location)
```

- **Framework**: [[fastapi]] with async endpoints for concurrent provider calls
- **Cache**: Redis with 15-minute TTL per location key
- **Providers**: Adapter pattern — each provider implements a `WeatherProvider` protocol
- **Deployment**: Docker Compose (app + Redis), deployed to Azure Container Apps

## Technical Reference

| Component | Detail |
|-----------|--------|
| Python | 3.11 |
| Framework | FastAPI 0.110+ |
| Cache | Redis 7.x |
| Container | Docker + Docker Compose |
| Providers | OpenWeatherMap, WeatherAPI |
| CI | GitHub Actions |

### Key Files

- `app/main.py` — FastAPI app, lifespan, routes
- `app/providers/` — Provider adapters (openweathermap.py, weatherapi.py)
- `app/cache.py` — Redis connection pool and cache helpers
- `app/config.py` — Pydantic Settings for env var loading

## Lessons Learned

### 2026-03-20 — API key rotation caused downtime

Rotated the OpenWeatherMap API key but forgot to update the environment variable in the production Container App. The app kept using the old key from the Docker image's cached layer.

**Root cause**: `.env` file was baked into the Docker image at build time instead of being injected at runtime.

**Fix**: Moved all secrets to Azure Container App secrets (injected as env vars at runtime). Added a `/health` endpoint that validates API keys on startup.

**See also**: [[api-auth-debugging]] for the full debugging pattern.

### 2026-04-01 — Redis connection pool exhaustion

Under load testing, the app started throwing `redis.exceptions.ConnectionError` after ~200 concurrent requests. The default connection pool size (10) was too small.

**Root cause**: Each request opened a new Redis connection instead of reusing the pool. The `aioredis` client was instantiated per-request instead of per-app.

**Fix**: Moved Redis client to app lifespan, configured pool with `max_connections=50`, and added [[retry-with-backoff]] for transient connection failures.

**Lesson**: Always configure connection pool limits explicitly. Defaults are designed for development, not production.

## Decision Record

### Why FastAPI over Flask

**Date**: 2026-03-15
**Decision**: Use [[fastapi]] instead of Flask.

**Context**: Need to call multiple weather providers concurrently per request. Flask's synchronous model would require threading or Celery.

**Rationale**:
- Native `async/await` support for concurrent provider calls
- Built-in OpenAPI docs (auto-generated Swagger UI)
- Pydantic integration for request/response validation
- Better performance under concurrent load

**Trade-off**: Smaller ecosystem than Flask, but sufficient for our needs. Team already had FastAPI experience from [[recipe-chatbot]] prototyping.

## Related

- [[fastapi]] — framework deep-dive
- [[retry-with-backoff]] — pattern used for Redis and provider resilience
- [[api-auth-debugging]] — debugging lesson from API key rotation incident
- [[recipe-chatbot]] — sibling project, shares FastAPI patterns

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
