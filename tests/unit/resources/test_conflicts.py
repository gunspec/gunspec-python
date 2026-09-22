"""Tests for the Conflicts and AsyncConflicts resource classes."""

from __future__ import annotations

from gunspec._resources._conflicts import AsyncConflicts, Conflicts


class TestConflicts:
    """Sync Conflicts resource tests."""

    def test_list(self, mock_sync_client):
        resource = Conflicts(mock_sync_client)
        resource.list()
        mock_sync_client.get.assert_called_once_with("/v1/conflicts")


class TestAsyncConflicts:
    """Async Conflicts resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncConflicts(mock_async_client)
        await resource.list()
        mock_async_client.get.assert_called_once_with("/v1/conflicts")
