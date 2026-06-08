"""
Mandi (market) price service backed by the data.gov.in open dataset.

Provides cascading dropdown helpers (commodity -> state -> district -> market)
so the app only ever offers combinations that actually have data today, plus
the final price lookup.
"""
from __future__ import annotations

import requests

from ..config import settings

# data.gov.in can be slow/intermittent, so allow a generous timeout + one retry.
_TIMEOUT = 30
_RETRIES = 2


class MandiError(Exception):
    """Raised when mandi data cannot be fetched."""


def _fetch(filters: dict | None = None, limit: int = 1000) -> list[dict]:
    if not settings.DATA_GOV_API_KEY:
        raise MandiError("DATA_GOV_API_KEY is not configured in .env")

    url = f"{settings.DATA_GOV_URL}/{settings.DATA_GOV_RESOURCE_ID}"
    params = {
        "api-key": settings.DATA_GOV_API_KEY,
        "format": "json",
        "limit": limit,
    }
    if filters:
        params.update(filters)

    last_exc: Exception | None = None
    for attempt in range(_RETRIES):
        try:
            res = requests.get(url, params=params, timeout=_TIMEOUT)
            data = res.json()
            return data.get("records", [])
        except requests.Timeout as exc:
            last_exc = exc
            continue  # upstream slow -> retry once more
        except requests.RequestException as exc:
            raise MandiError(f"Could not reach data.gov.in: {exc}") from exc
        except ValueError as exc:  # non-JSON response (bad key, HTML error page)
            raise MandiError(
                "data.gov.in returned an invalid response (check API key)."
            ) from exc

    raise MandiError(
        "data.gov.in is not responding right now (timed out). "
        "This is a temporary issue on the government server; try again shortly."
    ) from last_exc


def _distinct(records: list[dict], field: str) -> list[str]:
    return sorted({r[field] for r in records if r.get(field)})


def list_commodities() -> list[str]:
    return _distinct(_fetch(limit=2000), "commodity")


def list_states(commodity: str) -> list[str]:
    records = _fetch({"filters[commodity]": commodity})
    return _distinct(records, "state")


def list_districts(commodity: str, state: str) -> list[str]:
    records = _fetch(
        {"filters[commodity]": commodity, "filters[state.keyword]": state}
    )
    return _distinct(records, "district")


def list_markets(commodity: str, state: str, district: str) -> list[str]:
    records = _fetch(
        {
            "filters[commodity]": commodity,
            "filters[state.keyword]": state,
            "filters[district.keyword]": district,
        }
    )
    return _distinct(records, "market")


def get_prices(
    commodity: str,
    state: str | None = None,
    district: str | None = None,
    market: str | None = None,
    limit: int = 20,
) -> list[dict]:
    filters: dict = {"filters[commodity]": commodity}
    if state:
        filters["filters[state.keyword]"] = state
    if district:
        filters["filters[district.keyword]"] = district
    if market:
        filters["filters[market.keyword]"] = market

    records = _fetch(filters, limit=limit)
    return [
        {
            "state": r.get("state"),
            "district": r.get("district"),
            "market": r.get("market"),
            "commodity": r.get("commodity"),
            "variety": r.get("variety"),
            "arrival_date": r.get("arrival_date"),
            "min_price": r.get("min_price"),
            "max_price": r.get("max_price"),
            "modal_price": r.get("modal_price"),
        }
        for r in records
    ]
