"""Shared state and pure helpers for the sync and async HTTP clients."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Tuple, Union

import httpx

from ..._version import __version__
from .._auth import (
    UNSET,
    AuthScheme,
    _Unset,
    assert_transport_security,
    build_auth_headers,
    mask_api_key,
    resolve_api_key,
)
from .._errors import ConnectError, GunSpecError, RequestTimeoutError
from .._etag_cache import (
    CachedEntry,
    ETagStore,
    MemoryETagStore,
    cache_key_for,
    credential_fingerprint,
    now,
)
from .._response import (
    raise_api_error,
)
from .._retry import RetryConfig

Query = Optional[Mapping[str, Any]]
"""Query parameters as any mapping, so a TypedDict is accepted without a cast."""

DEFAULT_BASE_URL = "https://api.gunspec.io"
DEFAULT_TIMEOUT = 30.0
SDK_USER_AGENT = f"gunspec-sdk/python/{__version__}"

MAX_REDIRECTS = 5
"""Hops a raw download follows before giving up. The API answers a media or
model request with one redirect to the asset host, so five is generous."""

_AUTH_HEADERS = ("x-api-key", "authorization")
"""Header names that carry the credential, compared lower-case."""

_BODY_HEADERS = ("content-type", "content-length", "transfer-encoding")
_DEFAULT_PORTS = {"http": 80, "https": 443}


@dataclass
class HttpClientConfig:
    """Configuration for the HTTP client."""

    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    headers: Dict[str, str] = field(default_factory=dict)
    api_key: Union[str, _Unset, None] = UNSET
    retry: RetryConfig = field(default_factory=RetryConfig)
    auth_scheme: AuthScheme = "x-api-key"
    etag_cache: Union[bool, ETagStore, None] = None
    allow_insecure: bool = False


def serialize_query(params: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Serialize query parameters for httpx.

    - Skips ``None`` values.
    - Converts booleans to ``"true"``/``"false"`` strings.
    - Lists produce repeated keys via httpx's native handling.
    """
    if params is None:
        return {}

    out: Dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            out[key] = "true" if value else "false"
        else:
            out[key] = value
    return out


def _origin(url: httpx.URL) -> Tuple[str, str, Optional[int]]:
    """Scheme, host and effective port, the triple two URLs must share to be one origin."""
    return (url.scheme, url.host, url.port or _DEFAULT_PORTS.get(url.scheme))


class _BaseHttpClient:
    """State and pure helpers shared by the sync and async clients."""

    def __init__(self, config: Optional[HttpClientConfig] = None) -> None:
        cfg = config or HttpClientConfig()
        self._base_url = cfg.base_url.rstrip("/")
        self._timeout = cfg.timeout
        self._api_key = resolve_api_key(cfg.api_key)
        self._auth_scheme: AuthScheme = cfg.auth_scheme
        self._retry = cfg.retry
        self._allow_insecure = cfg.allow_insecure
        # Checked by identity, not truth: an empty store has ``__len__`` 0 and
        # would otherwise read as "no cache".
        self._store: Optional[ETagStore] = (
            MemoryETagStore()
            if cfg.etag_cache is True
            else None
            if cfg.etag_cache is None or cfg.etag_cache is False
            else cfg.etag_cache
        )
        self._fingerprint = credential_fingerprint(self._api_key)

        # A key passed through ``headers`` travels exactly like one passed as
        # ``api_key``, so it has to pass the same transport check.
        header_auth = any(k.lower() in _AUTH_HEADERS and v for k, v in cfg.headers.items())
        assert_transport_security(
            self._base_url, self._api_key is not None or header_auth, cfg.allow_insecure
        )
        self._base_origin = _origin(httpx.URL(self._base_url))

        self._default_headers = {
            "Accept": "application/json",
            "User-Agent": SDK_USER_AGENT,
            **cfg.headers,
            **build_auth_headers(self._api_key, self._auth_scheme),
        }

    @property
    def is_authenticated(self) -> bool:
        """Whether a credential will be sent. The key itself is never exposed."""
        return self._api_key is not None

    def url_for(self, path: str, query: Optional[Mapping[str, Any]] = None) -> str:
        """Absolute URL for a path, for links the caller renders rather than fetches."""
        params = serialize_query(query)
        url = httpx.URL(self._base_url + path)
        return str(url.copy_merge_params(params)) if params else str(url)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(base_url={self._base_url!r}, "
            f"api_key={mask_api_key(self._api_key)!r}, auth_scheme={self._auth_scheme!r}, "
            f"etag_cache={self._store is not None})"
        )

    # -- Request assembly ----------------------------------------------------

    def _build(
        self,
        method: str,
        path: str,
        query: Optional[Mapping[str, Any]],
        body: Optional[Any],
        headers: Optional[Dict[str, str]],
        if_none_match: Optional[str],
    ) -> Dict[str, Any]:
        req_headers: Dict[str, str] = dict(headers or {})
        if body is not None:
            req_headers["Content-Type"] = "application/json"
        if if_none_match is not None:
            req_headers["If-None-Match"] = if_none_match
        params = serialize_query(query)
        return {
            "method": method,
            "url": path,
            "params": params or None,
            "json": body,
            "headers": req_headers or None,
        }

    def _cache_lookup(
        self, method: str, path: str, query: Optional[Mapping[str, Any]], if_none_match: Optional[str]
    ) -> Tuple[bool, str, Optional[CachedEntry]]:
        cacheable = self._store is not None and method == "GET" and if_none_match is None
        key = cache_key_for(self._fingerprint, self.url_for(path, query))
        held = self._store.get(key) if cacheable and self._store is not None else None
        return cacheable, key, held

    def _cache_finish(
        self, response: httpx.Response, cacheable: bool, key: str, held: Optional[CachedEntry]
    ) -> Tuple[str, bool]:
        """Return ``(body_text, from_cache)``, storing a fresh tagged body."""
        if response.status_code == 304 and held is not None:
            return held.body, True
        if not response.is_success:
            raise_api_error(response)
        text = response.text
        etag = response.headers.get("ETag")
        if cacheable and etag and self._store is not None:
            self._store.set(key, CachedEntry(etag=etag, body=text, stored_at=now()))
        return text, False

    def _redirect_request(self, request: httpx.Request, response: httpx.Response, hops: int) -> httpx.Request:
        """The request for the next hop of a redirect the SDK follows by hand.

        httpx would follow it too, but it only drops ``Authorization`` on a
        cross-origin hop and keeps ``X-API-Key``, so a redirect to an asset
        host (or anywhere a compromised or misconfigured edge points) would
        receive the key. Here both credential headers go only to the origin
        of ``base_url``, and a hop from https down to http is refused
        outright, because it would put every header in the clear.

        Raises ``GunSpecError`` past ``MAX_REDIRECTS`` hops, on a downgrade
        to http, and on a ``Location`` that is not an http(s) URL.
        """
        if hops >= MAX_REDIRECTS:
            raise GunSpecError(f"Stopped after {MAX_REDIRECTS} redirects from {request.url}")
        url = request.url.join(response.headers["Location"])
        if url.scheme not in ("http", "https") or not url.host:
            raise GunSpecError(f"Refusing to follow a redirect to {url}: not an http(s) URL")
        if request.url.scheme == "https" and url.scheme == "http":
            raise GunSpecError(
                f"Refusing to follow a redirect from https to http ({url}): "
                "it would send the request in the clear"
            )

        method = request.method
        status = response.status_code
        # The same method rewrite browsers and httpx apply: a 303 always turns
        # into a GET, and so do 301 and 302 after a POST.
        rewrite = (status == 303 and method != "HEAD") or (status in (301, 302) and method == "POST")
        headers = httpx.Headers(request.headers)
        headers.pop("Host", None)
        if rewrite:
            method = "GET"
            for name in _BODY_HEADERS:
                headers.pop(name, None)
        if _origin(url) != self._base_origin:
            for name in _AUTH_HEADERS:
                headers.pop(name, None)
        return httpx.Request(
            method,
            url,
            headers=headers,
            content=None if rewrite else request.content,
            extensions=request.extensions,
        )

    @staticmethod
    def _wrap_transport_error(exc: Exception, timeout: float) -> Exception:
        if isinstance(exc, httpx.TimeoutException):
            return RequestTimeoutError(timeout)
        if isinstance(exc, httpx.ConnectError):
            return ConnectError(str(exc), exc)
        return exc
