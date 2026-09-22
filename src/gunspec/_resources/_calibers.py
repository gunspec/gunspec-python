from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, List, Optional

from ..types import CaliberBallisticsParams, CompareCalibersParams, ListCalibersParams, PaginationParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Calibers:
    """Sync calibers resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListCalibersParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/calibers", query=params)

    def list_auto_paging(self, params: Optional[ListCalibersParams] = None) -> Iterator[Dict[str, Any]]:
        page = (params or {}).get("page", 1)
        while True:
            query: Dict[str, Any] = dict(params or {})
            query["page"] = page
            result = self.list(query)  # type: ignore[arg-type]
            yield from result.data
            if not result.pagination.total_pages or page >= result.pagination.total_pages:
                break
            page += 1

    def compare(self, params: CompareCalibersParams) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/calibers/compare", query=params)

    def ballistics(self, params: CaliberBallisticsParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/calibers/ballistics", query=params)

    def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/calibers/{_seg(id)}")

    def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated(f"/v1/calibers/{_seg(id)}/firearms", query=params)

    def get_parent_chain(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/calibers/{_seg(id)}/parent-chain")

    def get_family(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/calibers/{_seg(id)}/family")

    def get_ammunition(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated(f"/v1/calibers/{_seg(id)}/ammunition", query=params)


class AsyncCalibers:
    """Async calibers resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self, params: Optional[ListCalibersParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/calibers", query=params)

    async def list_auto_paging(
        self, params: Optional[ListCalibersParams] = None
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

    async def compare(self, params: CompareCalibersParams) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/calibers/compare", query=params)

    async def ballistics(self, params: CaliberBallisticsParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/calibers/ballistics", query=params)

    async def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/calibers/{_seg(id)}")

    async def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(f"/v1/calibers/{_seg(id)}/firearms", query=params)

    async def get_parent_chain(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/calibers/{_seg(id)}/parent-chain")

    async def get_family(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/calibers/{_seg(id)}/family")

    async def get_ammunition(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(f"/v1/calibers/{_seg(id)}/ammunition", query=params)
