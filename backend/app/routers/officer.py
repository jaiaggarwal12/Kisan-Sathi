"""Officer dashboard endpoints: aggregate stats and farm geodata."""
from __future__ import annotations

from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farm, Farmer, PestReport, SosAlert

router = APIRouter(prefix="/officer", tags=["Officer Dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    """Headline counters + pest breakdown for the dashboard cards/charts."""
    pests = db.query(PestReport).all()
    pest_counts = Counter(p.pest for p in pests)
    return {
        "farmers": db.query(Farmer).count(),
        "farms": db.query(Farm).count(),
        "pest_reports": len(pests),
        "open_sos": db.query(SosAlert).filter(SosAlert.status == "open").count(),
        "pest_breakdown": [
            {"pest": k, "count": v} for k, v in pest_counts.most_common()
        ],
    }


@router.get("/farms")
def all_farms(db: Session = Depends(get_db)):
    """Every mapped farm with its owner -- used to plot markers on the map."""
    rows = db.query(Farm, Farmer).join(Farmer, Farm.farmer_phone == Farmer.phone).all()
    return [
        {
            "phone": farm.farmer_phone,
            "name": farmer.name,
            "village": farmer.village,
            "district": farmer.district,
            "lat": farm.lat,
            "lon": farm.lon,
            "area": farm.area,
        }
        for farm, farmer in rows
    ]
