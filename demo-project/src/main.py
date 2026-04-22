"""Weather API — FastAPI service with mock providers and retry logic."""

import asyncio
import random
from datetime import datetime

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Weather API", version="0.1.0")

PROVIDERS = ["OpenWeatherMap", "WeatherAPI"]


async def fetch_with_backoff(provider: str, city: str, max_retries: int = 3) -> dict:
    """Fetch weather data from a provider with exponential backoff."""
    for attempt in range(max_retries):
        try:
            # Simulate API call — replace with real HTTP client in production
            await asyncio.sleep(0.05)
            if random.random() < 0.1:
                raise ConnectionError(f"{provider} temporarily unavailable")
            return {
                "provider": provider,
                "city": city,
                "temp_c": round(random.uniform(-10, 40), 1),
                "humidity": random.randint(20, 95),
                "condition": random.choice(["sunny", "cloudy", "rainy", "snowy"]),
            }
        except ConnectionError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(0.1 * (2 ** attempt))
    raise ConnectionError(f"All retries exhausted for {provider}")


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/weather/{city}")
async def get_weather(city: str):
    """Try each provider with failover until one succeeds."""
    for provider in PROVIDERS:
        try:
            data = await fetch_with_backoff(provider, city)
            return data
        except ConnectionError:
            continue
    raise HTTPException(status_code=503, detail="All weather providers unavailable")
