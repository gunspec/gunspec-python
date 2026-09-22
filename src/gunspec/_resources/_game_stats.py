from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import ListSnapshotFirearmsParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class GameStats_:
    """Sync game stats snapshots resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list_versions(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/game-stats/versions")

    def list_firearms(
        self, version: str, params: Optional[ListSnapshotFirearmsParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated(f"/v1/game-stats/versions/{_seg(version)}/firearms", query=params)

    def get_firearm(self, version: str, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/game-stats/versions/{_seg(version)}/firearms/{_seg(id)}")


class AsyncGameStats_:
    """Async game stats snapshots resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list_versions(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/game-stats/versions")

    async def list_firearms(
        self, version: str, params: Optional[ListSnapshotFirearmsParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(
            f"/v1/game-stats/versions/{_seg(version)}/firearms", query=params
        )

    async def get_firearm(self, version: str, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/game-stats/versions/{_seg(version)}/firearms/{_seg(id)}")
