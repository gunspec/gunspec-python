from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, SyncHttpClient


class Collections:
    """Sync collections resource.

    Reads a user collection that has been shared publicly. The share id is the
    only credential, and collections that have not been shared are not reachable
    through it, so no API key is required.
    """

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get_shared(self, share_id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/collections/{_seg(share_id)}")


class AsyncCollections:
    """Async collections resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get_shared(self, share_id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/collections/{_seg(share_id)}")
