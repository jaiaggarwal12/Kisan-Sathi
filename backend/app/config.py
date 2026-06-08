"""
Central configuration.

All secrets and tunables are read from the .env file so they never live in
source code. Import `settings` anywhere you need a key or option.
"""
from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

# Load variables from backend/.env into the process environment.
load_dotenv()


class Settings:
    """Strongly-typed view over environment variables."""

    # --- External API keys ---
    OPENWEATHER_KEY: str = os.getenv("OPENWEATHER_KEY", "")
    AGRO_API_KEY: str = os.getenv("AGRO_API_KEY", "")
    DATA_GOV_API_KEY: str = os.getenv("DATA_GOV_API_KEY", "")
    DATA_GOV_RESOURCE_ID: str = os.getenv(
        "DATA_GOV_RESOURCE_ID", "9ef84268-d588-465a-a308-a864a43d0070"
    )

    # Default demo field (AgroMonitoring polygon id) used when a farm has none.
    DEFAULT_FIELD_ID: str = os.getenv("DEFAULT_FIELD_ID", "")

    # Hugging Face repo for the pre-trained pest/disease model (PlantVillage).
    PEST_MODEL_HF_REPO: str = os.getenv(
        "PEST_MODEL_HF_REPO",
        "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
    )

    # --- Infrastructure ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kisan_sathi.db")
    CORS_ORIGINS: list[str] = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()
    ]

    # --- External endpoints (kept here so URLs aren't scattered around) ---
    OPENWEATHER_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    AGRO_BASE_URL: str = "https://api.agromonitoring.com/agro/1.0"
    DATA_GOV_URL: str = "https://api.data.gov.in/resource"

    def missing_keys(self) -> list[str]:
        """Return the names of keys that are still unset (for a health check)."""
        checks = {
            "OPENWEATHER_KEY": self.OPENWEATHER_KEY,
            "AGRO_API_KEY": self.AGRO_API_KEY,
            "DATA_GOV_API_KEY": self.DATA_GOV_API_KEY,
        }
        return [name for name, value in checks.items() if not value]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
