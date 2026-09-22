"""Tests for the Favorites and AsyncFavorites resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._favorites import AsyncFavorites, Favorites


class TestFavorites:
    """Sync Favorites resource tests."""

    def test_list(self, mock_sync_client):
        resource = Favorites(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/favorites", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Favorites(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/favorites", query=None)

    def test_add(self, mock_sync_client):
        resource = Favorites(mock_sync_client)
        resource.add("glock-g17")
        mock_sync_client.post.assert_called_once_with(f"/v1/me/favorites/{quote('glock-g17', safe='')}")

    def test_remove(self, mock_sync_client):
        resource = Favorites(mock_sync_client)
        resource.remove("glock-g17")
        mock_sync_client.delete.assert_called_once_with(f"/v1/me/favorites/{quote('glock-g17', safe='')}")


class TestAsyncFavorites:
    """Async Favorites resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncFavorites(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/favorites", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncFavorites(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/favorites", query=None)

    async def test_add(self, mock_async_client):
        resource = AsyncFavorites(mock_async_client)
        await resource.add("glock-g17")
        mock_async_client.post.assert_called_once_with(f"/v1/me/favorites/{quote('glock-g17', safe='')}")

    async def test_remove(self, mock_async_client):
        resource = AsyncFavorites(mock_async_client)
        await resource.remove("glock-g17")
        mock_async_client.delete.assert_called_once_with(f"/v1/me/favorites/{quote('glock-g17', safe='')}")
