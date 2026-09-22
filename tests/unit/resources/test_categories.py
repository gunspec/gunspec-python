"""Tests for the Categories and AsyncCategories resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._categories import AsyncCategories, Categories


class TestCategories:
    """Sync Categories resource tests."""

    def test_list(self, mock_sync_client):
        resource = Categories(mock_sync_client)
        resource.list()
        mock_sync_client.get.assert_called_once_with("/v1/categories")

    def test_get_firearms(self, mock_sync_client):
        resource = Categories(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.get_firearms("pistols", params)
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/categories/{quote('pistols', safe='')}/firearms", query=params
        )

    def test_get_firearms_no_params(self, mock_sync_client):
        resource = Categories(mock_sync_client)
        resource.get_firearms("rifles")
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/categories/{quote('rifles', safe='')}/firearms", query=None
        )


class TestAsyncCategories:
    """Async Categories resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncCategories(mock_async_client)
        await resource.list()
        mock_async_client.get.assert_called_once_with("/v1/categories")

    async def test_get_firearms(self, mock_async_client):
        resource = AsyncCategories(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.get_firearms("pistols", params)
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/categories/{quote('pistols', safe='')}/firearms", query=params
        )

    async def test_get_firearms_no_params(self, mock_async_client):
        resource = AsyncCategories(mock_async_client)
        await resource.get_firearms("rifles")
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/categories/{quote('rifles', safe='')}/firearms", query=None
        )
