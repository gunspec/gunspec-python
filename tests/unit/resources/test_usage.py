"""Tests for the Usage and AsyncUsage resource classes."""

from __future__ import annotations

from gunspec._resources._usage import AsyncUsage, Usage


class TestUsage:
    """Sync Usage resource tests."""

    def test_get(self, mock_sync_client):
        resource = Usage(mock_sync_client)
        params = {"period": "monthly"}
        resource.get(params)
        mock_sync_client.get.assert_called_once_with("/v1/me/usage", query=params)

    def test_get_no_params(self, mock_sync_client):
        resource = Usage(mock_sync_client)
        resource.get()
        mock_sync_client.get.assert_called_once_with("/v1/me/usage", query=None)


class TestAsyncUsage:
    """Async Usage resource tests."""

    async def test_get(self, mock_async_client):
        resource = AsyncUsage(mock_async_client)
        params = {"period": "monthly"}
        await resource.get(params)
        mock_async_client.get.assert_called_once_with("/v1/me/usage", query=params)

    async def test_get_no_params(self, mock_async_client):
        resource = AsyncUsage(mock_async_client)
        await resource.get()
        mock_async_client.get.assert_called_once_with("/v1/me/usage", query=None)
