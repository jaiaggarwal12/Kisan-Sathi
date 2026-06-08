"""
NDVI / satellite crop-health service backed by AgroMonitoring.

Workflow reminder:
  1. A farm polygon is created on AgroMonitoring -> returns a `field_id`.
  2. NDVI history for that field_id gives vegetation index + satellite images.
This module wraps both the polygon listing and the NDVI history lookup.
"""
from __future__ import annotations

import time

import requests

from ..config import settings


class NdviError(Exception):
    """Raised when NDVI data cannot be fetched."""


def _health_label(ndvi: float | None) -> str:
    if ndvi is None:
        return "unknown"
    if ndvi < 0.2:
        return "bare soil / very poor vegetation"
    if ndvi < 0.4:
        return "sparse or stressed crop"
    if ndvi < 0.6:
        return "moderate, developing crop"
    return "healthy, dense crop"


def list_fields() -> list[dict]:
    """List all polygons (fields) registered on the AgroMonitoring account."""
    if not settings.AGRO_API_KEY:
        raise NdviError("AGRO_API_KEY is not configured in .env")
    url = f"{settings.AGRO_BASE_URL}/polygons"
    try:
        res = requests.get(url, params={"appid": settings.AGRO_API_KEY}, timeout=15)
        data = res.json()
    except requests.RequestException as exc:
        raise NdviError(f"Could not reach AgroMonitoring: {exc}") from exc
    if isinstance(data, dict) and data.get("cod"):
        raise NdviError(data.get("message", "AgroMonitoring error"))
    return data


def create_field(name: str, coordinates: list[list[list[float]]]) -> dict:
    """
    Create a polygon (field) on AgroMonitoring and return its details.

    `coordinates` is a GeoJSON polygon ring list, e.g.
    [[[lon, lat], [lon, lat], ..., [lon, lat]]]  (first == last point).
    """
    if not settings.AGRO_API_KEY:
        raise NdviError("AGRO_API_KEY is not configured in .env")
    url = f"{settings.AGRO_BASE_URL}/polygons"
    payload = {
        "name": name,
        "geo_json": {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": coordinates},
        },
    }
    try:
        res = requests.post(
            url, params={"appid": settings.AGRO_API_KEY}, json=payload, timeout=15
        )
        data = res.json()
    except requests.RequestException as exc:
        raise NdviError(f"Could not reach AgroMonitoring: {exc}") from exc
    if isinstance(data, dict) and data.get("cod"):
        raise NdviError(data.get("message", "AgroMonitoring error"))
    return data


def square_polygon(lat: float, lon: float, half_size_deg: float = 0.0015) -> list:
    """
    Build a small square polygon around a point so a farmer who only taps a
    location still gets a valid field. ~0.0015 deg ≈ 150-170 m per side.
    """
    return [
        [
            [lon - half_size_deg, lat - half_size_deg],
            [lon + half_size_deg, lat - half_size_deg],
            [lon + half_size_deg, lat + half_size_deg],
            [lon - half_size_deg, lat + half_size_deg],
            [lon - half_size_deg, lat - half_size_deg],
        ]
    ]


def get_ndvi(field_id: str, days: int = 60) -> dict:
    """Fetch the most recent NDVI reading for a field over the last `days`."""
    if not settings.AGRO_API_KEY:
        raise NdviError("AGRO_API_KEY is not configured in .env")

    end = int(time.time())
    start = end - days * 24 * 3600
    url = f"{settings.AGRO_BASE_URL}/ndvi/history"
    params = {
        "polyid": field_id,
        "start": start,
        "end": end,
        "appid": settings.AGRO_API_KEY,
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        data = res.json()
    except requests.RequestException as exc:
        raise NdviError(f"Could not reach AgroMonitoring: {exc}") from exc

    if isinstance(data, dict):
        # AgroMonitoring returns {"cod": 401, ...} or {"error": "-1"} on issues.
        raise NdviError(
            data.get("message")
            or "No NDVI data for this field yet (satellite pass pending)."
        )
    if not data:
        raise NdviError("No NDVI data available for this field in the time window.")

    latest = data[-1]
    ndvi_mean = latest.get("data", {}).get("mean")
    return {
        "field_id": field_id,
        "date": latest.get("dt"),
        "ndvi_mean": ndvi_mean,
        "health": _health_label(ndvi_mean),
        "image_url": latest.get("image", {}).get("ndvi"),
    }
