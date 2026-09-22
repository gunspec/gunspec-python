"""Webhook signature verification for the GunSpec SDK.

Every delivery carries ``X-Webhook-Signature: t=<unix seconds>,v1=<hex>``,
where ``v1`` is HMAC-SHA256 over ``f"{t}.{raw_body}"`` with the endpoint's
signing key. Verifying it proves the body came from GunSpec and was not
altered; the timestamp check refuses a captured delivery replayed later.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ._errors import GunSpecError

WEBHOOK_HEADERS: Dict[str, str] = {
    "signature": "X-Webhook-Signature",
    "event_id": "X-Webhook-Id",
    "event_type": "X-Webhook-Event",
    "delivery_id": "X-Webhook-Delivery",
}
"""The delivery headers a receiver should read. Dedupe on the event id; quote
the delivery id when asking why one never arrived."""

_HEX = re.compile(r"^[0-9a-fA-F]+$")


class WebhookSignatureError(GunSpecError):
    """Raised when a delivery fails verification. The body is untrusted."""


def parse_signature_header(header: Optional[str]) -> Tuple[int, List[str]]:
    """Parse ``t=...,v1=...`` into ``(timestamp, [signatures])``."""
    if not header:
        raise WebhookSignatureError("Missing X-Webhook-Signature header")
    timestamp: Optional[int] = None
    signatures: List[str] = []
    for part in header.split(","):
        key, sep, value = part.partition("=")
        if not sep:
            continue
        key, value = key.strip(), value.strip()
        if key == "t":
            try:
                timestamp = int(float(value))
            except ValueError:
                timestamp = None
        elif key == "v1" and _HEX.match(value):
            signatures.append(value.lower())
    if timestamp is None:
        raise WebhookSignatureError("X-Webhook-Signature has no valid timestamp")
    if not signatures:
        raise WebhookSignatureError("X-Webhook-Signature has no v1 signature")
    return timestamp, signatures


def sign_webhook_payload(secret: str, timestamp: Union[int, str], body: str) -> str:
    """HMAC-SHA256 hex of ``f"{timestamp}.{body}"``, exactly as the API computes it."""
    return hmac.new(secret.encode("utf-8"), f"{timestamp}.{body}".encode(), hashlib.sha256).hexdigest()


def verify_webhook_signature(
    raw_body: Union[str, bytes],
    signature_header: Optional[str],
    secret: str,
    *,
    tolerance_seconds: int = 300,
    now: Optional[Callable[[], float]] = None,
) -> None:
    """Verify a delivery.

    Returns when the signature is genuine and the timestamp is inside the
    tolerance; raises ``WebhookSignatureError`` otherwise.

    ``raw_body`` must be the request body as received, before any JSON
    parsing: re-serialising a parsed object changes whitespace and breaks the
    HMAC.
    """
    if not secret:
        raise WebhookSignatureError("Webhook secret is empty")
    body = raw_body.decode("utf-8") if isinstance(raw_body, bytes) else raw_body
    timestamp, signatures = parse_signature_header(signature_header)

    current = int((now or time.time)())
    if abs(current - timestamp) > tolerance_seconds:
        raise WebhookSignatureError(f"Delivery timestamp is outside the {tolerance_seconds}s tolerance")

    expected = sign_webhook_payload(secret, timestamp, body)
    if not any(hmac.compare_digest(sig, expected) for sig in signatures):
        raise WebhookSignatureError("Signature does not match")


def construct_webhook_event(
    raw_body: Union[str, bytes],
    signature_header: Optional[str],
    secret: str,
    *,
    tolerance_seconds: int = 300,
    now: Optional[Callable[[], float]] = None,
) -> Dict[str, Any]:
    """Verify a delivery and parse it into its event dict
    (``id``, ``type``, ``created_at``, ``data``).

    Example::

        event = construct_webhook_event(request.body, request.headers.get("X-Webhook-Signature"), key)
        if event["type"] == "firearm.updated":
            mirror.upsert(event["data"])
    """
    verify_webhook_signature(raw_body, signature_header, secret, tolerance_seconds=tolerance_seconds, now=now)
    body = raw_body.decode("utf-8") if isinstance(raw_body, bytes) else raw_body
    try:
        parsed = json.loads(body)
    except ValueError as exc:
        raise WebhookSignatureError("Delivery body is not JSON") from exc
    if not isinstance(parsed, dict):
        raise WebhookSignatureError("Delivery body is not an object")
    if (
        not isinstance(parsed.get("id"), str)
        or not isinstance(parsed.get("type"), str)
        or "data" not in parsed
    ):
        raise WebhookSignatureError("Delivery body is not a webhook event")
    # An event type this SDK has not heard of is let through: the versioning
    # promise is that new events arrive without a new API version.
    return parsed
