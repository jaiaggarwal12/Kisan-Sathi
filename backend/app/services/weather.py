"""Weather service backed by OpenWeather, plus simple farmer-facing advisories."""
from __future__ import annotations

import requests

from ..config import settings


class WeatherError(Exception):
    """Raised when weather data cannot be fetched."""


def _build_advisory(description: str, temp: float, humidity: int, wind: float) -> str:
    """Turn raw weather into a short, actionable nudge for the farmer."""
    desc = description.lower()
    if any(word in desc for word in ("rain", "drizzle", "thunder", "storm")):
        return "Rain expected soon - avoid spraying pesticide or irrigating today."
    if temp >= 38:
        return "High heat - irrigate in the early morning or evening, not at noon."
    if humidity >= 85:
        return "Very humid - watch for fungal disease; ensure good field drainage."
    if wind >= 10:
        return "Strong winds - postpone any spraying to avoid drift."
    return "Weather looks stable - a good day for routine field work."


def get_weather(lat: float, lon: float) -> dict:
    if not settings.OPENWEATHER_KEY:
        raise WeatherError("OPENWEATHER_KEY is not configured in .env")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_KEY,
        "units": "metric",
    }
    try:
        res = requests.get(settings.OPENWEATHER_URL, params=params, timeout=10)
        data = res.json()
    except requests.RequestException as exc:
        raise WeatherError(f"Could not reach weather service: {exc}") from exc

    if "main" not in data or "weather" not in data:
        raise WeatherError(data.get("message", "Weather data unavailable"))

    temp = float(data["main"]["temp"])
    humidity = int(data["main"]["humidity"])
    pressure = int(data["main"].get("pressure", 0))
    wind = float(data.get("wind", {}).get("speed", 0.0))
    description = data["weather"][0]["description"]

    return {
        "location": data.get("name", "Unknown"),
        "temperature": temp,
        "humidity": humidity,
        "pressure": pressure,
        "description": description,
        "wind_speed": wind,
        "advisory": _build_advisory(description, temp, humidity, wind),
    }
