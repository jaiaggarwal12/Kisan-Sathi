"""
Context-aware farm advisor.

This is an *explainable*, rule-based assistant (no external LLM key needed).
It pulls the farmer's real data -- latest soil test, mapped farm location,
and live weather -- then answers common questions, always stating the reasoning
so the farmer can trust it. Keyword matching covers English, Hindi and Punjabi
transliterations of frequent terms.

Swap in an LLM later by replacing `answer()` -- the context-gathering stays.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from ..models import Farm, Farmer, SoilRecord
from . import soil as soil_service
from . import weather as weather_service
from .crop_recommend import recommend

# intent -> keywords (lowercased substrings) in en/hi/pa transliteration.
_INTENTS = {
    "fertilizer": ["fertilizer", "urea", "khaad", "khad", "nutrient", "dap", "खाद", "ਖਾਦ"],
    "irrigation": ["irrigat", "water", "pani", "paani", "sinchai", "पानी", "ਪਾਣੀ"],
    "weather": ["weather", "rain", "mausam", "barish", "temperature", "मौसम", "ਮੌਸਮ"],
    "pest": ["pest", "insect", "disease", "keeda", "keet", "bimari", "कीट", "ਕੀਟ"],
    "price": ["price", "mandi", "rate", "sell", "bhaav", "mulya", "भाव", "ਭਾਅ"],
    "crop": ["which crop", "what to grow", "kaun si fasal", "crop recommend", "फसल", "ਫਸਲ"],
    "scheme": ["scheme", "subsidy", "yojana", "loan", "insurance", "योजना", "ਸਕੀਮ"],
}


def _detect_intent(message: str) -> str:
    msg = message.lower()
    for intent, keys in _INTENTS.items():
        if any(k in msg for k in keys):
            return intent
    return "general"


def _context(db: Session, phone: str) -> dict:
    farmer = db.get(Farmer, phone)
    soil = (
        db.query(SoilRecord)
        .filter(SoilRecord.farmer_phone == phone)
        .order_by(SoilRecord.created_at.desc())
        .first()
    )
    farm = db.query(Farm).filter(Farm.farmer_phone == phone).first()
    return {"farmer": farmer, "soil": soil, "farm": farm}


def answer(db: Session, phone: str, message: str) -> dict:
    intent = _detect_intent(message)
    ctx = _context(db, phone)
    soil = ctx["soil"]
    farm = ctx["farm"]
    reasoning: list[str] = []
    actions: list[str] = []

    if intent == "fertilizer":
        if not soil:
            reply = "Please add your soil test (N, P, K, pH) in the Advisory tab so I can give an exact fertilizer plan."
            actions.append("Open Advisory tab and enter soil values.")
        else:
            adv = soil_service.advise(soil.n, soil.p, soil.k, soil.ph, soil.oc, soil.ec, "your crop")
            reply = "Based on your latest soil test: " + "; ".join(adv["recommendations"])
            reasoning = adv["explanation"]

    elif intent == "irrigation":
        if farm:
            try:
                w = weather_service.get_weather(farm.lat, farm.lon)
                if "rain" in w["description"].lower():
                    reply = "Rain is expected near your farm soon - skip irrigation today to save water."
                else:
                    reply = f"No rain expected (currently {w['description']}, {round(w['temperature'])}C). Irrigate early morning or evening."
                reasoning.append(f"Live weather at your farm: {w['description']}, {round(w['temperature'])}C.")
            except weather_service.WeatherError:
                reply = "Irrigate at the crop's critical stages (tillering, flowering, grain filling) and avoid the hottest part of the day."
        else:
            reply = "Map your farm in the Profile tab so I can use your local weather for irrigation timing."
            actions.append("Map your farm (Profile tab).")

    elif intent == "weather":
        if farm:
            try:
                w = weather_service.get_weather(farm.lat, farm.lon)
                reply = f"At your farm it is {round(w['temperature'])}C, {w['description']}, humidity {w['humidity']}%. {w['advisory']}"
            except weather_service.WeatherError:
                reply = "I couldn't fetch live weather right now. Please try again shortly."
        else:
            reply = "Map your farm in Profile to get hyperlocal weather."

    elif intent == "pest":
        reply = "Open the Pest tab and upload a clear photo of the affected leaf - I'll identify the pest/disease and suggest a remedy. Early detection prevents spread."
        actions.append("Upload a leaf photo in the Pest tab.")

    elif intent == "price":
        reply = "Open the Market tab, pick your crop and district to see live mandi prices, and I'll show which nearby mandi pays the most."
        actions.append("Check the Market tab for live prices.")

    elif intent == "crop":
        if soil:
            rec = recommend(soil.n, soil.p, soil.k, soil.ph)
            top = rec["recommendations"][0]
            reply = f"For this {rec['season']} season and your soil, {top['crop']} is a strong choice."
            reasoning = top["reasons"]
        else:
            reply = "Add your soil test so I can recommend the best crops for your land and season."
            actions.append("Enter soil values in Advisory tab.")

    elif intent == "scheme":
        reply = "Check the Home tab for schemes matched to your land and state - e.g. PMFBY crop insurance, Kisan Credit Card, PM-KISAN income support."

    else:
        reply = (
            "I can help with fertilizer, irrigation, weather, pests, mandi prices, "
            "crop choice and government schemes. Ask me, e.g. 'How much urea for wheat?'"
        )

    return {
        "intent": intent,
        "reply": reply,
        "reasoning": reasoning,
        "actions": actions,
    }
