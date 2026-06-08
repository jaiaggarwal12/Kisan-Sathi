"""
Map a plant-disease label (PlantVillage style) to a practical remedy.

Labels look like "Tomato with Late Blight", "Apple Scab", "Healthy Apple",
"Cherry with Powdery Mildew". We match on disease keywords so the same logic
works across crops.
"""
from __future__ import annotations

# (keyword, remedy) -- checked in order; first match wins.
_RULES: list[tuple[str, str]] = [
    ("healthy", "Plant looks healthy. Keep monitoring weekly and maintain balanced nutrition."),
    ("late blight", "Remove and destroy infected parts; spray a copper-based or metalaxyl fungicide; improve drainage."),
    ("early blight", "Remove lower infected leaves; spray mancozeb or chlorothalonil; rotate crops next season."),
    ("leaf blight", "Spray a recommended fungicide (mancozeb); avoid overhead irrigation; remove debris."),
    ("blight", "Apply an appropriate fungicide promptly and remove affected foliage."),
    ("scab", "Apply captan or mancozeb at early leaf stage; prune for airflow; clear fallen leaves."),
    ("rust", "Spray a recommended fungicide (propiconazole); remove alternate host plants nearby."),
    ("powdery mildew", "Spray sulphur or potassium bicarbonate; improve airflow; avoid excess nitrogen."),
    ("black rot", "Prune and destroy infected wood/fruit; apply fungicide; sanitise the field."),
    ("bacterial spot", "Use copper-based bactericide; avoid working with wet plants; use clean seed."),
    ("leaf spot", "Remove affected leaves; apply copper or mancozeb; avoid overhead watering."),
    ("leaf mold", "Increase ventilation; reduce humidity; apply a recommended fungicide."),
    ("mosaic virus", "Remove infected plants; control aphid vectors; use virus-free seed."),
    ("leaf curl", "Remove infected plants; control the whitefly vector with neem/insecticide."),
    ("yellow leaf curl", "Remove infected plants; manage whitefly with sticky traps and neem."),
    ("spider mite", "Spray water to dislodge; use a miticide or neem oil; avoid dusty conditions."),
    ("measles", "Prune affected wood; manage canopy; apply fungicide as advised."),
    ("greening", "No cure; remove infected trees; control the psyllid vector to stop spread."),
    ("citrus greening", "No cure; remove infected trees; control psyllid vector."),
    ("esca", "Prune out diseased wood; protect pruning wounds; avoid water stress."),
]

_FALLBACK = "Consult your local agriculture officer for crop-specific treatment."


def remedy_for(label: str) -> str:
    low = label.lower()
    for keyword, advice in _RULES:
        if keyword in low:
            return advice
    return _FALLBACK
