"""
Market intelligence:
  - best_mandi: among available markets for a commodity, find where the modal
    price is highest and quantify the extra income vs the average.
  - profit_estimate: rough revenue/cost/profit for a crop on a given area using
    the live modal price and typical yield/cost from the knowledge base.
"""
from __future__ import annotations

from . import mandi as mandi_service
from .crop_knowledge import CROPS


def _to_float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def best_mandi(commodity: str, state: str | None = None) -> dict:
    rows = mandi_service.get_prices(commodity, state=state, limit=100)
    priced = [
        {**r, "_modal": _to_float(r.get("modal_price"))}
        for r in rows
        if _to_float(r.get("modal_price"))
    ]
    if not priced:
        return {"commodity": commodity, "best": None, "note": "No priced markets found."}

    best = max(priced, key=lambda r: r["_modal"])
    avg = sum(r["_modal"] for r in priced) / len(priced)
    extra = best["_modal"] - avg

    return {
        "commodity": commodity,
        "markets_compared": len(priced),
        "average_modal_price": round(avg, 2),
        "best": {
            "market": best.get("market"),
            "district": best.get("district"),
            "state": best.get("state"),
            "modal_price": best["_modal"],
        },
        "extra_income_per_quintal": round(extra, 2),
        "advice": (
            f"Sell at {best.get('market')} ({best.get('district')}) for about "
            f"Rs {round(extra)} more per quintal than the average mandi."
        ),
    }


def profit_estimate(crop: str, area_acres: float, state: str | None = None) -> dict:
    info = CROPS.get(crop)
    if not info:
        raise ValueError(f"Unknown crop '{crop}'")

    # Use the best live modal price if available, else fall back gracefully.
    price_per_quintal = None
    try:
        bm = best_mandi(crop, state=state)
        if bm.get("best"):
            price_per_quintal = bm["best"]["modal_price"]
    except mandi_service.MandiError:
        price_per_quintal = None

    yield_q = info["yield_q_per_acre"] * area_acres
    cost = info["cost_per_acre"] * area_acres

    result = {
        "crop": crop,
        "area_acres": area_acres,
        "expected_yield_quintal": round(yield_q, 1),
        "estimated_cost": round(cost),
        "price_source": "live mandi" if price_per_quintal else "unavailable",
        "price_per_quintal": price_per_quintal,
    }
    if price_per_quintal:
        revenue = yield_q * price_per_quintal
        result["estimated_revenue"] = round(revenue)
        result["estimated_profit"] = round(revenue - cost)
    result["disclaimer"] = "Estimates based on typical yields/costs; actuals vary."
    return result
