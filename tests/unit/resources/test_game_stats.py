"""Tests for the GameStats_ and AsyncGameStats_ resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._game_stats import AsyncGameStats_, GameStats_


class TestGameStats:
    """Sync GameStats_ resource tests."""

    def test_list_versions(self, mock_sync_client):
        resource = GameStats_(mock_sync_client)
        resource.list_versions()
        mock_sync_client.get.assert_called_once_with("/v1/game-stats/versions")

    def test_list_firearms(self, mock_sync_client):
        resource = GameStats_(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list_firearms("1.0.0", params)
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/game-stats/versions/{quote('1.0.0', safe='')}/firearms",
            query=params,
        )

    def test_list_firearms_no_params(self, mock_sync_client):
        resource = GameStats_(mock_sync_client)
        resource.list_firearms("1.0.0")
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/game-stats/versions/{quote('1.0.0', safe='')}/firearms",
            query=None,
        )

    def test_get_firearm(self, mock_sync_client):
        resource = GameStats_(mock_sync_client)
        resource.get_firearm("1.0.0", "glock-g17")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/game-stats/versions/{quote('1.0.0', safe='')}/firearms/{quote('glock-g17', safe='')}"
        )


class TestAsyncGameStats:
    """Async GameStats_ resource tests."""

    async def test_list_versions(self, mock_async_client):
        resource = AsyncGameStats_(mock_async_client)
        await resource.list_versions()
        mock_async_client.get.assert_called_once_with("/v1/game-stats/versions")

    async def test_list_firearms(self, mock_async_client):
        resource = AsyncGameStats_(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list_firearms("1.0.0", params)
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/game-stats/versions/{quote('1.0.0', safe='')}/firearms",
            query=params,
        )

    async def test_list_firearms_no_params(self, mock_async_client):
        resource = AsyncGameStats_(mock_async_client)
        await resource.list_firearms("1.0.0")
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/game-stats/versions/{quote('1.0.0', safe='')}/firearms",
            query=None,
        )

    async def test_get_firearm(self, mock_async_client):
        resource = AsyncGameStats_(mock_async_client)
        await resource.get_firearm("1.0.0", "glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/game-stats/versions/{quote('1.0.0', safe='')}/firearms/{quote('glock-g17', safe='')}"
        )
