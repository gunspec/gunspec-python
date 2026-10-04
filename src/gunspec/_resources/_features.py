from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from .._core._http_client import AsyncHttpClient, PaginatedResponse, SyncHttpClient


def _icon_query(q: Optional[str], page: Optional[int], per_page: Optional[int]) -> Dict[str, Any]:
    return {k: v for k, v in {"q": q, "page": page, "per_page": per_page}.items() if v is not None}


class Features:
    """Sync features resource: the drawn icon for each firearm feature."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list_icons(
        self, q: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List the drawn feature icons, a page at a time. On every plan.

        ``q`` narrows to icons whose name contains it; spaces and hyphens read
        as underscores. A single firearm's icons are ``feature_icon`` items in
        ``client.firearms.list_media(id)``.
        """
        return self._client.get_paginated("/v1/features/icons", query=_icon_query(q, page, per_page))


class AsyncFeatures:
    """Async features resource: the drawn icon for each firearm feature."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list_icons(
        self, q: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List the drawn feature icons, a page at a time. On every plan."""
        return await self._client.get_paginated("/v1/features/icons", query=_icon_query(q, page, per_page))
