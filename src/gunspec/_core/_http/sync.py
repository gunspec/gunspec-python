"""Synchronous HTTP client over ``httpx.Client``."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Tuple

import httpx

from .._response import (
    APIResponse,
    ConditionalResponse,
    PaginatedResponse,
    RawResponse,
    parse_envelope,
    parse_paginated_envelope,
    raise_api_error,
    response_meta,
)
from .._retry import with_retry
from .base import HttpClientConfig, _BaseHttpClient


class SyncHttpClient(_BaseHttpClient):
    """Synchronous HTTP client using ``httpx.Client``."""

    def __init__(self, config: Optional[HttpClientConfig] = None) -> None:
        super().__init__(config)
        self._client = httpx.Client(
            base_url=self._base_url, headers=self._default_headers, timeout=self._timeout
        )

    # -- Public API ---------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        body: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> APIResponse[Any]:
        """Execute an HTTP request and return the unwrapped response."""

        def _do() -> APIResponse[Any]:
            return self._execute_request(
                method, path, query=query, body=body, headers=headers, timeout=timeout
            )

        return with_retry(_do, method, self._retry)

    def request_paginated(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> PaginatedResponse[Any]:
        """Execute an HTTP request and return a paginated response."""

        def _do() -> PaginatedResponse[Any]:
            return self._execute_paginated_request(
                method, path, query=query, headers=headers, timeout=timeout
            )

        return with_retry(_do, method, self._retry)

    def request_conditional(
        self,
        path: str,
        *,
        if_none_match: str,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ConditionalResponse[Any]:
        """GET with the caller's own ``If-None-Match``, surfacing a 304 instead of a body."""

        def _do() -> ConditionalResponse[Any]:
            response = self._do_fetch(
                "GET", path, query=query, headers=headers, timeout=timeout, if_none_match=if_none_match
            )
            if response.status_code == 304:
                return ConditionalResponse(not_modified=True, data=None, **response_meta(response))
            if not response.is_success:
                raise_api_error(response)
            envelope = parse_envelope(response.text, response.headers.get("Content-Type"))
            return ConditionalResponse(
                not_modified=False, data=envelope.get("data"), **response_meta(response)
            )

        return with_retry(_do, "GET", self._retry)

    def request_raw(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> RawResponse:
        """Execute a request whose body is bytes rather than an envelope."""

        def _do() -> RawResponse:
            response = self._do_fetch(
                method,
                path,
                query=query,
                headers={"Accept": "*/*", **(headers or {})},
                timeout=timeout,
                follow_redirects=True,
            )
            if not response.is_success:
                raise_api_error(response)
            return RawResponse(
                body=response.content,
                content_type=response.headers.get("Content-Type"),
                url=str(response.url),
                **response_meta(response),
            )

        return with_retry(_do, method, self._retry)

    def resolve_redirect(self, path: str, query: Optional[Mapping[str, Any]] = None) -> Optional[str]:
        """Return where a redirecting endpoint points, without following it."""
        response = self._do_fetch("GET", path, query=query, follow_redirects=False)
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location")
            return str(location) if location is not None else None
        if not response.is_success:
            raise_api_error(response)
        return None

    def get(self, path: str, query: Optional[Mapping[str, Any]] = None) -> APIResponse[Any]:
        return self.request("GET", path, query=query)

    def get_paginated(self, path: str, query: Optional[Mapping[str, Any]] = None) -> PaginatedResponse[Any]:
        return self.request_paginated("GET", path, query=query)

    def get_text(self, path: str, query: Optional[Mapping[str, Any]] = None) -> str:
        """GET an endpoint that answers with text (an SVG, a CSV)."""
        return self.request_raw("GET", path, query=query).text()

    def get_bytes(self, path: str, query: Optional[Mapping[str, Any]] = None) -> RawResponse:
        """GET an endpoint that answers with binary content (a GLB, an image)."""
        return self.request_raw("GET", path, query=query)

    def post(
        self, path: str, body: Optional[Any] = None, query: Optional[Mapping[str, Any]] = None
    ) -> APIResponse[Any]:
        return self.request("POST", path, body=body, query=query)

    def put(
        self, path: str, body: Optional[Any] = None, query: Optional[Mapping[str, Any]] = None
    ) -> APIResponse[Any]:
        return self.request("PUT", path, body=body, query=query)

    def patch(
        self, path: str, body: Optional[Any] = None, query: Optional[Mapping[str, Any]] = None
    ) -> APIResponse[Any]:
        return self.request("PATCH", path, body=body, query=query)

    def delete(self, path: str, query: Optional[Mapping[str, Any]] = None) -> APIResponse[Any]:
        return self.request("DELETE", path, query=query)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SyncHttpClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    # -- Internal -----------------------------------------------------------

    def _fetch_with_cache(
        self,
        method: str,
        path: str,
        query: Optional[Mapping[str, Any]],
        body: Optional[Any],
        headers: Optional[Dict[str, str]],
        timeout: Optional[float],
    ) -> Tuple[httpx.Response, str, bool]:
        cacheable, key, held = self._cache_lookup(method, path, query, None)
        response = self._do_fetch(
            method,
            path,
            query=query,
            body=body,
            headers=headers,
            timeout=timeout,
            if_none_match=held.etag if held else None,
        )
        text, from_cache = self._cache_finish(response, cacheable, key, held)
        return response, text, from_cache

    def _execute_request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        body: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> APIResponse[Any]:
        response, text, from_cache = self._fetch_with_cache(method, path, query, body, headers, timeout)
        envelope = parse_envelope(text, response.headers.get("Content-Type"))
        return APIResponse(data=envelope.get("data"), from_cache=from_cache, **response_meta(response))

    def _execute_paginated_request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> PaginatedResponse[Any]:
        response, text, from_cache = self._fetch_with_cache(method, path, query, None, headers, timeout)
        data, pagination, meta = parse_paginated_envelope(text, response.headers.get("Content-Type"))
        return PaginatedResponse(
            data=data, pagination=pagination, meta=meta, from_cache=from_cache, **response_meta(response)
        )

    def _do_fetch(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        body: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        if_none_match: Optional[str] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        req = self._build(method, path, query, body, headers, if_none_match)
        try:
            request = self._client.build_request(timeout=timeout or self._timeout, **req)
            response = self._client.send(request, follow_redirects=False)
            # Redirects are followed here rather than by httpx, so the key
            # never leaves the API's origin (see ``_redirect_request``).
            hops = 0
            while follow_redirects and response.is_redirect:
                request = self._redirect_request(request, response, hops)
                hops += 1
                response.close()
                response = self._client.send(request, follow_redirects=False)
            return response
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            raise self._wrap_transport_error(exc, timeout or self._timeout) from exc
