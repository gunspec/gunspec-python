"""Tests for the Docs and AsyncDocs resource classes."""

from __future__ import annotations

from gunspec._resources._docs import AsyncDocs, Docs


class TestDocs:
    """Sync Docs resource tests."""

    def test_get_operations(self, mock_sync_client):
        resource = Docs(mock_sync_client)
        params = {"path": "/v1/firearms/{id}", "method": "GET"}
        resource.get_operations(params)
        mock_sync_client.get.assert_called_once_with("/v1/docs/operations", query=params)

    def test_get_sample(self, mock_sync_client):
        resource = Docs(mock_sync_client)
        params = {"path": "/v1/firearms", "method": "GET", "language": "sdk-python"}
        resource.get_sample(params)
        mock_sync_client.get.assert_called_once_with("/v1/docs/samples", query=params)

    def test_get_limits(self, mock_sync_client):
        resource = Docs(mock_sync_client)
        resource.get_limits()
        mock_sync_client.get.assert_called_once_with("/v1/docs/limits")


class TestAsyncDocs:
    """Async Docs resource tests."""

    async def test_get_operations(self, mock_async_client):
        resource = AsyncDocs(mock_async_client)
        params = {"path": "/v1/vendor"}
        await resource.get_operations(params)
        mock_async_client.get.assert_called_once_with("/v1/docs/operations", query=params)

    async def test_get_sample(self, mock_async_client):
        resource = AsyncDocs(mock_async_client)
        params = {"path": "/v1/firearms", "language": "curl"}
        await resource.get_sample(params)
        mock_async_client.get.assert_called_once_with("/v1/docs/samples", query=params)

    async def test_get_limits(self, mock_async_client):
        resource = AsyncDocs(mock_async_client)
        await resource.get_limits()
        mock_async_client.get.assert_called_once_with("/v1/docs/limits")
