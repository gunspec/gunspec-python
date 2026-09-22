"""Tests for the DataQuality and AsyncDataQuality resource classes."""

from __future__ import annotations

from gunspec._resources._data_quality import AsyncDataQuality, DataQuality


class TestDataQuality:
    """Sync DataQuality resource tests."""

    def test_coverage(self, mock_sync_client):
        resource = DataQuality(mock_sync_client)
        resource.coverage()
        mock_sync_client.get.assert_called_once_with("/v1/data/coverage")

    def test_confidence(self, mock_sync_client):
        resource = DataQuality(mock_sync_client)
        params = {"min_score": 0.8}
        resource.confidence(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/data/confidence", query=params)

    def test_confidence_no_params(self, mock_sync_client):
        resource = DataQuality(mock_sync_client)
        resource.confidence()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/data/confidence", query=None)


class TestAsyncDataQuality:
    """Async DataQuality resource tests."""

    async def test_coverage(self, mock_async_client):
        resource = AsyncDataQuality(mock_async_client)
        await resource.coverage()
        mock_async_client.get.assert_called_once_with("/v1/data/coverage")

    async def test_confidence(self, mock_async_client):
        resource = AsyncDataQuality(mock_async_client)
        params = {"min_score": 0.8}
        await resource.confidence(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/data/confidence", query=params)

    async def test_confidence_no_params(self, mock_async_client):
        resource = AsyncDataQuality(mock_async_client)
        await resource.confidence()
        mock_async_client.get_paginated.assert_called_once_with("/v1/data/confidence", query=None)
