# Kisan Sathi — Backend

Smart Crop Advisory System for small & marginal farmers (SIH 2025).
FastAPI backend with a real database, live weather/NDVI/mandi integrations,
soil advisory, AI pest detection, government schemes, and SOS alerts.

## Project layout

```
backend/
├─ app/
│  ├─ main.py            # FastAPI app + router wiring
│  ├─ config.py          # reads keys/options from .env
│  ├─ database.py        # SQLAlchemy engine + session
│  ├─ models.py          # database tables (Farmer, Farm, Soil, Pest, SOS)
│  ├─ schemas.py         # request/response shapes
│  ├─ ml/
│  │  └─ pest_model.py   # pest detection (graceful fallback w/o torch)
│  ├─ services/          # external APIs + business logic
│  │  ├─ weather.py  ndvi.py  mandi.py  soil.py  schemes.py
│  └─ routers/           # one file per feature
│     ├─ farmers.py  farms.py  soil.py  weather.py  ndvi.py
│     ├─ mandi.py  pest.py  schemes.py  sos.py
├─ data/schemes.json     # government schemes
├─ requirements.txt
├─ .env                  # your real keys (NOT committed)
└─ .env.example          # template
```

## Run it (Windows)

```bat
cd "e:\kisan sathi\backend"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the interactive API docs: http://127.0.0.1:8000/docs
Health check (shows missing keys): http://127.0.0.1:8000/health

## Optional: real pest AI

The server runs without PyTorch (pest detection uses a safe stub). For real
inference:

```bat
pip install torch torchvision
```

Then replace the labels/weights in `app/ml/pest_model.py` with your
PlantVillage-trained model.

## Key endpoints

| Area      | Method & path |
|-----------|---------------|
| Farmer    | `POST /farmers/register`, `GET /farmers/{phone}`, `GET /farmers` |
| Farm      | `POST /farms/register`, `GET /farms/{phone}` |
| Soil      | `POST /soil/register`, `GET /soil/advisory/{phone}?crop=Wheat` |
| Weather   | `GET /weather/{lat}/{lon}` |
| NDVI      | `GET /ndvi/fields`, `GET /ndvi/field/{field_id}`, `GET /ndvi/farmer/{phone}` |
| Mandi     | `GET /mandi/commodities` → `/states` → `/districts` → `/markets` → `/prices` |
| Pest      | `POST /pest/report` (image), `GET /pest/heatmap` |
| Schemes   | `GET /schemes/all`, `GET /schemes/eligible/{phone}` |
| SOS       | `POST /sos`, `GET /sos`, `PATCH /sos/{id}/resolve` |
```
