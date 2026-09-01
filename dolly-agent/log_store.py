"""Read/append/query Dolly's check-in log.

The log is an append-only markdown file where each entry is a small YAML
block delimited by `---` lines. This module never rewrites past entries —
it only reads them and appends new ones.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date, datetime
from zoneinfo import ZoneInfo

import yaml

LOCAL_TZ = ZoneInfo("America/Los_Angeles")

DEFAULT_LOG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "dolly-log", "check-in-log.md"
)

HABITS = [
    "marijuana_free",
    "bedtime_by_11",
    "workout",
    "meditation",
    "yoga",
    "outdoor_walk_run",
    "dog_park",
    "healthy_meal",
    "sleep",
]

# Goal habits that get *chosen* in the morning (no streak change yet -- nothing's
# been done today) and *completed* in the evening (this is what actually moves
# the streak). marijuana_free/bedtime_by_11/sleep are reported directly each
# morning about the prior night/period, so they don't need this two-step
# handling -- see core.py's streak logic.
ACTIVITY_HABITS = [
    "workout",
    "meditation",
    "yoga",
    "outdoor_walk_run",
    "dog_park",
    "healthy_meal",
]


@dataclass
class Entry:
    date: date
    time_of_day: str
    habit: str
    status: bool | None
    value: str | None
    streak: int
    notes: str = ""


def today_local() -> date:
    """The real local date, pulled live -- never hardcoded or assumed."""
    return datetime.now(LOCAL_TZ).date()


def read_entries(path: str = DEFAULT_LOG_PATH) -> list[Entry]:
    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        text = f.read()

    blocks = text.split("---")
    entries: list[Entry] = []
    for block in blocks:
        block = block.strip()
        if not block or ":" not in block:
            continue
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict) or "date" not in data or "habit" not in data:
            continue
        entries.append(
            Entry(
                date=data["date"] if isinstance(data["date"], date) else date.fromisoformat(str(data["date"])),
                time_of_day=data.get("time_of_day", ""),
                habit=data["habit"],
                status=data.get("status"),
                value=data.get("value"),
                streak=data.get("streak", 0),
                notes=data.get("notes", "") or "",
            )
        )
    return entries


def append_entries(entries: list[Entry], path: str = DEFAULT_LOG_PATH) -> None:
    lines = []
    for e in entries:
        block = {
            "date": e.date.isoformat(),
            "time_of_day": e.time_of_day,
            "habit": e.habit,
            "status": e.status,
            "value": e.value,
            "streak": e.streak,
            "notes": e.notes,
        }
        lines.append("---\n" + yaml.safe_dump(block, sort_keys=False) + "---\n")

    with open(path, "a") as f:
        f.write("\n" + "\n".join(lines))


def latest_streak(entries: list[Entry], habit: str) -> int:
    """Current streak for a habit: the streak value on its most recent entry."""
    matches = [e for e in entries if e.habit == habit]
    if not matches:
        return 0
    return max(matches, key=lambda e: e.date).streak


def next_streak(entries: list[Entry], habit: str, achieved_today: bool) -> int:
    """What the new streak should be, given whether the habit was achieved today."""
    if not achieved_today:
        return 0
    return latest_streak(entries, habit) + 1


def entries_for_date(entries: list[Entry], on_date: date) -> list[Entry]:
    return [e for e in entries if e.date == on_date]
