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

from datetime import datetime
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
    (see ``required_tier``), ``ACCOUNT_SUSPENDED``, ``KEY_ON_HOLD`` (this free
    key kept calling after its daily limit refused it and is paused until
    ``retry_after`` seconds from now; a paid plan lifts it at once),
    ``KEY_NOT_LINKED_TO_SHOP``, ``NOT_OWNER``, ``PAGINATION_DEPTH_EXCEEDED``
    and others."""

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


# The two reasons that mean a day's allowance is spent: the plan's, and the
# share of it for the hosted MCP server.
_DAILY_CAP_REASONS = frozenset({"DAILY_CAP_EXCEEDED", "MCP_DAILY_CAP_EXCEEDED"})

# The reason that means the plan's month is spent.
_MONTHLY_CAP_REASON = "MONTHLY_CAP_EXCEEDED"


class RateLimitError(APIError):
    """429 Too Many Requests.

    ``reason`` distinguishes a per-minute limit (``RATE_LIMITED``, wait
    ``retry_after`` seconds) from the plan's daily allowance
    (``DAILY_CAP_EXCEEDED``, resets at midnight UTC), the plan's monthly
    allowance (``MONTHLY_CAP_EXCEEDED``, resets at midnight UTC on the 1st), a
    pagination burst and a repeated data report.

    On a daily or monthly refusal ``retry_after`` is the real time left until
    the reset, up to a whole day or a whole month, and :attr:`daily_reset` or
    :attr:`monthly_reset` says when as a ``datetime``. Nothing is served before
    then, and a free key that keeps calling after being refused is paused, so
    stop and resume at the reset. The SDK retries one of these only when the
    reset is within ``max_retry_after_s`` (a call refused a second before
    midnight waits the second and succeeds); a longer wait is raised at once,
    never slept through.
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
        """``True`` when a day's allowance is spent and no short wait will help.

        The plan's (``DAILY_CAP_EXCEEDED``) or the hosted MCP server's share of
        it (``MCP_DAILY_CAP_EXCEEDED``). Only the daily refusals: the month is
        :attr:`is_monthly_cap`, and a caller that wants "any allowance that
        resets later" writes ``is_daily_cap or is_monthly_cap``.
        """
        return self.reason in _DAILY_CAP_REASONS

    @property
    def is_monthly_cap(self) -> bool:
        """``True`` when the plan's month is spent (``MONTHLY_CAP_EXCEEDED``).

        The allowance belongs to the whole account, so every key is refused
        until the reset, or until the plan changes.
        """
        return self.reason == _MONTHLY_CAP_REASON

    def _header(self, name: str) -> Optional[str]:
        """A response header by name, whatever case the transport gave it."""
        wanted = name.lower()
        for key, value in self.headers.items():
            if key.lower() == wanted:
                return value
        return None

    def _read_limit(self, header: str) -> Optional[int]:
        """The body's ``limit`` when it is an integer, else the named header, else ``None``."""
        from_body = (self.details or {}).get("limit")
        if isinstance(from_body, int) and not isinstance(from_body, bool):
            return from_body
        raw = self._header(header)
        try:
            return int(raw) if raw is not None else None
        except ValueError:
            return None

    def _read_reset(self, header: str) -> Optional[datetime]:
        """The body's ``resetsAt`` when it parses as a date, else the named header, else ``None``."""
        for value in ((self.details or {}).get("resetsAt"), self._header(header)):
            if not isinstance(value, str):
                continue
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                continue
        return None

    @property
    def daily_limit(self) -> Optional[int]:
        """The daily limit that was reached, per key.

        ``None`` when this is not a daily refusal or the API did not say. Read
        from the response body's ``limit``, then the ``X-Daily-Limit`` header
        (``X-Daily-MCP-Limit`` for the MCP share).
        """
        if not self.is_daily_cap:
            return None
        mcp = self.reason == "MCP_DAILY_CAP_EXCEEDED"
        return self._read_limit("X-Daily-MCP-Limit" if mcp else "X-Daily-Limit")

    @property
    def daily_reset(self) -> Optional[datetime]:
        """When the daily counters return to zero: the next midnight UTC.

        ``None`` when this is not a daily refusal or the API did not say. Read
        from the response body's ``resetsAt``, then the ``X-Daily-Reset`` header
        (``X-Daily-MCP-Reset`` for the MCP share). A timezone-aware ``datetime``,
        the same instant as ``retry_after`` seconds from now.
        """
        if not self.is_daily_cap:
            return None
        mcp = self.reason == "MCP_DAILY_CAP_EXCEEDED"
        return self._read_reset("X-Daily-MCP-Reset" if mcp else "X-Daily-Reset")

    @property
    def monthly_limit(self) -> Optional[int]:
        """The monthly allowance that was reached, for the whole account.

        ``None`` when this is not a monthly refusal or the API did not say. Read
        from the response body's ``limit``, then the ``X-Monthly-Limit`` header.
        """
        if not self.is_monthly_cap:
            return None
        return self._read_limit("X-Monthly-Limit")

    @property
    def monthly_reset(self) -> Optional[datetime]:
        """When the monthly allowance returns to zero: midnight UTC on the 1st.

        ``None`` when this is not a monthly refusal or the API did not say. Read
        from the response body's ``resetsAt``, then the ``X-Monthly-Reset``
        header. A timezone-aware ``datetime``.
        """
        if not self.is_monthly_cap:
            return None
        return self._read_reset("X-Monthly-Reset")


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
