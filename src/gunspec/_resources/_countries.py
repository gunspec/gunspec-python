from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, SyncHttpClient


class Countries:
    """Sync countries resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/countries")

    def get_arsenal(self, code: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/countries/{_seg(code)}/arsenal")


class AsyncCountries:
    """Async countries resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/countries")

    async def get_arsenal(self, code: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/countries/{_seg(code)}/arsenal")
