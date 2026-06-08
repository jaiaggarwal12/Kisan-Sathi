"""NDVI / satellite crop-health endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Farm
from ..schemas import NdviOut
from ..services import ndvi as ndvi_service

router = APIRouter(prefix="/ndvi", tags=["NDVI / Satellite"])


@router.get("/fields")
def list_fields():
    """List all AgroMonitoring polygons on the account."""
    try:
        return ndvi_service.list_fields()
    except ndvi_service.NdviError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/field/{field_id}", response_model=NdviOut)
def ndvi_by_field(field_id: str):
    """NDVI for a specific AgroMonitoring polygon id."""
    try:
        return ndvi_service.get_ndvi(field_id)
    except ndvi_service.NdviError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/farmer/{phone}", response_model=NdviOut)
def ndvi_by_farmer(phone: str, db: Session = Depends(get_db)):
    """NDVI for a farmer's first registered farm (uses its stored field_id)."""
    farm = db.query(Farm).filter(Farm.farmer_phone == phone).first()
    field_id = (farm.field_id if farm else None) or settings.DEFAULT_FIELD_ID
    if not field_id:
        raise HTTPException(status_code=404, detail="No field_id available for this farmer")
    try:
        return ndvi_service.get_ndvi(field_id)
    except ndvi_service.NdviError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
