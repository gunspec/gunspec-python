"""Tests for the Reports and AsyncReports resource classes."""

from __future__ import annotations

from gunspec._resources._reports import AsyncReports, Reports


class TestReports:
    """Sync Reports resource tests."""

    def test_create(self, mock_sync_client):
        resource = Reports(mock_sync_client)
        params = {"firearm_id": "glock-g17", "reason": "incorrect-spec"}
        resource.create(params)
        mock_sync_client.post.assert_called_once_with("/v1/me/reports", body=params)

    def test_list(self, mock_sync_client):
        resource = Reports(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/reports", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Reports(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/reports", query=None)


class TestAsyncReports:
    """Async Reports resource tests."""

    async def test_create(self, mock_async_client):
        resource = AsyncReports(mock_async_client)
        params = {"firearm_id": "glock-g17", "reason": "incorrect-spec"}
        await resource.create(params)
        mock_async_client.post.assert_called_once_with("/v1/me/reports", body=params)

    async def test_list(self, mock_async_client):
        resource = AsyncReports(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/reports", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncReports(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/reports", query=None)
