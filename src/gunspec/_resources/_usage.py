from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import UsageParams

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, SyncHttpClient


class Usage:
    """Sync usage resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get(self, params: Optional[UsageParams] = None) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/me/usage", query=params)


class AsyncUsage:
    """Async usage resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get(self, params: Optional[UsageParams] = None) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/me/usage", query=params)
