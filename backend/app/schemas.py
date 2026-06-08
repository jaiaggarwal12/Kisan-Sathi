"""Pydantic schemas: validate inputs and shape JSON responses."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------- Farmer ----------
class FarmerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone: str
    name: str
    village: str | None = None
    district: str | None = None
    state: str | None = None
    language: str = "hi"
    created_at: datetime


# ---------- Farm ----------
class FarmOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farmer_phone: str
    lat: float
    lon: float
    area: float
    field_id: str | None = None
    created_at: datetime


# ---------- Soil ----------
class SoilOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farmer_phone: str
    n: int
    p: int
    k: int
    ph: float
    oc: float
    ec: float
    created_at: datetime


class FertilizerAdvisory(BaseModel):
    farmer_phone: str
    crop: str
    recommendations: list[str]
    explanation: list[str]


# ---------- Weather ----------
class WeatherOut(BaseModel):
    location: str
    temperature: float
    humidity: int
    pressure: int
    description: str
    wind_speed: float
    advisory: str


# ---------- NDVI ----------
class NdviOut(BaseModel):
    field_id: str
    date: int | None = None
    ndvi_mean: float | None = None
    health: str
    image_url: str | None = None


# ---------- Pest ----------
class PestReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farmer_phone: str
    lat: float
    lon: float
    pest: str
    confidence: float
    created_at: datetime


# ---------- SOS ----------
class SosOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farmer_phone: str
    issue: str
    lat: float | None = None
    lon: float | None = None
    status: str
    created_at: datetime


# ---------- Generic ----------
class Message(BaseModel):
    status: str = "ok"
    detail: str = ""
