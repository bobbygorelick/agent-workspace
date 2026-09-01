"""Transport-agnostic Dolly conversation logic.

get_dolly_reply() is the piece meant to survive the move to a real server
later: give it an incoming message, the conversation so far, and today's
context (already assembled by the caller), and it returns a reply plus
any habit observations to record. It knows nothing about terminals, HTTP,
SMS, or even the log file's storage format -- that's the caller's job
(see cli.py and log_store.py).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date

import anthropic
from dotenv import load_dotenv

import log_store
from log_store import ACTIVITY_HABITS, Entry, HABITS
from persona import build_system_prompt

load_dotenv()

MODEL = "claude-sonnet-5"


@dataclass
class CheckInContext:
    today: date
    time_of_day: str  # "morning" or "evening"
    streaks: dict  # habit name -> current streak count
    mornings_goals: list = field(default_factory=list)


def build_todays_context() -> CheckInContext:
    """Build today's CheckInContext straight from the log file.

    Shared by every entry point (terminal, SMS) so morning/evening
    detection and streak math can't drift between them.
    """
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


@dataclass
class DollyReply:
    text: str
    new_entries: list = field(default_factory=list)
    raw_history: list = field(default_factory=list)


LOG_HABIT_TOOL = {
    "name": "log_habit",
    "description": "Record a single habit observation from today's check-in.",
    "input_schema": {
        "type": "object",
        "properties": {
            "habit": {"type": "string", "enum": HABITS},
            "status": {
                "type": "boolean",
                "description": "Whether the habit was achieved (ignored for 'sleep').",
            },
            "value": {
                "type": "string",
                "description": "Extra free-form data, e.g. bedtime/wake time for 'sleep'.",
            },
            "notes": {"type": "string", "description": "Optional short note."},
        },
        "required": ["habit", "status"],
    },
}


def _client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set -- add it to dolly-agent/.env "
            "(see .env.example)."
        )
    return anthropic.Anthropic(api_key=api_key)


def get_dolly_reply(
    message: str, history: list, context: CheckInContext
) -> DollyReply:
    """Given an incoming message and today's context, return Dolly's reply
    plus any habit entries to persist. Performs the Anthropic tool-use loop
    itself since a single model turn may log several habits before
    producing user-facing text.
    """
    client = _client()
    system = build_system_prompt(
        today=context.today.isoformat(),
        time_of_day=context.time_of_day,
        streaks=context.streaks,
        mornings_goals=context.mornings_goals,
    )
    streaks = dict(context.streaks)
    conversation = list(history) + [{"role": "user", "content": message}]
    new_entries: list[Entry] = []

    for _ in range(5):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system,
            tools=[LOG_HABIT_TOOL],
            messages=conversation,
        )
        conversation.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            reply_text = "".join(
                b.text for b in response.content if b.type == "text"
            )
            return DollyReply(
                text=reply_text, new_entries=new_entries, raw_history=conversation
            )

        tool_results = []
        for block in tool_uses:
            habit = block.input["habit"]
            status = bool(block.input.get("status", True))
            value = block.input.get("value") or None
            notes = block.input.get("notes", "") or ""

            if habit == "sleep":
                streak = 0
            elif context.time_of_day == "morning" and habit in ACTIVITY_HABITS:
                # Morning = goal chosen, not completed yet -- carry the streak
                # forward unchanged. The evening completion entry is what
                # actually moves it.
                streak = streaks.get(habit, 0)
            else:
                streak = streaks.get(habit, 0) + 1 if status else 0
                streaks[habit] = streak

            new_entries.append(
                Entry(
                    date=context.today,
                    time_of_day=context.time_of_day,
                    habit=habit,
                    status=status,
                    value=value,
                    streak=streak,
                    notes=notes,
                )
            )
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Logged {habit} (streak now {streak}).",
                }
            )

        conversation.append({"role": "user", "content": tool_results})

    return DollyReply(
        text="(Dolly got a little tongue-tied there -- mind saying that again?)",
        new_entries=new_entries,
        raw_history=conversation,
    )
