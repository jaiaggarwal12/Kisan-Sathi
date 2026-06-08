"""Weather endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import WeatherOut
from ..services import weather as weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/{lat}/{lon}", response_model=WeatherOut)
def get_weather(lat: float, lon: float):
    try:
        return weather_service.get_weather(lat, lon)
    except weather_service.WeatherError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
