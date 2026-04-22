---
title: API Authentication Debugging
category: lessons
tags: [debugging, api, auth, docker, env-vars]
source_docs: []
date_created: 2026-03-20
date_updated: 2026-04-10
---

# API Authentication Debugging

## Summary

Common authentication debugging patterns discovered across API projects. Covers environment variable issues, Docker caching pitfalls, and verification strategies for API keys and tokens.

## Failed Attempt: The Stale Key Trap

In [[weather-api]], a 401 Unauthorized started appearing after rotating the OpenWeatherMap API key. The initial instinct was to regenerate the key again — but the real issue was deeper.

**What happened**:
1. Rotated the API key in the OpenWeatherMap dashboard
2. Updated the `.env` file locally
3. Redeployed the Docker container
4. Still getting 401 errors

**Root cause**: The `.env` file was copied into the Docker image during build (`COPY .env .`). The redeployment used a cached Docker layer — the old `.env` was still baked into the image. The new key in the local `.env` was never picked up.

**Debugging steps that would have caught it faster**:
```bash
# 1. Check what the app actually sees (not what the file says)
docker exec <container> env | grep API_KEY

# 2. Compare with expected value
echo $EXPECTED_KEY

# 3. Check if Docker used a cached layer
docker history <image> | head -20
```

## Rules

### 1. Verify the actual value reaching the API

Never assume the value in your config file is what the application uses. Always check the runtime value:

```python
# Add a startup log (redacted) to verify
logger.info(f"API key loaded: {api_key[:4]}...{api_key[-4:]}")
```

For [[fastapi]] apps, add a debug endpoint (protected, non-production):
```python
@app.get("/debug/config")
async def debug_config(settings: Settings = Depends(get_settings)):
    return {
        "api_key_prefix": settings.api_key[:4] + "...",
        "provider_url": settings.provider_url,
    }
```

### 2. Check Docker layer caching when env vars change

Docker caches layers aggressively. If your `Dockerfile` has:
```dockerfile
COPY .env .          # This layer is cached!
COPY . .             # This layer changes, but .env is already baked in
```

**Fix**: Never bake `.env` into images. Use runtime injection:
```yaml
# docker-compose.yml
services:
  app:
    env_file: .env       # Injected at runtime, not build time
```

Or for Azure Container Apps / Kubernetes: use secrets and configmaps.

### 3. Use a health endpoint that validates auth before deploying

Add a health check that actually tests the API key, not just returns 200:

```python
@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    try:
        # Actually call the provider with a minimal request
        await weather_provider.ping(api_key=settings.api_key)
        return {"status": "healthy", "provider": "connected"}
    except AuthenticationError:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "reason": "provider auth failed"},
        )
```

This pattern was also useful in [[recipe-chatbot]] for validating the Azure OpenAI API key on startup. A misconfigured key is caught immediately instead of failing on the first user request.

## Key Takeaway

Auth failures are almost never about the key itself — they're about the delivery mechanism. Treat the path from config file → environment → runtime as a chain, and verify each link.

## Related

- [[weather-api]] — origin of this lesson (API key rotation incident)
- [[recipe-chatbot]] — applied health-check validation for Azure OpenAI
- [[fastapi]] — framework-specific auth patterns
- [[retry-with-backoff]] — complementary pattern (don't retry auth failures)

<!-- DEMO DATA: This content is fictional, created to demonstrate the wiki structure. -->
