"""Tests for the Support and AsyncSupport resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._support import AsyncSupport, Support


class TestSupport:
    """Sync Support resource tests."""

    def test_create(self, mock_sync_client):
        resource = Support(mock_sync_client)
        params = {"subject": "Bug report", "message": "Something is wrong"}
        resource.create(params)
        mock_sync_client.post.assert_called_once_with("/v1/me/support", body=params)

    def test_list(self, mock_sync_client):
        resource = Support(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/support", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Support(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/support", query=None)

    def test_get(self, mock_sync_client):
        resource = Support(mock_sync_client)
        resource.get("ticket-123")
        mock_sync_client.get.assert_called_once_with(f"/v1/me/support/{quote('ticket-123', safe='')}")

    def test_reply(self, mock_sync_client):
        resource = Support(mock_sync_client)
        params = {"message": "Here is more info"}
        resource.reply("ticket-123", params)
        mock_sync_client.post.assert_called_once_with(
            f"/v1/me/support/{quote('ticket-123', safe='')}/replies", body=params
        )


class TestAsyncSupport:
    """Async Support resource tests."""

    async def test_create(self, mock_async_client):
        resource = AsyncSupport(mock_async_client)
        params = {"subject": "Bug report", "message": "Something is wrong"}
        await resource.create(params)
        mock_async_client.post.assert_called_once_with("/v1/me/support", body=params)

    async def test_list(self, mock_async_client):
        resource = AsyncSupport(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/support", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncSupport(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/support", query=None)

    async def test_get(self, mock_async_client):
        resource = AsyncSupport(mock_async_client)
        await resource.get("ticket-123")
        mock_async_client.get.assert_called_once_with(f"/v1/me/support/{quote('ticket-123', safe='')}")

    async def test_reply(self, mock_async_client):
        resource = AsyncSupport(mock_async_client)
        params = {"message": "Here is more info"}
        await resource.reply("ticket-123", params)
        mock_async_client.post.assert_called_once_with(
            f"/v1/me/support/{quote('ticket-123', safe='')}/replies", body=params
        )
