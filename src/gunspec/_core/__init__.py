from __future__ import annotations

from ._auth import (
    UNSET,
    AuthScheme,
    assert_transport_security,
    build_auth_headers,
    mask_api_key,
    resolve_api_key,
)
from ._error_factory import create_api_error, parse_retry_after
from ._errors import (
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
from ._etag_cache import CachedEntry, ETagStore, MemoryETagStore, cache_key_for, credential_fingerprint
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
from ._pagination import AsyncPage, SyncPage
from ._retry import RetryConfig, async_with_retry, compute_delay, is_retryable, with_retry
from ._webhook_signature import (
    WEBHOOK_HEADERS,
    WebhookSignatureError,
    construct_webhook_event,
    parse_signature_header,
    sign_webhook_payload,
    verify_webhook_signature,
)

__all__ = [
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
    "create_api_error",
    "parse_retry_after",
    # Auth
    "AuthScheme",
    "UNSET",
    "resolve_api_key",
    "build_auth_headers",
    "mask_api_key",
    "assert_transport_security",
    # HTTP client
    "SyncHttpClient",
    "AsyncHttpClient",
    "HttpClientConfig",
    "Query",
    "APIResponse",
    "PaginatedResponse",
    "ConditionalResponse",
    "RawResponse",
    "PaginationMeta",
    "RateLimitInfo",
    "serialize_query",
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "SDK_USER_AGENT",
    # ETag cache
    "ETagStore",
    "MemoryETagStore",
    "CachedEntry",
    "credential_fingerprint",
    "cache_key_for",
    # Webhooks
    "WEBHOOK_HEADERS",
    "WebhookSignatureError",
    "verify_webhook_signature",
    "construct_webhook_event",
    "sign_webhook_payload",
    "parse_signature_header",
    # Pagination
    "SyncPage",
    "AsyncPage",
    # Retry
    "RetryConfig",
    "is_retryable",
    "compute_delay",
    "with_retry",
    "async_with_retry",
]
