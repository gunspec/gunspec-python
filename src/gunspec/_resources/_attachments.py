from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, List, Optional
from urllib.parse import quote

from ..types import ListAttachmentsParams, OffersParams, PaginationParams

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Attachments:
    """Sync attachments resource.

    Browsing the catalog is open on the same terms as ``/v1/firearms``;
    computing fit (``fits=`` on the list, ``get_firearms``) is Studio.
    """

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListAttachmentsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/attachments", query=params)

    def list_auto_paging(self, params: Optional[ListAttachmentsParams] = None) -> Iterator[Dict[str, Any]]:
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
        return self._client.get(f"/v1/attachments/{quote(id, safe='')}")

    def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        """Firearms an attachment fits, with how each fit was reached. Studio."""
        return self._client.get_paginated(f"/v1/attachments/{quote(id, safe='')}/firearms", query=params)

    def get_offers(self, id: str, params: Optional[OffersParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        """Sellers stocking this attachment. Link out through ``vendor.click_url``."""
        return self._client.get(f"/v1/attachments/{quote(id, safe='')}/offers", query=params)


class AsyncAttachments:
    """Async attachments resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self, params: Optional[ListAttachmentsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/attachments", query=params)

    async def list_auto_paging(
        self, params: Optional[ListAttachmentsParams] = None
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
        return await self._client.get(f"/v1/attachments/{quote(id, safe='')}")

    async def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(
            f"/v1/attachments/{quote(id, safe='')}/firearms", query=params
        )

    async def get_offers(
        self, id: str, params: Optional[OffersParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/attachments/{quote(id, safe='')}/offers", query=params)
