"""Redirects on raw downloads, and credentials passed as default headers.

httpx drops ``Authorization`` on a cross-origin redirect but keeps
``X-API-Key``, so the SDK follows redirects itself. These tests pin what
reaches the next hop on both clients.
"""

from __future__ import annotations

from typing import Any, Callable, Union

import httpx
import pytest
import respx

from gunspec._core._errors import ConfigurationError, GunSpecError
from gunspec._core._http.base import MAX_REDIRECTS
from gunspec._core._http_client import AsyncHttpClient, HttpClientConfig, SyncHttpClient
from gunspec._core._retry import RetryConfig

BASE = "https://api.gunspec.io"
KEY = "gsk_redirect_test"
NO_RETRY = RetryConfig(max_retries=0)


def _cfg(**kw: Any) -> HttpClientConfig:
    cfg = HttpClientConfig(base_url=BASE, api_key=KEY, retry=NO_RETRY)
    for k, v in kw.items():
        setattr(cfg, k, v)
    return cfg


def _redirect(to: str, status: int = 302) -> httpx.Response:
    return httpx.Response(status, headers={"Location": to})


def _asset() -> httpx.Response:
    return httpx.Response(200, content=b"\x01", headers={"Content-Type": "model/gltf-binary"})


Client = Union[SyncHttpClient, AsyncHttpClient]


async def _get_bytes(client: Client, path: str) -> Any:
    if isinstance(client, AsyncHttpClient):
        try:
            return await client.get_bytes(path)
        finally:
            await client.aclose()
    try:
        return client.get_bytes(path)
    finally:
        client.close()


Factory = Callable[..., Client]
FACTORIES = [
    pytest.param(lambda **kw: SyncHttpClient(_cfg(**kw)), id="sync"),
    pytest.param(lambda **kw: AsyncHttpClient(_cfg(**kw)), id="async"),
]


@pytest.mark.parametrize("make", FACTORIES)
class TestManualRedirects:
    @respx.mock
    async def test_cross_origin_hop_carries_no_credential(self, make: Factory) -> None:
        respx.get(f"{BASE}/v1/firearms/x/model").mock(return_value=_redirect("https://cdn.example/x.glb"))
        cdn = respx.get("https://cdn.example/x.glb").mock(return_value=_asset())
        raw = await _get_bytes(make(), "/v1/firearms/x/model")
        assert raw.body == b"\x01" and raw.url == "https://cdn.example/x.glb"
        sent = cdn.calls[0].request.headers
        assert "x-api-key" not in sent and "authorization" not in sent
        assert sent["host"] == "cdn.example"

    @respx.mock
    async def test_cross_origin_hop_drops_bearer_too(self, make: Factory) -> None:
        respx.get(f"{BASE}/v1/firearms/x/model").mock(return_value=_redirect("https://cdn.example/x.glb"))
        cdn = respx.get("https://cdn.example/x.glb").mock(return_value=_asset())
        await _get_bytes(make(auth_scheme="bearer"), "/v1/firearms/x/model")
        assert "authorization" not in cdn.calls[0].request.headers

    @respx.mock
    async def test_same_origin_hop_keeps_the_credential(self, make: Factory) -> None:
        respx.get(f"{BASE}/v1/firearms/x/model").mock(return_value=_redirect("/v1/firearms/x/model.glb"))
        final = respx.get(f"{BASE}/v1/firearms/x/model.glb").mock(return_value=_asset())
        raw = await _get_bytes(make(), "/v1/firearms/x/model")
        assert raw.url == f"{BASE}/v1/firearms/x/model.glb"
        assert final.calls[0].request.headers["x-api-key"] == KEY

    @respx.mock
    async def test_other_port_is_another_origin(self, make: Factory) -> None:
        respx.get(f"{BASE}/v1/x").mock(return_value=_redirect("https://api.gunspec.io:8443/x"))
        other = respx.get("https://api.gunspec.io:8443/x").mock(return_value=_asset())
        await _get_bytes(make(), "/v1/x")
        assert "x-api-key" not in other.calls[0].request.headers

    @respx.mock
    async def test_https_to_http_is_refused(self, make: Factory) -> None:
        respx.get(f"{BASE}/v1/x").mock(return_value=_redirect("http://cdn.example/x.glb"))
        plain = respx.get("http://cdn.example/x.glb").mock(return_value=_asset())
        with pytest.raises(GunSpecError, match="https to http"):
            await _get_bytes(make(), "/v1/x")
        assert not plain.called

    @respx.mock
    async def test_stops_after_the_hop_limit(self, make: Factory) -> None:
        loop = respx.get(url__regex=rf"{BASE}/v1/loop/\d+")
        loop.side_effect = lambda request: _redirect(
            f"/v1/loop/{int(request.url.path.rsplit('/', 1)[1]) + 1}"
        )
        with pytest.raises(GunSpecError, match=f"{MAX_REDIRECTS} redirects"):
            await _get_bytes(make(), "/v1/loop/0")
        assert loop.call_count == MAX_REDIRECTS + 1

    @respx.mock
    async def test_follows_up_to_the_hop_limit(self, make: Factory) -> None:
        for i in range(MAX_REDIRECTS):
            respx.get(f"{BASE}/v1/hop/{i}").mock(return_value=_redirect(f"/v1/hop/{i + 1}"))
        respx.get(f"{BASE}/v1/hop/{MAX_REDIRECTS}").mock(return_value=_asset())
        raw = await _get_bytes(make(), "/v1/hop/0")
        assert raw.body == b"\x01"


class TestDefaultHeaderCredential:
    @pytest.mark.parametrize("name", ["X-API-Key", "x-api-key", "Authorization", "AUTHORIZATION"])
    def test_key_in_default_headers_is_checked_over_http(self, name: str) -> None:
        cfg = HttpClientConfig(base_url="http://api.example", api_key=None, headers={name: "gsk_x"})
        with pytest.raises(ConfigurationError, match="http://"):
            SyncHttpClient(cfg)

    def test_anonymous_http_without_auth_headers_is_allowed(self) -> None:
        cfg = HttpClientConfig(base_url="http://api.example", api_key=None, headers={"X-Trace": "1"})
        SyncHttpClient(cfg).close()

    def test_allow_insecure_still_opts_in(self) -> None:
        cfg = HttpClientConfig(
            base_url="http://api.example", api_key=None, headers={"X-API-Key": "k"}, allow_insecure=True
        )
        SyncHttpClient(cfg).close()

    @respx.mock
    def test_header_credential_is_dropped_on_cross_origin_hop(self) -> None:
        respx.get(f"{BASE}/v1/x").mock(return_value=_redirect("https://cdn.example/x"))
        cdn = respx.get("https://cdn.example/x").mock(return_value=_asset())
        client = SyncHttpClient(_cfg(api_key=None, headers={"x-api-key": "gsk_h"}))
        try:
            client.get_bytes("/v1/x")
        finally:
            client.close()
        assert "x-api-key" not in cdn.calls[0].request.headers
