from __future__ import annotations

from typing import TypedDict


class ErrorDetail(TypedDict):
    """Individual error detail returned by the API."""

    code: str
    message: str


class APIErrorResponse(TypedDict):
    """Top-level error response envelope."""

    success: bool
    error: ErrorDetail
