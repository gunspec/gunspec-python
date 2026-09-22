"""Build the right ``APIError`` subclass from an HTTP response."""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ._errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PayloadTooLargeError,
    PermissionDeniedError,
    RateLimitError,
    ServiceUnavailableError,
)

_CORE_KEYS = frozenset({"code", "message", "reason", "request_id", "details"})


def parse_retry_after(headers: Dict[str, str]) -> Optional[float]:
    """Parse a ``Retry-After`` header into seconds.

    Args:
        headers: Response headers; the lookup is case-insensitive on the two
            common spellings.

    Returns:
        Seconds to wait, from delta-seconds or an HTTP-date, or ``None``.
    """
    raw = headers.get("Retry-After") or headers.get("retry-after")
    if raw is None:
        return None

    try:
        seconds = float(raw)
        if not math.isnan(seconds) and seconds >= 0:
            return seconds
    except ValueError:
        pass

    try:
        dt = datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S %Z")
        dt = dt.replace(tzinfo=timezone.utc)
        delta = (dt - datetime.now(timezone.utc)).total_seconds()
        return max(delta, 0.0)
    except ValueError:
        pass

    return None


def _extract_details(error: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Body fields that are neither the core four nor ``request_id`` are detail."""
    merged: Dict[str, Any] = {}
    details = error.get("details")
    if isinstance(details, dict):
        merged.update(details)
    for key, value in error.items():
        if key not in _CORE_KEYS:
            merged[key] = value
    return merged or None


def create_api_error(
    status: int,
    body: Optional[Dict[str, Any]],
    request_id: str,
    headers: Dict[str, str],
) -> APIError:
    """Create the ``APIError`` subclass for an HTTP status and error envelope.

    Args:
        status: HTTP status code.
        body: The parsed JSON body, or ``None`` when it was empty or not JSON.
        request_id: The ``X-Request-Id`` header; the body's ``request_id`` is
            used when the header is absent.
        headers: Response headers, for ``Retry-After`` and inspection.

    Returns:
        A concrete ``APIError`` subclass, or ``APIError`` itself for a status
        without one.
    """
    raw = body.get("error", {}) if body else {}
    error_data: Dict[str, Any] = raw if isinstance(raw, dict) else {}
    code: str = error_data.get("code", f"HTTP_{status}")
    message: str = error_data.get("message", f"Request failed with status {status}")
    retry_after = parse_retry_after(headers)
    extra: Dict[str, Any] = {
        "reason": error_data.get("reason"),
        "details": _extract_details(error_data) if error_data else None,
        "retry_after": retry_after,
    }
    rid = request_id or str(error_data.get("request_id") or "")

    if status == 400:
        return BadRequestError(code, message, rid, headers, **extra)
    if status == 401:
        return AuthenticationError(code, message, rid, headers, **extra)
    if status == 403:
        return PermissionDeniedError(code, message, rid, headers, **extra)
    if status == 404:
        return NotFoundError(code, message, rid, headers, **extra)
    if status == 409:
        return ConflictError(code, message, rid, headers, **extra)
    if status == 413:
        return PayloadTooLargeError(code, message, rid, headers, **extra)
    if status == 429:
        extra.pop("retry_after")
        return RateLimitError(code, message, rid, headers, retry_after, **extra)
    if status == 500:
        return InternalServerError(code, message, rid, headers, **extra)
    if status == 503:
        return ServiceUnavailableError(code, message, rid, headers, **extra)
    return APIError(status, code, message, rid, headers, **extra)
