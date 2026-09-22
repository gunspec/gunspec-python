from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Union

from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Content:
    """Sync content resource.

    Wraps the public ``/v1/blog`` and ``/v1/changelog`` feeds. Neither requires
    an API key, so they can be rendered somewhere without a credential to hand.
    """

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def list_changelog(self, params: Optional[Mapping[str, Any]] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/changelog", query=params)

    def get_changelog_entry(self, id: Union[str, int]) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/changelog/{_seg(id)}")

    def list_blog_posts(
        self, params: Optional[Mapping[str, Any]] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/blog", query=params)

    def get_blog_post(self, slug: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/blog/{_seg(slug)}")

    def list_notices(self) -> APIResponse[Dict[str, Any]]:
        """The notices the website is showing right now, best first. Public."""
        return self._client.get("/v1/notices")


class AsyncContent:
    """Async content resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list_changelog(
        self, params: Optional[Mapping[str, Any]] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/changelog", query=params)

    async def get_changelog_entry(self, id: Union[str, int]) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/changelog/{_seg(id)}")

    async def list_blog_posts(
        self, params: Optional[Mapping[str, Any]] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/blog", query=params)

    async def get_blog_post(self, slug: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/blog/{_seg(slug)}")

    async def list_notices(self) -> APIResponse[Dict[str, Any]]:
        """The notices the website is showing right now, best first. Public."""
        return await self._client.get("/v1/notices")
