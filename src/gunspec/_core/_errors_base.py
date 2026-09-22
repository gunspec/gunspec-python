"""The error hierarchy root and the errors raised before or instead of an
HTTP response: configuration, connection, timeout.

The API-status errors live in ``_errors``; everything shares
``GunSpecError`` so one ``except GunSpecError`` catches the lot.
"""

from __future__ import annotations

from typing import Optional


class GunSpecError(Exception):
    """Base class for every error raised by the GunSpec SDK."""


class ConfigurationError(GunSpecError):
    """Raised before any request is sent when the client cannot be used safely.

    Examples: an API key over plain ``http://`` to a remote host, or a base
    URL that is not a URL.
    """


class ConnectError(GunSpecError):
    """A network-level failure (DNS, connection reset) before any response.

    Attributes:
        cause: The underlying httpx exception, if any.
    """

    cause: Optional[BaseException]

    def __init__(self, message: str, cause: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.cause = cause

    def __repr__(self) -> str:
        return f"ConnectError({str(self)!r})"


class RequestTimeoutError(GunSpecError):
    """The request exceeded the configured timeout.

    Attributes:
        timeout_s: The timeout that was exceeded, in seconds.
    """

    timeout_s: float

    def __init__(self, timeout_s: float) -> None:
        super().__init__(f"Request timed out after {timeout_s}s")
        self.timeout_s = timeout_s

    def __repr__(self) -> str:
        return f"RequestTimeoutError(timeout_s={self.timeout_s!r})"
