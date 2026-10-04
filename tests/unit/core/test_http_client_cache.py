"""Tests for the ETag cache, conditional and raw requests, auth scheme,
transport security and the retry policy on the sync and async clients."""

from __future__ import annotations

import httpx
import pytest
import respx

from gunspec._core._errors import (
    ConfigurationError,
    GunSpecError,
    RateLimitError,
    ServiceUnavailableError,
)
from gunspec._core._etag_cache import MemoryETagStore
from gunspec._core._http_client import AsyncHttpClient, HttpClientConfig, SyncHttpClient
from gunspec._core._retry import RetryConfig

BASE = "https://api.gunspec.io"
NO_RETRY = RetryConfig(max_retries=0)


def _client(**kw: object) -> SyncHttpClient:
    cfg = HttpClientConfig(base_url=BASE, api_key="gsk_test", retry=NO_RETRY)
    for k, v in kw.items():
        setattr(cfg, k, v)
    return SyncHttpClient(cfg)


def _ok(data: object, headers: dict | None = None) -> httpx.Response:
    return httpx.Response(
        200, json={"success": True, "data": data}, headers={"X-Request-Id": "r1", **(headers or {})}
    )


class TestETagCache:
    @respx.mock
    def test_stores_then_sends_if_none_match_and_serves_304_from_cache(self) -> None:
        route = respx.get(f"{BASE}/v1/firearms/ak-47").mock(
            side_effect=[_ok({"v": 1}, {"ETag": '"abc"'}), httpx.Response(304, headers={"ETag": '"abc"'})]
        )
        client = _client(etag_cache=True)
        try:
            first = client.get("/v1/firearms/ak-47")
            assert first.etag == '"abc"' and first.from_cache is False
            assert "if-none-match" not in route.calls[0].request.headers
            second = client.get("/v1/firearms/ak-47")
            assert route.calls[1].request.headers["if-none-match"] == '"abc"'
            assert second.status == 304 and second.from_cache is True
            assert second.data == {"v": 1}
        finally:
            client.close()

    @respx.mock
    def test_replaces_held_body_on_new_tag(self) -> None:
        respx.get(f"{BASE}/v1/x").mock(side_effect=[_ok(1, {"ETag": '"1"'}), _ok(2, {"ETag": '"2"'})])
        store = MemoryETagStore()
        client = _client(etag_cache=store)
        try:
            client.get("/v1/x")
            res = client.get("/v1/x")
            assert res.data == 2 and res.from_cache is False
            assert len(store) == 1
        finally:
            client.close()

    @respx.mock
    def test_no_etag_and_non_get_are_not_cached(self) -> None:
        respx.get(f"{BASE}/v1/x").mock(return_value=_ok(1))
        respx.post(f"{BASE}/v1/x").mock(return_value=_ok(1, {"ETag": '"p"'}))
        store = MemoryETagStore()
        client = _client(etag_cache=store)
        try:
            client.get("/v1/x")
            client.post("/v1/x", body={})
            assert len(store) == 0
        finally:
            client.close()

    @respx.mock
    def test_two_keys_do_not_share_a_body(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            side_effect=[_ok("paid", {"ETag": '"t"'}), _ok("free", {"ETag": '"t"'})]
        )
        store = MemoryETagStore()
        a = _client(etag_cache=store, api_key="gsk_a")
        b = _client(etag_cache=store, api_key="gsk_b")
        try:
            a.get("/v1/x")
            b.get("/v1/x")
            assert "if-none-match" not in route.calls[1].request.headers
            assert len(store) == 2
        finally:
            a.close()
            b.close()

    @respx.mock
    def test_paginated_keeps_meta_and_per_page(self) -> None:
        page = {
            "success": True,
            "data": [1],
            "pagination": {"page": 1, "limit": 20, "per_page": 20},
            "meta": {"fp": "f"},
        }
        respx.get(f"{BASE}/v1/list").mock(
            side_effect=[
                httpx.Response(200, json=page, headers={"ETag": '"p"'}),
                httpx.Response(304, headers={"ETag": '"p"'}),
            ]
        )
        client = _client(etag_cache=True)
        try:
            first = client.get_paginated("/v1/list")
            assert first.meta == {"fp": "f"}
            second = client.get_paginated("/v1/list")
            assert second.from_cache and second.data == [1] and second.pagination.per_page == 20
        finally:
            client.close()

    @respx.mock
    async def test_async_client_caches_too(self) -> None:
        respx.get(f"{BASE}/v1/x").mock(
            side_effect=[_ok(1, {"ETag": '"a"'}), httpx.Response(304, headers={"ETag": '"a"'})]
        )
        cfg = HttpClientConfig(base_url=BASE, api_key="gsk_test", retry=NO_RETRY, etag_cache=True)
        client = AsyncHttpClient(cfg)
        try:
            await client.get("/v1/x")
            second = await client.get("/v1/x")
            assert second.from_cache and second.data == 1
        finally:
            await client.aclose()


class TestConditional:
    @respx.mock
    def test_surfaces_304_for_a_held_tag(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(304, headers={"ETag": '"z"', "Cache-Control": "public, max-age=300"})
        )
        client = _client()
        try:
            res = client.request_conditional("/v1/x", if_none_match='"z"')
            assert route.calls[0].request.headers["if-none-match"] == '"z"'
            assert res.not_modified and res.data is None
            assert res.etag == '"z"' and res.cache_control == "public, max-age=300"
        finally:
            client.close()

    @respx.mock
    def test_returns_body_when_tag_changed(self) -> None:
        respx.get(f"{BASE}/v1/x").mock(return_value=_ok("new", {"ETag": '"y"'}))
        client = _client()
        try:
            res = client.request_conditional("/v1/x", if_none_match='"z"')
            assert not res.not_modified and res.data == "new"
        finally:
            client.close()


class TestRaw:
    @respx.mock
    def test_get_text_reads_svg(self) -> None:
        route = respx.get(f"{BASE}/v1/ammunition/x/bullet.svg").mock(
            return_value=httpx.Response(200, text="<svg/>", headers={"Content-Type": "image/svg+xml"})
        )
        client = _client()
        try:
            assert client.get_text("/v1/ammunition/x/bullet.svg") == "<svg/>"
            assert route.calls[0].request.headers["accept"] == "*/*"
        finally:
            client.close()

    @respx.mock
    def test_get_bytes_follows_redirect_to_cdn(self) -> None:
        respx.get(f"{BASE}/v1/firearms/x/model").mock(
            return_value=httpx.Response(302, headers={"Location": "https://cdn.example/x.glb"})
        )
        respx.get("https://cdn.example/x.glb").mock(
            return_value=httpx.Response(
                200, content=b"\x01\x02", headers={"Content-Type": "model/gltf-binary"}
            )
        )
        client = _client()
        try:
            raw = client.get_bytes("/v1/firearms/x/model")
            assert raw.body == b"\x01\x02" and raw.content_type == "model/gltf-binary"
            assert raw.url == "https://cdn.example/x.glb"
        finally:
            client.close()

    @respx.mock
    def test_binary_read_as_json_names_the_right_method(self) -> None:
        respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(200, text="<svg/>", headers={"Content-Type": "image/svg+xml"})
        )
        client = _client()
        try:
            with pytest.raises(GunSpecError, match=r"get_text\(\) or get_bytes\(\)"):
                client.get("/v1/x")
        finally:
            client.close()

    @respx.mock
    def test_resolve_redirect_does_not_follow(self) -> None:
        respx.get(f"{BASE}/v1/out/abc").mock(
            return_value=httpx.Response(302, headers={"Location": "https://shop.example/x"})
        )
        client = _client()
        try:
            assert client.resolve_redirect("/v1/out/abc") == "https://shop.example/x"
        finally:
            client.close()


class TestAuthScheme:
    @respx.mock
    def test_x_api_key_by_default_and_bearer_on_request(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(return_value=_ok(None))
        a = _client()
        b = _client(auth_scheme="bearer")
        try:
            a.get("/v1/x")
            assert route.calls[0].request.headers["x-api-key"] == "gsk_test"
            assert "authorization" not in route.calls[0].request.headers
            b.get("/v1/x")
            assert route.calls[1].request.headers["authorization"] == "Bearer gsk_test"
            assert "x-api-key" not in route.calls[1].request.headers
        finally:
            a.close()
            b.close()

    def test_repr_masks_the_key(self) -> None:
        client = _client(api_key="gsk_72ee457ac9ccc5b2b5bc788f5269feca")
        try:
            printed = repr(client)
            assert "gsk_72ee457ac9ccc5b2b5bc788f5269feca" not in printed
            assert "gsk_...feca" in printed
            assert client.is_authenticated
        finally:
            client.close()

    @respx.mock
    def test_explicit_none_is_anonymous(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GUNSPEC_API_KEY", "gs_env")
        route = respx.get(f"{BASE}/v1/x").mock(return_value=_ok(None))
        client = SyncHttpClient(HttpClientConfig(base_url=BASE, api_key=None, retry=NO_RETRY))
        try:
            client.get("/v1/x")
            assert "x-api-key" not in route.calls[0].request.headers
            assert not client.is_authenticated
        finally:
            client.close()


class TestTransportSecurity:
    def test_refuses_key_over_http_to_remote(self) -> None:
        with pytest.raises(ConfigurationError):
            _client(base_url="http://api.example.com")

    def test_allows_loopback_override_and_keyless(self) -> None:
        _client(base_url="http://localhost:8788").close()
        _client(base_url="http://127.0.0.1:8788").close()
        _client(base_url="http://api.example.com", allow_insecure=True).close()
        SyncHttpClient(HttpClientConfig(base_url="http://api.example.com", api_key=None)).close()

    def test_refuses_non_url(self) -> None:
        with pytest.raises(ConfigurationError):
            _client(base_url="not a url")


class TestRetryPolicy:
    @respx.mock
    def test_daily_cap_is_not_retried_when_its_reset_is_beyond_max_retry_after(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(
                429,
                json={
                    "success": False,
                    "error": {"code": "DAILY_CAP_EXCEEDED", "reason": "DAILY_CAP_EXCEEDED", "message": "x"},
                },
                headers={"Retry-After": "600"},
            )
        )
        client = _client(retry=RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with pytest.raises(RateLimitError) as exc:
                client.get("/v1/x")
            assert exc.value.is_daily_cap
            assert route.call_count == 1
        finally:
            client.close()

    @respx.mock
    def test_long_retry_after_is_raised_not_slept(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(
                503,
                json={
                    "success": False,
                    "error": {"code": "SERVICE_UNAVAILABLE", "reason": "MAINTENANCE", "message": "x"},
                },
                headers={"Retry-After": "600"},
            )
        )
        client = _client(retry=RetryConfig(max_retries=3, initial_delay_s=0.001, max_retry_after_s=1.0))
        try:
            with pytest.raises(ServiceUnavailableError):
                client.get("/v1/x")
            assert route.call_count == 1
        finally:
            client.close()

    @respx.mock
    def test_short_retry_after_on_503_is_retried(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            side_effect=[
                httpx.Response(
                    503,
                    json={"success": False, "error": {"code": "SERVICE_UNAVAILABLE", "message": "x"}},
                    headers={"Retry-After": "0"},
                ),
                _ok("ok"),
            ]
        )
        client = _client(retry=RetryConfig(max_retries=1, initial_delay_s=0.001))
        try:
            assert client.get("/v1/x").data == "ok"
            assert route.call_count == 2
        finally:
            client.close()
