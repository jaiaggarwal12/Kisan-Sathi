# Kisan Sathi — Smart Crop Advisory System (SIH 2025)

A farmer-first, multilingual crop advisory platform: live weather, satellite
crop health (NDVI), soil-based fertilizer advice, AI pest detection, real mandi
prices, government schemes, and SOS alerts.

```
kisan-sathi/
├─ backend/        FastAPI + SQLite, all APIs and ML inference
├─ farmer-app/     React + Vite mobile-style web app (DigiLocker look)
└─ ai/             Pest-detection model training (EfficientNet-B3)
```

## Run the backend
```bat
cd "e:\kisan sathi\backend"
.venv\Scripts\activate
uvicorn app.main:app --reload
```
- API docs: http://127.0.0.1:8000/docs
- Health:   http://127.0.0.1:8000/health

## Run the farmer app (in a second terminal)
```bat
cd "e:\kisan sathi\farmer-app"
npm run dev
```
- Open http://localhost:5173
- Login with any 10-digit number, OTP = **1234**

The app proxies `/api` to the backend automatically, so start the backend first.

## Train the pest model (optional, free GPU)
See `ai/README.md`. Drop the result at `backend/models/pest_model_india.pt`
and the backend uses it automatically.

## Status of each feature
| Feature | State |
|---------|-------|
| Farmer login / profile | ✅ working, stored in DB |
| Weather + advisory | ✅ live (OpenWeather) |
| Soil fertilizer advisory + "why?" | ✅ working |
| Mandi prices (cascading filters) | ✅ working (depends on data.gov.in uptime) |
| Pest detection + remedy | ✅ working (stub until model trained) |
| Pest outbreak map | ✅ working (Leaflet) |
| Government schemes | ✅ working |
| Farm mapping + NDVI | ✅ working (needs satellite pass for NDVI) |
| SOS alerts | ✅ working |
| Multilingual (EN/HI/PA) | ✅ working |
| Officer portal | ⏳ next |
