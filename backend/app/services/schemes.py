"""Government scheme matching. Loads schemes from data/schemes.json."""
from __future__ import annotations

import json
from pathlib import Path

_SCHEMES_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "schemes.json"


def _load() -> list[dict]:
    if not _SCHEMES_PATH.exists():
        return []
    with _SCHEMES_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def match_schemes(land_size: float | None = None, state: str | None = None) -> list[dict]:
    """
    Return schemes a farmer is likely eligible for.

    The rules are intentionally simple and transparent: a scheme is included
    if the farmer's land size falls within the scheme's min/max range (when
    provided) and the state matches (when the scheme is state-specific).
    """
    results: list[dict] = []
    for scheme in _load():
        max_land = scheme.get("max_land_acres")
        scheme_state = scheme.get("state")

        if max_land is not None and land_size is not None and land_size > max_land:
            continue
        if scheme_state and state and scheme_state.lower() != state.lower():
            continue
        results.append(scheme)
    return results
