"""Krishi Diary: generate a date-stamped activity schedule for a crop."""
from __future__ import annotations

from datetime import date, datetime, timedelta

from .crop_knowledge import CROPS


def build_calendar(crop: str, sowing_date: str | None = None) -> dict:
    info = CROPS.get(crop)
    if not info:
        raise ValueError(f"Unknown crop '{crop}'")

    start = (
        datetime.strptime(sowing_date, "%Y-%m-%d").date()
        if sowing_date
        else date.today()
    )
    today = date.today()

    items = []
    for offset, task in info["schedule"]:
        due = start + timedelta(days=offset)
        days_away = (due - today).days
        if days_away < -3:
            status = "done"
        elif days_away <= 3:
            status = "due"
        else:
            status = "upcoming"
        items.append(
            {
                "date": due.isoformat(),
                "day_offset": offset,
                "task": task,
                "status": status,
                "days_away": days_away,
            }
        )

    next_task = next((i for i in items if i["status"] != "done"), None)
    return {
        "crop": crop,
        "sowing_date": start.isoformat(),
        "duration_days": info["duration_days"],
        "harvest_date": (start + timedelta(days=info["duration_days"])).isoformat(),
        "next_task": next_task,
        "schedule": items,
    }
