"""Tests for the Countries and AsyncCountries resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._countries import AsyncCountries, Countries


class TestCountries:
    """Sync Countries resource tests."""

    def test_list(self, mock_sync_client):
        resource = Countries(mock_sync_client)
        resource.list()
        mock_sync_client.get.assert_called_once_with("/v1/countries")

    def test_get_arsenal(self, mock_sync_client):
        resource = Countries(mock_sync_client)
        resource.get_arsenal("US")
        mock_sync_client.get.assert_called_once_with(f"/v1/countries/{quote('US', safe='')}/arsenal")


class TestAsyncCountries:
    """Async Countries resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncCountries(mock_async_client)
        await resource.list()
        mock_async_client.get.assert_called_once_with("/v1/countries")

    async def test_get_arsenal(self, mock_async_client):
        resource = AsyncCountries(mock_async_client)
        await resource.get_arsenal("US")
        mock_async_client.get.assert_called_once_with(f"/v1/countries/{quote('US', safe='')}/arsenal")
