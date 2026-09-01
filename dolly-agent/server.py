"""Twilio SMS webhook for Dolly.

This is the only file that knows about Twilio, HTTP, or keeping a
conversation's history alive across separate text messages -- core.py,
persona.py, and log_store.py are untouched, exactly like the old
terminal harness (cli.py) always intended.
"""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from flask import Flask, abort, request
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from werkzeug.middleware.proxy_fix import ProxyFix

import log_store
from core import build_todays_context, get_dolly_reply

load_dotenv()

app = Flask(__name__)
# Render (and most hosts) terminate HTTPS at a proxy and forward plain HTTP
# to the app. Without this, request.url comes back as http://... and
# Twilio's signature check (which was computed against the https:// URL it
# actually called) fails every time.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# A text message is a separate, stateless HTTP request each time, so
# "today's conversation so far" has to be kept somewhere between requests.
# This is a single-user bot, so one small file is all that's needed.
SESSION_PATH = os.path.join(os.path.dirname(__file__), ".session.json")


def _load_history(today_iso: str) -> list:
    if not os.path.exists(SESSION_PATH):
        return []
    with open(SESSION_PATH, "r") as f:
        session = json.load(f)
    return session["history"] if session.get("date") == today_iso else []


def _jsonable(obj):
    """Anthropic SDK content blocks (TextBlock, ToolUseBlock, ...) are
    pydantic objects, not plain dicts -- convert them so history can
    round-trip through JSON between separate HTTP requests."""
    return obj.model_dump() if hasattr(obj, "model_dump") else str(obj)


def _save_history(today_iso: str, history: list) -> None:
    with open(SESSION_PATH, "w") as f:
        json.dump({"date": today_iso, "history": history}, f, default=_jsonable)


def _verify_twilio_request() -> None:
    """Reject anything that didn't actually come from Twilio."""
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    if not auth_token:
        raise RuntimeError(
            "TWILIO_AUTH_TOKEN is not set -- add it to dolly-agent/.env"
        )

    validator = RequestValidator(auth_token)
    signature = request.headers.get("X-Twilio-Signature", "")
    if not validator.validate(request.url, request.form, signature):
        abort(403)


@app.route("/sms", methods=["POST"])
def sms_webhook():
    _verify_twilio_request()

    incoming_message = request.form.get("Body", "").strip()
    context = build_todays_context()
    today_iso = context.today.isoformat()

    reply = get_dolly_reply(incoming_message, _load_history(today_iso), context)

    _save_history(today_iso, reply.raw_history)
    if reply.new_entries:
        log_store.append_entries(reply.new_entries)

    twiml = MessagingResponse()
    twiml.message(reply.text)
    return str(twiml), 200, {"Content-Type": "text/xml"}


@app.route("/health", methods=["GET"])
def health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
