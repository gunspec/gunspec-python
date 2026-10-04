"""Response parsing helpers shared by the sync and async HTTP clients.

Extracts metadata (rate limit, request id, cache headers), unwraps the
``{"success", "data"}`` envelope, and names the mistake when a binary endpoint
is read as JSON.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

import httpx

from ._error_factory import create_api_error
from ._errors import GunSpecError

T = TypeVar("T")


@dataclass
class RateLimitInfo:
    """What the response said about your allowance.

    The ``daily_*`` fields are the real ones. ``limit``, ``remaining`` and
    ``reset`` are always ``None`` against this API and always were: the edge
    limiter reports whether a request was allowed, not how much of the minute
    is left, so no ``X-RateLimit-*`` header is sent. They are kept so reading
    them keeps working, and will go in the next major.
    """

    limit: Optional[int] = None
    """Deprecated. Always ``None``; use :attr:`daily_limit`."""
    remaining: Optional[int] = None
    """Deprecated. Always ``None``; use :attr:`daily_remaining`."""
    reset: Optional[int] = None
    """Deprecated. Always ``None``; use :attr:`daily_reset`."""
    daily_limit: Optional[int] = None
    """Requests the plan allows per day, or ``None`` on a plan with no ceiling."""
    daily_remaining: Optional[int] = None
    """Requests left today after this one, never below zero: the response to the
    last request that will be served reports ``0``, and the next is refused. A
    figure to pace against: it is served from a short cache until you are near
    the cap, then read live. Reconcile against ``GET /v1/me/usage``."""
    daily_reset: Optional[datetime] = None
    """When the daily counter rolls over (UTC midnight), or ``None``."""
    monthly_limit: Optional[int] = None
    """Requests the plan allows per UTC month, for the whole account (every key
    draws on one pool). ``None`` on a call made without a key, which has the
    daily limit only."""
    monthly_remaining: Optional[int] = None
    """Requests left this month after this one, never below zero. Only calls
    that were served spend it: a call a limit refused, and a ``304``, do not.
    The last request that will be served reports ``0``, and the next is refused
    with ``MONTHLY_CAP_EXCEEDED`` until :attr:`monthly_reset`."""
    monthly_reset: Optional[datetime] = None
    """When the monthly allowance returns to zero (midnight UTC on the 1st), or
    ``None``."""


@dataclass
class PaginationMeta:
    """Pagination metadata from list responses."""

    page: int = 1
    limit: int = 25
    total: Optional[int] = None
    total_pages: Optional[int] = None
    per_page: Optional[int] = None


@dataclass
class APIResponse(Generic[T]):
    """Unwrapped API response for a single resource."""

    data: T
    status: int
    headers: Dict[str, str]
    request_id: str
    rate_limit: RateLimitInfo
    etag: Optional[str] = None
    cache_control: Optional[str] = None
    from_cache: bool = False


@dataclass
class PaginatedResponse(Generic[T]):
    """Unwrapped API response for a paginated list."""

    data: List[T]
    pagination: PaginationMeta
    status: int
    headers: Dict[str, str]
    request_id: str
    rate_limit: RateLimitInfo
    etag: Optional[str] = None
    cache_control: Optional[str] = None
    from_cache: bool = False
    meta: Optional[Dict[str, Any]] = None


@dataclass
class ConditionalResponse(Generic[T]):
    """A conditional GET's outcome: ``not_modified`` with no data, or a body."""

    not_modified: bool
    data: Optional[T]
    status: int
    headers: Dict[str, str]
    request_id: str
    rate_limit: RateLimitInfo
    etag: Optional[str] = None
    cache_control: Optional[str] = None


@dataclass
class RawResponse:
    """A response whose body is bytes rather than an envelope (SVG, GLB, images)."""

    body: bytes
    content_type: Optional[str]
    url: str
    status: int
    headers: Dict[str, str]
    request_id: str
    rate_limit: RateLimitInfo
    etag: Optional[str] = None
    cache_control: Optional[str] = None

    def text(self) -> str:
        return self.body.decode("utf-8")


def parse_rate_limit(headers: httpx.Headers) -> RateLimitInfo:
    """Parse the allowance headers: ``X-Daily-*``, ``X-Monthly-*``, and ``X-RateLimit-*`` if present."""

    def _int_or_none(name: str) -> Optional[int]:
        raw = headers.get(name)
        if raw is None:
            return None
        try:
            return int(raw)
        except (ValueError, TypeError):
            return None

    def _date(name: str) -> Optional[datetime]:
        raw = headers.get(name)
        if raw is None:
            return None
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None

    return RateLimitInfo(
        # Parsed rather than hardcoded to None, so a proxy in front of this API
        # that does send them is still read. GunSpec itself sends none.
        limit=_int_or_none("X-RateLimit-Limit"),
        remaining=_int_or_none("X-RateLimit-Remaining"),
        reset=_int_or_none("X-RateLimit-Reset"),
        daily_limit=_int_or_none("X-Daily-Limit"),
        daily_remaining=_int_or_none("X-Daily-Remaining"),
        daily_reset=_date("X-Daily-Reset"),
        monthly_limit=_int_or_none("X-Monthly-Limit"),
        monthly_remaining=_int_or_none("X-Monthly-Remaining"),
        monthly_reset=_date("X-Monthly-Reset"),
    )


def extract_request_id(headers: httpx.Headers) -> str:
    return str(headers.get("X-Request-Id", ""))


def headers_to_dict(headers: httpx.Headers) -> Dict[str, str]:
    return dict(headers.items())


def response_meta(response: httpx.Response) -> Dict[str, Any]:
    """The keyword arguments every response dataclass shares."""
    return {
        "status": response.status_code,
        "headers": headers_to_dict(response.headers),
        "request_id": extract_request_id(response.headers),
        "rate_limit": parse_rate_limit(response.headers),
        "etag": response.headers.get("ETag"),
        "cache_control": response.headers.get("Cache-Control"),
    }


def raise_api_error(response: httpx.Response) -> None:
    body: Optional[Dict[str, Any]] = None
    try:
        parsed = response.json()
        body = parsed if isinstance(parsed, dict) else None
    except Exception:
        pass
    raise create_api_error(
        response.status_code, body, extract_request_id(response.headers), headers_to_dict(response.headers)
    )


def parse_envelope(text: str, content_type: Optional[str]) -> Dict[str, Any]:
    """Parse a single-resource envelope, naming the right method when the
    body is not JSON (an SVG or GLB read through the JSON path)."""
    try:
        parsed = json.loads(text)
    except ValueError as exc:
        kind = f" ({content_type})" if content_type else ""
        raise GunSpecError(
            f"Response body is not JSON{kind}. Use get_text() or get_bytes() for binary endpoints."
        ) from exc
    if not isinstance(parsed, dict) or "data" not in parsed:
        raise GunSpecError('Response body is not a GunSpec envelope (missing "data")')
    return parsed


def parse_paginated_envelope(
    text: str, content_type: Optional[str]
) -> Tuple[List[Any], PaginationMeta, Optional[Dict[str, Any]]]:
    parsed = parse_envelope(text, content_type)
    raw = parsed.get("pagination")
    if not isinstance(parsed.get("data"), list) or not isinstance(raw, dict):
        raise GunSpecError('Response body is not a paginated GunSpec envelope (missing "pagination")')
    pagination = PaginationMeta(
        page=raw.get("page", 1),
        limit=raw.get("limit", 25),
        total=raw.get("total"),
        total_pages=raw.get("totalPages"),
        per_page=raw.get("per_page"),
    )
    meta = parsed.get("meta")
    return parsed["data"], pagination, meta if isinstance(meta, dict) else None
