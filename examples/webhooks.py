"""Receive and verify GunSpec webhook deliveries.

A minimal WSGI app so the example has no web-framework dependency. Run it
with ``GUNSPEC_WEBHOOK_SECRET`` set to the endpoint's signing key, then run a
tunnel to ``http://127.0.0.1:8000`` and point an endpoint at its public https
URL plus ``/hooks/gunspec`` (the API only delivers to public https URLs).

    uv run python examples/webhooks.py
"""

from __future__ import annotations

import os
import sys
from typing import Any, Callable, Iterable, List, Tuple
from wsgiref.simple_server import make_server

from gunspec import WEBHOOK_HEADERS, WebhookSignatureError, construct_webhook_event

StartResponse = Callable[[str, List[Tuple[str, str]]], Any]


def app(environ: dict, start_response: StartResponse) -> Iterable[bytes]:
    if environ.get("PATH_INFO") != "/hooks/gunspec" or environ.get("REQUEST_METHOD") != "POST":
        start_response("404 Not Found", [])
        return [b""]

    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw_body = environ["wsgi.input"].read(length)  # verify the bytes as received
    header_key = "HTTP_" + WEBHOOK_HEADERS["signature"].upper().replace("-", "_")

    try:
        event = construct_webhook_event(
            raw_body, environ.get(header_key), os.environ["GUNSPEC_WEBHOOK_SECRET"]
        )
    except WebhookSignatureError as err:
        sys.stderr.write(f"refused delivery: {err}\n")
        start_response("400 Bad Request", [])
        return [b""]

    # Dedupe on the event id: a retry re-sends the same one.
    sys.stdout.write(f"{event['id']} {event['type']} {event['created_at']}\n")
    if event["type"] in ("firearm.created", "firearm.updated"):
        record = event["data"]
        sys.stdout.write(f"  upsert {record['id']} version={record.get('version')}\n")
    elif event["type"] == "firearm.deleted":
        sys.stdout.write(f"  delete {event['data']['id']}\n")
    elif event["type"] == "catalog.resynced":
        sys.stdout.write("  whole catalog re-stamped: refetch everything\n")

    start_response("204 No Content", [])
    return [b""]


if __name__ == "__main__":
    # Loopback only. The tunnel (or reverse proxy) that gives the endpoint its
    # public https URL forwards to 127.0.0.1:8000; nothing else on the network
    # needs to reach this process directly.
    with make_server("127.0.0.1", 8000, app) as server:
        sys.stdout.write("listening on 127.0.0.1:8000/hooks/gunspec\n")
        server.serve_forever()
