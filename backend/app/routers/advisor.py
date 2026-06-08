"""AI advisor chatbot, crop calendar and crop recommendation endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import SoilRecord
from ..services import chatbot
from ..services import crop_calendar
from ..services import crop_recommend
from ..services.crop_knowledge import crop_list

router = APIRouter(prefix="/advisor", tags=["AI Advisor"])


@router.post("/chat")
def chat(phone: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)):
    """Context-aware advisor reply using the farmer's real soil/farm/weather."""
    return chatbot.answer(db, phone, message)


@router.get("/crops")
def crops():
    return {"crops": crop_list()}


@router.get("/calendar/{crop}")
def calendar(crop: str, sowing_date: str | None = None):
    try:
        return crop_calendar.build_calendar(crop, sowing_date)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/recommend/{phone}")
def recommend_for_farmer(phone: str, season: str | None = None, db: Session = Depends(get_db)):
    soil = (
        db.query(SoilRecord)
        .filter(SoilRecord.farmer_phone == phone)
        .order_by(SoilRecord.created_at.desc())
        .first()
    )
    if soil is None:
        raise HTTPException(status_code=404, detail="No soil test found for this farmer")
    return crop_recommend.recommend(soil.n, soil.p, soil.k, soil.ph, season)
