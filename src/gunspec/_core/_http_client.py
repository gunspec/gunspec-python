"""Compatibility shim: the transport lives in ``gunspec._core._http``."""

from __future__ import annotations

from ._http import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    SDK_USER_AGENT,
    APIResponse,
    AsyncHttpClient,
    ConditionalResponse,
    HttpClientConfig,
    PaginatedResponse,
    PaginationMeta,
    Query,
    RateLimitInfo,
    RawResponse,
    SyncHttpClient,
    serialize_query,
)

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "SDK_USER_AGENT",
    "HttpClientConfig",
    "Query",
    "APIResponse",
    "PaginatedResponse",
    "ConditionalResponse",
    "RawResponse",
    "PaginationMeta",
    "RateLimitInfo",
    "SyncHttpClient",
    "AsyncHttpClient",
    "serialize_query",
]
