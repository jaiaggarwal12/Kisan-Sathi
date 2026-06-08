"""SOS emergency alert endpoints (farmer raises, officer resolves)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import SosAlert
from ..schemas import SosOut

router = APIRouter(prefix="/sos", tags=["SOS Alerts"])


@router.post("", response_model=SosOut)
def raise_sos(
    phone: str = Form(...),
    issue: str = Form(...),
    lat: float | None = Form(None),
    lon: float | None = Form(None),
    db: Session = Depends(get_db),
):
    alert = SosAlert(farmer_phone=phone, issue=issue, lat=lat, lon=lon)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.get("", response_model=list[SosOut])
def list_sos(status: str | None = None, db: Session = Depends(get_db)):
    """List SOS alerts for the officer dashboard, optionally filtered by status."""
    query = db.query(SosAlert).order_by(SosAlert.created_at.desc())
    if status:
        query = query.filter(SosAlert.status == status)
    return query.all()


@router.patch("/{alert_id}/resolve", response_model=SosOut)
def resolve_sos(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(SosAlert, alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="SOS alert not found")
    alert.status = "resolved"
    db.commit()
    db.refresh(alert)
    return alert
