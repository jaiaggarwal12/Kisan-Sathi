"""Farmer registration and profile endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farmer
from ..schemas import FarmerOut

router = APIRouter(prefix="/farmers", tags=["Farmers"])


@router.post("/register", response_model=FarmerOut)
def register_farmer(
    phone: str = Form(...),
    name: str = Form(...),
    village: str = Form(""),
    district: str = Form(""),
    state: str = Form(""),
    language: str = Form("hi"),
    db: Session = Depends(get_db),
):
    """Create or update a farmer profile (keyed by phone number)."""
    farmer = db.get(Farmer, phone)
    if farmer is None:
        farmer = Farmer(phone=phone)
        db.add(farmer)
    farmer.name = name
    farmer.village = village or None
    farmer.district = district or None
    farmer.state = state or None
    farmer.language = language or "hi"
    db.commit()
    db.refresh(farmer)
    return farmer


@router.get("/{phone}", response_model=FarmerOut)
def get_farmer(phone: str, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, phone)
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer


@router.get("", response_model=list[FarmerOut])
def list_farmers(db: Session = Depends(get_db)):
    """List all farmers (used by the officer dashboard)."""
    return db.query(Farmer).all()
