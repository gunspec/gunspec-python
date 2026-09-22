from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, Optional

from ..types import AmmunitionBallisticsParams, ListAmmunitionParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Ammunition:
    """Sync ammunition resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListAmmunitionParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/ammunition", query=params)

    def list_auto_paging(self, params: Optional[ListAmmunitionParams] = None) -> Iterator[Dict[str, Any]]:
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
        return self._client.get(f"/v1/ammunition/{_seg(id)}")

    def get_bullet_svg(self, id: str) -> str:
        """The bullet profile as an SVG string. Not an envelope: read as text.

        @endpoint GET /v1/ammunition/{id}/bullet.svg
        """
        return self._client.get_text(f"/v1/ammunition/{_seg(id)}/bullet.svg")

    def ballistics(
        self, id: str, params: Optional[AmmunitionBallisticsParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/ammunition/{_seg(id)}/ballistics", query=params)


class AsyncAmmunition:
    """Async ammunition resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self, params: Optional[ListAmmunitionParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/ammunition", query=params)

    async def list_auto_paging(
        self, params: Optional[ListAmmunitionParams] = None
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
        return await self._client.get(f"/v1/ammunition/{_seg(id)}")

    async def get_bullet_svg(self, id: str) -> str:
        """The bullet profile as an SVG string. Not an envelope: read as text."""
        return await self._client.get_text(f"/v1/ammunition/{_seg(id)}/bullet.svg")

    async def ballistics(
        self, id: str, params: Optional[AmmunitionBallisticsParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/ammunition/{_seg(id)}/ballistics", query=params)
