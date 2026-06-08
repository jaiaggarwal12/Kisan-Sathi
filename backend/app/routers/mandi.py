"""Mandi (market) price endpoints with cascading dropdown helpers."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..services import mandi as mandi_service
from ..services import market_intel

router = APIRouter(prefix="/mandi", tags=["Mandi Prices"])


def _guard(func, *args):
    try:
        return func(*args)
    except mandi_service.MandiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/commodities")
def commodities():
    return {"commodities": _guard(mandi_service.list_commodities)}


@router.get("/states/{commodity}")
def states(commodity: str):
    return {"commodity": commodity, "states": _guard(mandi_service.list_states, commodity)}


@router.get("/districts/{commodity}/{state}")
def districts(commodity: str, state: str):
    return {
        "commodity": commodity,
        "state": state,
        "districts": _guard(mandi_service.list_districts, commodity, state),
    }


@router.get("/markets/{commodity}/{state}/{district}")
def markets(commodity: str, state: str, district: str):
    return {
        "commodity": commodity,
        "state": state,
        "district": district,
        "markets": _guard(mandi_service.list_markets, commodity, state, district),
    }


@router.get("/prices/{commodity}")
def prices(commodity: str, state: str | None = None,
           district: str | None = None, market: str | None = None):
    rows = _guard(mandi_service.get_prices, commodity, state, district, market)
    return {"commodity": commodity, "count": len(rows), "markets": rows}


@router.get("/best/{commodity}")
def best_market(commodity: str, state: str | None = None):
    """Find the highest-paying mandi for a commodity and the extra income."""
    try:
        return market_intel.best_mandi(commodity, state)
    except mandi_service.MandiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/profit/{crop}")
def profit(crop: str, area: float, state: str | None = None):
    """Estimate revenue/cost/profit for a crop over the given area (acres)."""
    try:
        return market_intel.profit_estimate(crop, area, state)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
