# Weather API

## Overview

A FastAPI service that aggregates weather data from multiple providers (OpenWeatherMap, WeatherAPI) with Redis caching and automatic failover.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│   Client     │────▶│  FastAPI App  │────▶│  Weather APIs  │
└─────────────┘     │  + Redis     │     │  (providers)   │
                    └──────────────┘     └────────────────┘
```

- **FastAPI** — async HTTP framework
- **Redis** — response cache (5 min TTL)
- **Docker** — containerized deployment

## Quick Reference

### Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
docker compose up -d redis
uvicorn src.main:app --reload
```

### Common Commands
| Command | Description |
|---------|-------------|
| `pytest` | Run tests |
| `docker compose up` | Start all services |
| `uvicorn src.main:app --reload` | Dev server |

## Key Paths

| Path | Description |
|------|-------------|
| `src/main.py` | FastAPI app entry point |
| `src/providers/` | Weather data providers |
| `src/cache.py` | Redis caching layer |
| `tests/` | Test suite |

## Workflow Rules

Read `../memory/agent-config/workflow.md` for global rules. Key rules:

1. **Plan Before Coding** — For any task with 3+ steps, outline first.
2. **Verify Before Done** — Never mark complete without proving it works.
3. **Learn From Mistakes** — Update `../memory/wiki/projects/weather-api.md` after corrections.
4. **No Blind Retries** — Diagnose root cause on failure.
5. **Keep It Simple** — Don't over-engineer.

## Reference Documents

| Document | Contents |
|----------|----------|
| `../memory/wiki/projects/weather-api.md` | Project wiki page (lessons, decisions) |
| `../memory/wiki/domains/fastapi.md` | FastAPI patterns and gotchas |
| `../memory/wiki/patterns/retry-with-backoff.md` | Retry pattern used in this project |

## Platform & Environment

- Python 3.11+
- Docker & Docker Compose
- Redis 7.x

## What NOT To Do

- Do not commit `.env` files or API keys
- Do not skip tests before marking a task done
- Do not over-engineer simple fixes
