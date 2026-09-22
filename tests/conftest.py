"""Shared test fixtures for the GunSpec Python SDK."""

from __future__ import annotations

from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest

from gunspec._core._http_client import (
    APIResponse,
    PaginatedResponse,
    PaginationMeta,
    RateLimitInfo,
    RawResponse,
)


def make_api_response(
    data: Any = None,
    status: int = 200,
    request_id: str = "req-test-123",
) -> APIResponse[Any]:
    """Build a mock APIResponse."""
    return APIResponse(
        data=data or {},
        status=status,
        headers={"x-request-id": request_id},
        request_id=request_id,
        rate_limit=RateLimitInfo(limit=100, remaining=99, reset=1700000000),
    )


def make_paginated_response(
    data: Any = None,
    page: int = 1,
    limit: int = 25,
    total: int = 1,
    total_pages: int = 1,
    status: int = 200,
    request_id: str = "req-test-123",
) -> PaginatedResponse[Any]:
    """Build a mock PaginatedResponse."""
    return PaginatedResponse(
        data=data or [],
        pagination=PaginationMeta(page=page, limit=limit, total=total, total_pages=total_pages),
        status=status,
        headers={"x-request-id": request_id},
        request_id=request_id,
        rate_limit=RateLimitInfo(limit=100, remaining=99, reset=1700000000),
    )


def make_raw_response(text: str = "", content_type: str = "application/octet-stream") -> RawResponse:
    """Build a mock RawResponse."""
    return RawResponse(
        body=text.encode("utf-8"),
        content_type=content_type,
        url="https://api.gunspec.io/raw",
        status=200,
        headers={},
        request_id="req-test-123",
        rate_limit=RateLimitInfo(limit=100, remaining=99, reset=1700000000),
    )


def _url_for(path: str, query: Optional[Dict[str, Any]] = None) -> str:
    from urllib.parse import urlencode

    qs = urlencode({k: v for k, v in (query or {}).items() if v is not None})
    return f"https://api.gunspec.io{path}" + (f"?{qs}" if qs else "")


@pytest.fixture()
def mock_sync_client() -> MagicMock:
    """Return a MagicMock that behaves like SyncHttpClient."""
    client = MagicMock()
    client.get.return_value = make_api_response()
    client.get_paginated.return_value = make_paginated_response()
    client.post.return_value = make_api_response()
    client.put.return_value = make_api_response()
    client.delete.return_value = make_api_response()
    client.patch.return_value = make_api_response()
    client.get_text.return_value = ""
    client.get_bytes.return_value = make_raw_response()
    client.resolve_redirect.return_value = None
    client.url_for.side_effect = _url_for
    client.is_authenticated = True
    return client


@pytest.fixture()
def mock_async_client() -> AsyncMock:
    """Return an AsyncMock that behaves like AsyncHttpClient."""
    client = AsyncMock()
    client.get.return_value = make_api_response()
    client.get_paginated.return_value = make_paginated_response()
    client.post.return_value = make_api_response()
    client.put.return_value = make_api_response()
    client.delete.return_value = make_api_response()
    client.patch.return_value = make_api_response()
    client.get_text.return_value = ""
    client.get_bytes.return_value = make_raw_response()
    client.resolve_redirect.return_value = None
    client.url_for = MagicMock(side_effect=_url_for)
    client.is_authenticated = True
    return client
