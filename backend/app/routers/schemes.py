"""Government scheme recommendation endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farm, Farmer
from ..services import schemes as scheme_service

router = APIRouter(prefix="/schemes", tags=["Government Schemes"])


@router.get("/all")
def all_schemes():
    return {"schemes": scheme_service.match_schemes()}


@router.get("/eligible/{phone}")
def eligible_schemes(phone: str, db: Session = Depends(get_db)):
    """Match schemes using the farmer's state and total registered land."""
    farmer = db.get(Farmer, phone)
    state = farmer.state if farmer else None
    total_area = (
        db.query(Farm).filter(Farm.farmer_phone == phone).all()
    )
    land = sum(f.area for f in total_area) if total_area else None
    return {
        "farmer": phone,
        "land_acres": land,
        "state": state,
        "eligible_schemes": scheme_service.match_schemes(land_size=land, state=state),
    }
