"""
Crop recommendation from soil + season.

Transparent scoring: each crop earns points when the soil pH sits inside its
ideal band and when its nitrogen demand matches the measured N level, with a
bonus for matching the current sowing season. Designed to be explainable, not
a black box.
"""
from __future__ import annotations

from datetime import date

from .crop_knowledge import CROPS

N_LOW = 280  # kg/ha threshold for "low" nitrogen


def current_season() -> str:
    month = date.today().month
    # Kharif sowing ~ Jun-Sep, Rabi sowing ~ Oct-Mar.
    return "kharif" if 6 <= month <= 9 else "rabi"


def recommend(n: int, p: int, k: int, ph: float, season: str | None = None) -> dict:
    season = season or current_season()
    scored = []

    for crop, info in CROPS.items():
        score = 0
        reasons = []

        lo, hi = info["ideal_ph"]
        if lo <= ph <= hi:
            score += 3
            reasons.append(f"pH {ph} suits {crop} (ideal {lo}-{hi}).")
        else:
            reasons.append(f"pH {ph} is outside {crop}'s ideal {lo}-{hi}.")

        if info["season"] == season:
            score += 3
            reasons.append(f"It is {season} season - right time to sow {crop}.")

        if info["n_need"] == "high" and n >= N_LOW:
            score += 2
            reasons.append("Soil nitrogen is adequate for this high-demand crop.")
        elif info["n_need"] != "high":
            score += 1
            reasons.append("Crop has modest nitrogen needs - fits most soils.")

        scored.append({"crop": crop, "score": score, "reasons": reasons})

    scored.sort(key=lambda c: c["score"], reverse=True)
    return {"season": season, "recommendations": scored[:4]}
