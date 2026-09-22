from __future__ import annotations

import os
from typing import Dict, Literal, Optional
from urllib.parse import urlsplit

from ._errors import ConfigurationError

AuthScheme = Literal["x-api-key", "bearer"]
"""Which header carries the key. Both are canonical and permanent on the API;
``X-API-Key`` wins when a caller sends both."""

_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "[::1]"})


class _Unset:
    """Sentinel for "no ``api_key`` argument was given", so that an explicit
    ``None`` can mean anonymous on purpose while an omitted key still falls
    back to ``GUNSPEC_API_KEY``."""

    def __repr__(self) -> str:
        return "UNSET"


UNSET = _Unset()


def resolve_api_key(api_key: Optional[str] | _Unset = UNSET) -> Optional[str]:
    """Resolve the API key from the explicit parameter or GUNSPEC_API_KEY env var.

    Resolution order:
    1. An explicit ``None`` means anonymous on purpose: no header is sent and
       the environment is not read. This is how a test or a public-only caller
       opts out of a key the shell happens to export.
    2. Explicit non-empty ``api_key`` parameter.
    3. ``GUNSPEC_API_KEY`` environment variable (omitted or empty key).
    4. ``None`` (anonymous / unauthenticated).
    """
    if api_key is None:
        return None
    if not isinstance(api_key, _Unset) and api_key != "":
        return api_key
    return os.environ.get("GUNSPEC_API_KEY") or None


def build_auth_headers(api_key: Optional[str] = None, scheme: AuthScheme = "x-api-key") -> Dict[str, str]:
    """Build the authentication headers for a request.

    Returns ``{"X-API-Key": key}`` (or ``{"Authorization": "Bearer key"}`` for
    the ``bearer`` scheme) when a key is available, or an empty dict for
    anonymous mode.
    """
    if api_key is None or api_key == "":
        return {}
    if scheme == "bearer":
        return {"Authorization": f"Bearer {api_key}"}
    return {"X-API-Key": api_key}


def mask_api_key(api_key: Optional[str]) -> str:
    """Render a key for a log line: first four and last four characters, or
    ``"(none)"``. Short keys are fully masked."""
    if not api_key:
        return "(none)"
    if len(api_key) <= 12:
        return "*" * len(api_key)
    return f"{api_key[:4]}...{api_key[-4:]}"


def assert_transport_security(base_url: str, has_api_key: bool, allow_insecure: bool) -> None:
    """Refuse to send a key over a transport that would expose it.

    A base URL that is not ``https:`` puts the key in every request in the
    clear. Loopback hosts are allowed, because that is how the SDK is pointed
    at a local ``wrangler dev``; anything else needs ``allow_insecure=True``.

    Raises ``ConfigurationError`` on a malformed URL or an insecure remote host.
    """
    parts = urlsplit(base_url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ConfigurationError(f"base_url is not a valid URL: {base_url!r}")
    if parts.scheme == "https" or not has_api_key or allow_insecure:
        return
    if (parts.hostname or "") in _LOOPBACK_HOSTS:
        return
    raise ConfigurationError(
        f"Refusing to send an API key over http:// to {parts.hostname}. "
        "Use an https:// base_url, or pass allow_insecure=True if this is a trusted private network."
    )
