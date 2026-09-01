"""Local terminal test harness for the portable Dolly core.

This is the only file in this project with input()/print() -- core.py,
persona.py, and log_store.py have no idea whether they're being driven
from a terminal, a future Twilio webhook, or anything else. When Twilio
gets added, this file is what gets replaced by a web server route; core.py
and persona.py stay exactly as they are.
"""

from __future__ import annotations

import log_store
from core import build_todays_context, get_dolly_reply


def main() -> None:
    context = build_todays_context()
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
