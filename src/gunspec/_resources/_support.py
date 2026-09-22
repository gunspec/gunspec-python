from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import CreateReplyParams, CreateTicketParams, ListTicketsParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Support:
    """Sync support resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def create(self, params: CreateTicketParams) -> APIResponse[Dict[str, Any]]:
        return self._client.post("/v1/me/support", body=params)

    def list(self, params: Optional[ListTicketsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/me/support", query=params)

    def get(self, ticket_id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/me/support/{_seg(ticket_id)}")

    def reply(self, ticket_id: str, params: CreateReplyParams) -> APIResponse[Dict[str, Any]]:
        return self._client.post(f"/v1/me/support/{_seg(ticket_id)}/replies", body=params)


class AsyncSupport:
    """Async support resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: CreateTicketParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.post("/v1/me/support", body=params)

    async def list(self, params: Optional[ListTicketsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/me/support", query=params)

    async def get(self, ticket_id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/me/support/{_seg(ticket_id)}")

    async def reply(self, ticket_id: str, params: CreateReplyParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.post(f"/v1/me/support/{_seg(ticket_id)}/replies", body=params)
