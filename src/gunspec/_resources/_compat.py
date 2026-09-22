from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import ListInterfacesParams, PaginationParams
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Interfaces:
    """Sync interface standards resource: the mount vocabulary every fit is
    computed from (``thread:1/2x28``, ``mag:stanag``)."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self, params: Optional[ListInterfacesParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/interfaces", query=params)

    def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        """Firearms exposing a standard. The id's colon and slash are encoded. Studio."""
        return self._client.get_paginated(f"/v1/interfaces/{_seg(id)}/firearms", query=params)


class AsyncInterfaces:
    """Async interface standards resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self, params: Optional[ListInterfacesParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/interfaces", query=params)

    async def get_firearms(
        self, id: str, params: Optional[PaginationParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated(f"/v1/interfaces/{_seg(id)}/firearms", query=params)


class Platforms:
    """Sync platforms resource: the families whose interface rows every
    member inherits. Studio."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/platforms")

    def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/platforms/{_seg(id)}")


class AsyncPlatforms:
    """Async platforms resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/platforms")

    async def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/platforms/{_seg(id)}")
