from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import CreateWebhookEndpointParams, ListWebhookEndpointsParams, UpdateWebhookEndpointParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Webhooks:
    """Sync webhooks resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListWebhookEndpointsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/me/webhooks", query=params)

    def create(self, params: CreateWebhookEndpointParams) -> APIResponse[Dict[str, Any]]:
        return self._client.post("/v1/me/webhooks", body=params)

    def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/me/webhooks/{_seg(id)}")

    def update(self, id: str, params: UpdateWebhookEndpointParams) -> APIResponse[Dict[str, Any]]:
        return self._client.put(f"/v1/me/webhooks/{_seg(id)}", body=params)

    def delete(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.delete(f"/v1/me/webhooks/{_seg(id)}")

    def test(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.post(f"/v1/me/webhooks/{_seg(id)}/test")


class AsyncWebhooks:
    """Async webhooks resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(
        self, params: Optional[ListWebhookEndpointsParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/me/webhooks", query=params)

    async def create(self, params: CreateWebhookEndpointParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.post("/v1/me/webhooks", body=params)

    async def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/me/webhooks/{_seg(id)}")

    async def update(self, id: str, params: UpdateWebhookEndpointParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.put(f"/v1/me/webhooks/{_seg(id)}", body=params)

    async def delete(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.delete(f"/v1/me/webhooks/{_seg(id)}")

    async def test(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.post(f"/v1/me/webhooks/{_seg(id)}/test")
