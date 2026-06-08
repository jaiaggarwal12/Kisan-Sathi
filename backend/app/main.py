"""
Kisan Sathi -- FastAPI application entry point.

Run from the backend/ folder:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import settings
from .database import init_db
from .routers import (
    advisor,
    farmers,
    farms,
    mandi,
    ndvi,
    officer,
    pest,
    schemes,
    soil,
    sos,
    weather,
)

app = FastAPI(
    title="Kisan Sathi - Smart Crop Advisory System",
    description="Farmer-first, multilingual crop advisory backend for SIH 2025.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Kisan Sathi backend is running",
        "version": __version__,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    """Quick health check that also reports any missing API keys."""
    missing = settings.missing_keys()
    return {
        "status": "ok" if not missing else "degraded",
        "missing_keys": missing,
        "database": settings.DATABASE_URL.split("://")[0],
    }


# Register all feature routers.
app.include_router(farmers.router)
app.include_router(farms.router)
app.include_router(soil.router)
app.include_router(weather.router)
app.include_router(ndvi.router)
app.include_router(mandi.router)
app.include_router(pest.router)
app.include_router(schemes.router)
app.include_router(sos.router)
app.include_router(advisor.router)
app.include_router(officer.router)
