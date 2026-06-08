"""
Farm mapping endpoints.

When a farm is registered we automatically create an AgroMonitoring polygon
around its location and store the returned field_id, so NDVI works later
without any manual Postman steps.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Farm, Farmer
from ..schemas import FarmOut
from ..services import ndvi as ndvi_service

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("/register", response_model=FarmOut)
def register_farm(
    phone: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    area: float = Form(...),
    db: Session = Depends(get_db),
):
    if db.get(Farmer, phone) is None:
        raise HTTPException(status_code=404, detail="Register the farmer first")

    field_id: str | None = None
    # Best-effort polygon creation; never block farm registration if Agro fails.
    try:
        poly = ndvi_service.create_field(
            name=f"farm_{phone}",
            coordinates=ndvi_service.square_polygon(lat, lon),
        )
        field_id = poly.get("id")
    except ndvi_service.NdviError:
        field_id = settings.DEFAULT_FIELD_ID or None

    farm = Farm(farmer_phone=phone, lat=lat, lon=lon, area=area, field_id=field_id)
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm


@router.get("/{phone}", response_model=list[FarmOut])
def get_farms(phone: str, db: Session = Depends(get_db)):
    farms = db.query(Farm).filter(Farm.farmer_phone == phone).all()
    if not farms:
        raise HTTPException(status_code=404, detail="No farm registered for this farmer")
    return farms
