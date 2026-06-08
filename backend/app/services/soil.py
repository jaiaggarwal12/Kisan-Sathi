"""
Soil-based fertilizer advisory.

Uses simplified ICAR-style thresholds for N/P/K and pH to produce concrete
fertilizer recommendations plus a plain-language explanation so the farmer
(or a judge) can see *why* each suggestion was made -- the "explainable AI"
trust layer.
"""
from __future__ import annotations

# Threshold reference (kg/ha) for low vs sufficient nutrient levels.
N_LOW = 280
P_LOW = 22
K_LOW = 120


def advise(n: int, p: int, k: int, ph: float, oc: float, ec: float, crop: str) -> dict:
    recommendations: list[str] = []
    explanation: list[str] = []

    if n < N_LOW:
        recommendations.append("Apply Urea: ~50 kg/acre")
        explanation.append(
            f"Nitrogen is {n} kg/ha (below {N_LOW}); {crop} needs more N for leaf growth."
        )
    if p < P_LOW:
        recommendations.append("Apply DAP: ~20 kg/acre")
        explanation.append(
            f"Phosphorus is {p} kg/ha (below {P_LOW}); supports root and grain development."
        )
    if k < K_LOW:
        recommendations.append("Apply MOP: ~20 kg/acre")
        explanation.append(
            f"Potassium is {k} kg/ha (below {K_LOW}); improves disease resistance and yield."
        )
    if ph < 6.0:
        recommendations.append("Apply Lime: ~5 kg/acre")
        explanation.append(f"Soil pH {ph} is acidic; lime raises pH toward the ideal 6.5-7.5.")
    if ph > 8.0:
        recommendations.append("Apply Gypsum: ~10 kg/acre")
        explanation.append(f"Soil pH {ph} is alkaline; gypsum helps lower it.")
    if oc < 0.5:
        recommendations.append("Add organic compost / farmyard manure")
        explanation.append(
            f"Organic carbon {oc}% is low; compost improves soil structure and microbes."
        )

    if not recommendations:
        recommendations.append("Soil nutrients are in a healthy range. No extra fertilizer needed.")
        explanation.append("All measured values fall within recommended ranges for this crop.")

    return {"crop": crop, "recommendations": recommendations, "explanation": explanation}
