from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import PaginationParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Categories:
    """Sync categories resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/categories")

    def get_firearms(
        self, slug: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated(f"/v1/categories/{_seg(slug)}/firearms", query=params)


class AsyncCategories:
    """Async categories resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/categories")

    async def get_firearms(
        self, slug: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(f"/v1/categories/{_seg(slug)}/firearms", query=params)
