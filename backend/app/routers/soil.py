"""Soil test storage and fertilizer advisory endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farmer, SoilRecord
from ..schemas import FertilizerAdvisory, SoilOut
from ..services import soil as soil_service

router = APIRouter(prefix="/soil", tags=["Soil"])


@router.post("/register", response_model=SoilOut)
def register_soil(
    phone: str = Form(...),
    N: int = Form(...),
    P: int = Form(...),
    K: int = Form(...),
    pH: float = Form(...),
    OC: float = Form(...),
    EC: float = Form(...),
    db: Session = Depends(get_db),
):
    if db.get(Farmer, phone) is None:
        raise HTTPException(status_code=404, detail="Register the farmer first")
    record = SoilRecord(farmer_phone=phone, n=N, p=P, k=K, ph=pH, oc=OC, ec=EC)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/advisory/{phone}", response_model=FertilizerAdvisory)
def fertilizer_advisory(phone: str, crop: str = "Wheat", db: Session = Depends(get_db)):
    record = (
        db.query(SoilRecord)
        .filter(SoilRecord.farmer_phone == phone)
        .order_by(SoilRecord.created_at.desc())
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="No soil test found for this farmer")

    result = soil_service.advise(
        record.n, record.p, record.k, record.ph, record.oc, record.ec, crop
    )
    return FertilizerAdvisory(
        farmer_phone=phone,
        crop=result["crop"],
        recommendations=result["recommendations"],
        explanation=result["explanation"],
    )
