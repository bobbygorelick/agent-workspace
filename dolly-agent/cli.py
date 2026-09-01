"""Local terminal test harness for the portable Dolly core.

This is the only file in this project with input()/print() -- core.py,
persona.py, and log_store.py have no idea whether they're being driven
from a terminal, a future Twilio webhook, or anything else. When Twilio
gets added, this file is what gets replaced by a web server route; core.py
and persona.py stay exactly as they are.
"""

from __future__ import annotations

import log_store
from core import CheckInContext, get_dolly_reply
from log_store import ACTIVITY_HABITS, HABITS


def _build_context() -> CheckInContext:
    entries = log_store.read_entries()
    today = log_store.today_local()
    todays_entries = log_store.entries_for_date(entries, today)

    already_morning = any(e.time_of_day == "morning" for e in todays_entries)
    time_of_day = "evening" if already_morning else "morning"

    streaks = {
        habit: log_store.latest_streak(entries, habit)
        for habit in HABITS
        if habit != "sleep"
    }

    mornings_goals = [
        e.habit
        for e in todays_entries
        if e.time_of_day == "morning" and e.habit in ACTIVITY_HABITS and e.status
    ]

    return CheckInContext(
        today=today,
        time_of_day=time_of_day,
        streaks=streaks,
        mornings_goals=mornings_goals,
    )


def main() -> None:
    context = _build_context()
    print(
        f"(Starting Dolly's {context.time_of_day} check-in for "
        f"{context.today.isoformat()}. Type 'quit' to stop.)\n"
    )

    history: list = []
    while True:
        message = input("You: ").strip()
        if not message:
            continue
        if message.lower() in ("quit", "exit"):
            break

        reply = get_dolly_reply(message, history, context)
        print(f"Dolly: {reply.text}\n")

        history = reply.raw_history
        if reply.new_entries:
            log_store.append_entries(reply.new_entries)


if __name__ == "__main__":
    main()
