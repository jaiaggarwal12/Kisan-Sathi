"""
Community proximity: find pest outbreaks reported near a location.

Powers the "3 farmers within 5 km reported Whitefly" early-warning feature.
Uses the haversine formula (great-circle distance) -- no external service.
"""
from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ..models import PestReport


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0  # Earth radius in km
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def nearby_outbreaks(
    db: Session,
    lat: float,
    lon: float,
    radius_km: float = 5.0,
    days: int = 30,
    exclude_phone: str | None = None,
) -> dict:
    """Group recent nearby pest reports by pest type, closest first."""
    since = datetime.utcnow() - timedelta(days=days)
    reports = (
        db.query(PestReport)
        .filter(PestReport.created_at >= since)
        .filter(PestReport.pest != "Healthy")
        .all()
    )

    grouped: dict[str, list[dict]] = defaultdict(list)
    for rep in reports:
        if exclude_phone and rep.farmer_phone == exclude_phone:
            continue
        dist = haversine_km(lat, lon, rep.lat, rep.lon)
        if dist <= radius_km:
            grouped[rep.pest].append(
                {
                    "distance_km": round(dist, 2),
                    "confidence": rep.confidence,
                    "when": rep.created_at.isoformat(),
                }
            )

    clusters = []
    for pest, items in grouped.items():
        items.sort(key=lambda x: x["distance_km"])
        clusters.append(
            {
                "pest": pest,
                "count": len(items),
                "nearest_km": items[0]["distance_km"],
                "alert": (
                    f"{len(items)} farmer(s) within {radius_km:.0f} km reported "
                    f"{pest} (nearest {items[0]['distance_km']} km). Scout your crop early."
                ),
            }
        )

    clusters.sort(key=lambda c: (-c["count"], c["nearest_km"]))
    return {
        "center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "total_nearby_reports": sum(c["count"] for c in clusters),
        "clusters": clusters,
    }
