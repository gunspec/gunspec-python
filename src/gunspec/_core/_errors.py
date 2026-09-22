"""Error hierarchy for the GunSpec SDK.

Every error the SDK raises extends ``GunSpecError``, so one ``except
GunSpecError`` catches them all. HTTP errors returned by the API are mapped to
a subclass of ``APIError`` per status by ``create_api_error`` (in
``_error_factory``); transport failures and misconfiguration have their own
classes under the same root.

An ``APIError`` carries two machine-readable fields. ``code`` is the family
(``UNAUTHORIZED``, ``FORBIDDEN``, ``RATE_LIMITED``) and is stable forever.
``reason`` is the specific situation (``KEY_EXPIRED``, ``PLAN_REQUIRED``,
``DAILY_CAP_EXCEEDED``) and is what a program should branch on, because the
fix for each is different.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..types.error_reasons import ERROR_REASONS, is_error_reason
from ._errors_base import ConfigurationError as ConfigurationError
from ._errors_base import ConnectError as ConnectError
from ._errors_base import GunSpecError as GunSpecError
from ._errors_base import RequestTimeoutError as RequestTimeoutError

# The reason an error with none carries, by status, mirroring the API's own
# default so a ``match`` on ``reason`` never meets ``None``.
_DEFAULT_REASON_BY_STATUS: Dict[int, str] = {
    400: "INVALID_REQUEST",
    401: "AUTH_REQUIRED",
    403: "ACTION_NOT_ALLOWED",
    404: "RESOURCE_NOT_FOUND",
    409: "CONFLICT",
    413: "PAYLOAD_TOO_LARGE",
    429: "RATE_LIMITED",
    503: "DEPENDENCY_UNAVAILABLE",
}


def default_reason_for(status: int) -> str:
    """Return the reason an error with none is given, by HTTP status.

    Args:
        status: The HTTP status code.

    Returns:
        A reason name from ``ERROR_REASONS``.
    """
    return _DEFAULT_REASON_BY_STATUS.get(status, "INTERNAL_ERROR")


class APIError(GunSpecError):
    """An error returned by the GunSpec API with an HTTP status code.

    Attributes:
        status: HTTP status code.
        code: Error family from the response body, e.g. ``"NOT_FOUND"``.
        message: Human-readable message from the API.
        reason: The specific situation, always populated (falls back to the
            status default when the API sent none).
        details: Endpoint-specific detail such as validation issues,
            ``requiredTier`` or ``maxBytes``, or ``None``.
        retry_after: Seconds to wait before retrying, from ``Retry-After``,
            or ``None``.
        request_id: The ``X-Request-Id`` header, to quote in support requests.
        headers: Raw response headers. Never included in ``str`` or ``repr``.
    """

    status: int
    code: str
    message: str
    request_id: str
    headers: Dict[str, str]
    reason: str
    details: Optional[Dict[str, Any]]
    retry_after: Optional[float]

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        *,
        reason: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        retry_after: Optional[float] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.request_id = request_id
        self.headers = headers
        self.reason = reason if reason is not None and is_error_reason(reason) else default_reason_for(status)
        self.details = details
        self.retry_after = retry_after

    @property
    def action(self) -> str:
        """The API's own one-line advice for this reason."""
        return ERROR_REASONS[self.reason]["action"]

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable dict safe to log.

        Never includes the API key or the response headers. Keys are stable:
        ``name``, ``status``, ``code``, ``reason``, ``message``,
        ``request_id``, plus ``details`` and ``retry_after`` when present.
        """
        out: Dict[str, Any] = {
            "name": type(self).__name__,
            "status": self.status,
            "code": self.code,
            "reason": self.reason,
            "message": self.message,
            "request_id": self.request_id,
        }
        if self.details is not None:
            out["details"] = self.details
        if self.retry_after is not None:
            out["retry_after"] = self.retry_after
        return out

    def __str__(self) -> str:
        """``NotFoundError(404 RESOURCE_NOT_FOUND): Firearm 'x' not found [request_id=...]``."""
        suffix = f" [request_id={self.request_id}]" if self.request_id else ""
        return f"{type(self).__name__}({self.status} {self.reason}): {self.message}{suffix}"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(status={self.status}, code={self.code!r}, "
            f"reason={self.reason!r}, message={self.message!r}, request_id={self.request_id!r})"
        )


class BadRequestError(APIError):
    """400 Bad Request: ``INVALID_PARAMETER`` (with ``details`` naming each
    field), ``INVALID_JSON`` or ``INVALID_REQUEST``."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(400, code, message, request_id, headers, **extra)


class AuthenticationError(APIError):
    """401 Unauthorized: the credential itself is the problem, so presenting a
    different key can work. ``reason`` says which: ``KEY_MISSING``,
    ``KEY_INVALID``, ``KEY_DISABLED``, ``KEY_EXPIRED``, ``AUTH_REQUIRED``."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(401, code, message, request_id, headers, **extra)


class PermissionDeniedError(APIError):
    """403 Forbidden: the key is valid and the caller is not permitted.
    Reissuing a key changes nothing. ``reason`` says why: ``PLAN_REQUIRED``
    (see ``required_tier``), ``ACCOUNT_SUSPENDED``, ``KEY_NOT_LINKED_TO_SHOP``,
    ``NOT_OWNER``, ``PAGINATION_DEPTH_EXCEEDED`` and others."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(403, code, message, request_id, headers, **extra)

    @property
    def required_tier(self) -> Optional[str]:
        """The plan this endpoint needs, when ``reason`` is ``PLAN_REQUIRED``."""
        tier = (self.details or {}).get("requiredTier")
        return tier if isinstance(tier, str) else None


class NotFoundError(APIError):
    """404 Not Found: the path is right and no record has that id."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(404, code, message, request_id, headers, **extra)


class ConflictError(APIError):
    """409 Conflict: the request conflicts with existing data."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(409, code, message, request_id, headers, **extra)


class PayloadTooLargeError(APIError):
    """413 Payload Too Large; ``max_bytes`` carries the limit when reported."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(413, code, message, request_id, headers, **extra)

    @property
    def max_bytes(self) -> Optional[int]:
        """The largest body this endpoint accepts, in bytes, if reported."""
        n = (self.details or {}).get("maxBytes")
        return n if isinstance(n, int) else None


class RateLimitError(APIError):
    """429 Too Many Requests.

    ``reason`` distinguishes a per-minute limit (``RATE_LIMITED``, wait
    ``retry_after`` seconds) from the plan's daily allowance
    (``DAILY_CAP_EXCEEDED``, resets at midnight UTC), a pagination burst and
    a repeated data report.
    """

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        retry_after: Optional[float],
        **extra: Any,
    ) -> None:
        extra.pop("retry_after", None)
        super().__init__(429, code, message, request_id, headers, retry_after=retry_after, **extra)

    @property
    def is_daily_cap(self) -> bool:
        """``True`` when the day's allowance is spent and no short wait will help."""
        return self.reason == "DAILY_CAP_EXCEEDED"


class InternalServerError(APIError):
    """500 Internal Server Error: logged on our side against ``request_id``."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(500, code, message, request_id, headers, **extra)


class ServiceUnavailableError(APIError):
    """503: a dependency is down (``DEPENDENCY_UNAVAILABLE``) or the API is
    paused (``MAINTENANCE``, wait ``retry_after`` seconds)."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str,
        headers: Dict[str, str],
        **extra: Any,
    ) -> None:
        super().__init__(503, code, message, request_id, headers, **extra)


def __getattr__(name: str) -> Any:
    """Keep ``from gunspec._core._errors import create_api_error`` working."""
    if name in ("create_api_error", "parse_retry_after", "_parse_retry_after"):
        from . import _error_factory

        return getattr(_error_factory, name.lstrip("_"))
    raise AttributeError(name)
