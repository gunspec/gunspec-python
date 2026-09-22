"""Tests for the Manufacturers and AsyncManufacturers resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._manufacturers import AsyncManufacturers, Manufacturers


class TestManufacturers:
    """Sync Manufacturers resource tests."""

    def test_list(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/manufacturers", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/manufacturers", query=None)

    def test_get(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        resource.get("glock")
        mock_sync_client.get.assert_called_once_with(f"/v1/manufacturers/{quote('glock', safe='')}")

    def test_get_firearms(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        params = {"page": 1}
        resource.get_firearms("glock", params)
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/manufacturers/{quote('glock', safe='')}/firearms", query=params
        )

    def test_get_firearms_no_params(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        resource.get_firearms("glock")
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/manufacturers/{quote('glock', safe='')}/firearms", query=None
        )

    def test_get_timeline(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        resource.get_timeline("glock")
        mock_sync_client.get.assert_called_once_with(f"/v1/manufacturers/{quote('glock', safe='')}/timeline")

    def test_get_stats(self, mock_sync_client):
        resource = Manufacturers(mock_sync_client)
        resource.get_stats("glock")
        mock_sync_client.get.assert_called_once_with(f"/v1/manufacturers/{quote('glock', safe='')}/stats")


class TestAsyncManufacturers:
    """Async Manufacturers resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/manufacturers", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/manufacturers", query=None)

    async def test_get(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        await resource.get("glock")
        mock_async_client.get.assert_called_once_with(f"/v1/manufacturers/{quote('glock', safe='')}")

    async def test_get_firearms(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        params = {"page": 1}
        await resource.get_firearms("glock", params)
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/manufacturers/{quote('glock', safe='')}/firearms", query=params
        )

    async def test_get_firearms_no_params(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        await resource.get_firearms("glock")
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/manufacturers/{quote('glock', safe='')}/firearms", query=None
        )

    async def test_get_timeline(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        await resource.get_timeline("glock")
        mock_async_client.get.assert_called_once_with(f"/v1/manufacturers/{quote('glock', safe='')}/timeline")

    async def test_get_stats(self, mock_async_client):
        resource = AsyncManufacturers(mock_async_client)
        await resource.get_stats("glock")
        mock_async_client.get.assert_called_once_with(f"/v1/manufacturers/{quote('glock', safe='')}/stats")
