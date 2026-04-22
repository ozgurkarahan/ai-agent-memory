---
title: FastAPI
category: domains
tags: [python, api, async]
source_docs: []
date_created: 2026-03-15
date_updated: 2026-04-10
---

# FastAPI

## Summary

FastAPI is a modern Python web framework for building APIs. It provides native async support, automatic OpenAPI documentation, and Pydantic-based validation. This page captures patterns, gotchas, and deployment knowledge accumulated across projects.

## Key Patterns

### Dependency Injection

FastAPI's `Depends()` system is the primary way to share resources (DB sessions, auth, config) across endpoints:

```python
async def get_db():
    async with async_session() as session:
        yield session

@app.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    ...
```

Use `Depends()` for: database sessions, authenticated user, configuration, external clients.

### Pydantic Models

Use separate models for request, response, and database:

```python
class WeatherRequest(BaseModel):
    location: str
    units: Literal["metric", "imperial"] = "metric"

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    conditions: str
    provider: str
```

### Async Endpoints

All I/O-bound endpoints should be `async def`. Use `def` only for CPU-bound work (FastAPI runs these in a threadpool automatically):

```python
# Good — async for I/O
async def get_weather(location: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PROVIDER_URL}?q={location}")
    return response.json()

# Good — sync for CPU-bound
def compute_forecast(data: list[float]) -> ForecastResult:
    return heavy_computation(data)
```

### Middleware

Common middleware stack:

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*.example.com"])

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response
```

## Common Gotchas

### Lifespan Events

FastAPI 0.100+ uses the `lifespan` context manager instead of `@app.on_event("startup")`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize connections
    app.state.redis = await aioredis.from_url(REDIS_URL)
    yield
    # Shutdown: clean up
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
```

**Gotcha**: The old `on_event` decorators still work but are deprecated. They don't support cleanup on shutdown properly.

### CORS Configuration

CORS must be added **before** other middleware. A common mistake is adding it after authentication middleware, which causes preflight `OPTIONS` requests to be blocked.

### Background Tasks

FastAPI's `BackgroundTasks` runs **after** the response is sent but **within the same process**. For long-running work, use a task queue (Celery, ARQ) instead:

```python
@app.post("/report")
async def generate_report(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, recipient="user@example.com")
    return {"status": "Report generation started"}
```

**Gotcha**: Background tasks share the event loop. A CPU-bound background task will block all requests.

## Projects Using This

- [[weather-api]] — async weather aggregation with Redis caching
- [[recipe-chatbot]] — AI chatbot with WebSocket support

## Related

- [[retry-with-backoff]] — resilience pattern commonly used with FastAPI async clients
- [[api-auth-debugging]] — auth debugging lessons from FastAPI projects

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
