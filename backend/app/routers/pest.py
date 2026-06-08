"""Pest detection (image upload) and community outbreak heatmap endpoints."""
from __future__ import annotations

import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..ml.pest_model import predict_pest
from ..models import Farm, PestReport
from ..schemas import PestReportOut
from ..services import proximity

router = APIRouter(prefix="/pest", tags=["Pest Detection"])

UPLOAD_DIR = "uploads"


@router.post("/report")
def report_pest(
    phone: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a pest photo -> AI detects the pest -> stored for the heatmap."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}.jpg")
    try:
        with open(path, "wb") as fh:
            fh.write(file.file.read())
        result = predict_pest(path)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Detection failed: {exc}") from exc
    finally:
        if os.path.exists(path):
            os.remove(path)

    report = PestReport(
        farmer_phone=phone,
        lat=lat,
        lon=lon,
        pest=result["pest"],
        confidence=result["confidence"],
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "status": "success",
        "report": PestReportOut.model_validate(report),
        "remedy": result["remedy"],
        "model": result["model"],
    }


@router.get("/heatmap", response_model=list[PestReportOut])
def heatmap(limit: int = 50, db: Session = Depends(get_db)):
    """Recent pest reports (lat/lon + pest) for the community outbreak map."""
    return (
        db.query(PestReport)
        .order_by(PestReport.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/nearby")
def nearby(
    lat: float,
    lon: float,
    radius_km: float = 5.0,
    db: Session = Depends(get_db),
):
    """Pest outbreaks reported near a coordinate (community early warning)."""
    return proximity.nearby_outbreaks(db, lat, lon, radius_km)


@router.get("/nearby/farmer/{phone}")
def nearby_for_farmer(phone: str, radius_km: float = 5.0, db: Session = Depends(get_db)):
    """Outbreaks near a farmer's mapped farm, excluding their own reports."""
    farm = db.query(Farm).filter(Farm.farmer_phone == phone).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Map your farm to get nearby alerts")
    return proximity.nearby_outbreaks(
        db, farm.lat, farm.lon, radius_km, exclude_phone=phone
    )
