from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import ConfidenceParams

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class DataQuality:
    """Sync data quality resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def coverage(self) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/data/coverage")

    def confidence(self, params: Optional[ConfidenceParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/data/confidence", query=params)


class AsyncDataQuality:
    """Async data quality resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def coverage(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/data/coverage")

    async def confidence(
        self, params: Optional[ConfidenceParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/data/confidence", query=params)
