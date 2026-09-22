from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional
from urllib.parse import quote

from ..types import ListFavoritesParams

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Favorites:
    """Sync favorites resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListFavoritesParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/me/favorites", query=params)

    def list_ids(self) -> APIResponse[Dict[str, Any]]:
        """``data`` is ``{"ids": [...]}``, not a bare list. See ``FavoriteIds``."""
        return self._client.get("/v1/me/favorites/ids")

    def add(self, firearm_id: str) -> APIResponse[Dict[str, Any]]:
        """Idempotent add; ``data`` is ``{"firearmId", "favorited": True}``."""
        return self._client.post(f"/v1/me/favorites/{quote(firearm_id, safe='')}")

    def remove(self, firearm_id: str) -> APIResponse[Dict[str, Any]]:
        """``data`` is ``{"firearmId", "favorited": False}``."""
        return self._client.delete(f"/v1/me/favorites/{quote(firearm_id, safe='')}")


class AsyncFavorites:
    """Async favorites resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self, params: Optional[ListFavoritesParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/me/favorites", query=params)

    async def list_ids(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/me/favorites/ids")

    async def add(self, firearm_id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.post(f"/v1/me/favorites/{quote(firearm_id, safe='')}")

    async def remove(self, firearm_id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.delete(f"/v1/me/favorites/{quote(firearm_id, safe='')}")
