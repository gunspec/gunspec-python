"""Tests for the Webhooks and AsyncWebhooks resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._webhooks import AsyncWebhooks, Webhooks


class TestWebhooks:
    """Sync Webhooks resource tests."""

    def test_list(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/webhooks", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/me/webhooks", query=None)

    def test_create(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        params = {"url": "https://example.com/webhook", "events": ["firearm.created"]}
        resource.create(params)
        mock_sync_client.post.assert_called_once_with("/v1/me/webhooks", body=params)

    def test_get(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        resource.get("wh-123")
        mock_sync_client.get.assert_called_once_with(f"/v1/me/webhooks/{quote('wh-123', safe='')}")

    def test_update(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        params = {"url": "https://example.com/webhook-v2"}
        resource.update("wh-123", params)
        mock_sync_client.put.assert_called_once_with(
            f"/v1/me/webhooks/{quote('wh-123', safe='')}", body=params
        )

    def test_delete(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        resource.delete("wh-123")
        mock_sync_client.delete.assert_called_once_with(f"/v1/me/webhooks/{quote('wh-123', safe='')}")

    def test_test(self, mock_sync_client):
        resource = Webhooks(mock_sync_client)
        resource.test("wh-123")
        mock_sync_client.post.assert_called_once_with(f"/v1/me/webhooks/{quote('wh-123', safe='')}/test")


class TestAsyncWebhooks:
    """Async Webhooks resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/webhooks", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/me/webhooks", query=None)

    async def test_create(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        params = {"url": "https://example.com/webhook", "events": ["firearm.created"]}
        await resource.create(params)
        mock_async_client.post.assert_called_once_with("/v1/me/webhooks", body=params)

    async def test_get(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        await resource.get("wh-123")
        mock_async_client.get.assert_called_once_with(f"/v1/me/webhooks/{quote('wh-123', safe='')}")

    async def test_update(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        params = {"url": "https://example.com/webhook-v2"}
        await resource.update("wh-123", params)
        mock_async_client.put.assert_called_once_with(
            f"/v1/me/webhooks/{quote('wh-123', safe='')}", body=params
        )

    async def test_delete(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        await resource.delete("wh-123")
        mock_async_client.delete.assert_called_once_with(f"/v1/me/webhooks/{quote('wh-123', safe='')}")

    async def test_test(self, mock_async_client):
        resource = AsyncWebhooks(mock_async_client)
        await resource.test("wh-123")
        mock_async_client.post.assert_called_once_with(f"/v1/me/webhooks/{quote('wh-123', safe='')}/test")
