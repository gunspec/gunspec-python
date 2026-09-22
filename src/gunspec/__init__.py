"""GunSpec.io Python SDK."""

from __future__ import annotations

from gunspec._client import AsyncGunSpec, GunSpec
from gunspec._core._auth import AuthScheme, mask_api_key
from gunspec._core._errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConfigurationError,
    ConflictError,
    ConnectError,
    GunSpecError,
    InternalServerError,
    NotFoundError,
    PayloadTooLargeError,
    PermissionDeniedError,
    RateLimitError,
    RequestTimeoutError,
    ServiceUnavailableError,
)
from gunspec._core._etag_cache import CachedEntry, ETagStore, MemoryETagStore
from gunspec._core._http_client import (
    APIResponse,
    ConditionalResponse,
    HttpClientConfig,
    PaginatedResponse,
    PaginationMeta,
    RateLimitInfo,
    RawResponse,
)
from gunspec._core._pagination import AsyncPage, SyncPage
from gunspec._core._retry import RetryConfig
from gunspec._core._webhook_signature import (
    WEBHOOK_HEADERS,
    WebhookSignatureError,
    construct_webhook_event,
    sign_webhook_payload,
    verify_webhook_signature,
)
from gunspec._version import __version__
from gunspec.types.error_reasons import ERROR_REASONS, ErrorReason
from gunspec.types.webhook_events import WEBHOOK_EVENT_TYPES, WebhookEventType

__all__ = [
    # Client
    "GunSpec",
    "AsyncGunSpec",
    # Version
    "__version__",
    # Config
    "HttpClientConfig",
    "RetryConfig",
    "AuthScheme",
    "mask_api_key",
    # Response types
    "APIResponse",
    "PaginatedResponse",
    "ConditionalResponse",
    "RawResponse",
    "PaginationMeta",
    "RateLimitInfo",
    # Conditional requests
    "ETagStore",
    "MemoryETagStore",
    "CachedEntry",
    # Pagination
    "SyncPage",
    "AsyncPage",
    # Webhooks
    "WEBHOOK_HEADERS",
    "WEBHOOK_EVENT_TYPES",
    "WebhookEventType",
    "WebhookSignatureError",
    "sign_webhook_payload",
    "verify_webhook_signature",
    "construct_webhook_event",
    # Errors
    "GunSpecError",
    "APIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "BadRequestError",
    "ConflictError",
    "PayloadTooLargeError",
    "RateLimitError",
    "InternalServerError",
    "ServiceUnavailableError",
    "ConnectError",
    "RequestTimeoutError",
    "ConfigurationError",
    "ERROR_REASONS",
    "ErrorReason",
]
