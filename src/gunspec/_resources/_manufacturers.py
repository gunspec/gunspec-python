from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, Optional

from ..types import ListManufacturersParams, PaginationParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Manufacturers:
    """Sync manufacturers resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListManufacturersParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/manufacturers", query=params)

    def list_auto_paging(self, params: Optional[ListManufacturersParams] = None) -> Iterator[Dict[str, Any]]:
        page = (params or {}).get("page", 1)
        while True:
            query: Dict[str, Any] = dict(params or {})
            query["page"] = page
            result = self.list(query)  # type: ignore[arg-type]
            yield from result.data
            if not result.pagination.total_pages or page >= result.pagination.total_pages:
                break
            page += 1

    def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/manufacturers/{_seg(id)}")

    def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated(f"/v1/manufacturers/{_seg(id)}/firearms", query=params)

    def get_timeline(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/manufacturers/{_seg(id)}/timeline")

    def get_stats(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/manufacturers/{_seg(id)}/stats")


class AsyncManufacturers:
    """Async manufacturers resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(
        self, params: Optional[ListManufacturersParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/manufacturers", query=params)

    async def list_auto_paging(
        self, params: Optional[ListManufacturersParams] = None
    ) -> AsyncIterator[Dict[str, Any]]:
        page = (params or {}).get("page", 1)
        while True:
            query: Dict[str, Any] = dict(params or {})
            query["page"] = page
            result = await self.list(query)  # type: ignore[arg-type]
            for item in result.data:
                yield item
            if not result.pagination.total_pages or page >= result.pagination.total_pages:
                break
            page += 1

    async def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/manufacturers/{_seg(id)}")

    async def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(f"/v1/manufacturers/{_seg(id)}/firearms", query=params)

    async def get_timeline(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/manufacturers/{_seg(id)}/timeline")

    async def get_stats(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/manufacturers/{_seg(id)}/stats")
