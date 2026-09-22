"""Tests for the Game and AsyncGame resource classes."""

from __future__ import annotations

from gunspec._resources._game import AsyncGame, Game


class TestGame:
    """Sync Game resource tests."""

    def test_balance_report(self, mock_sync_client):
        resource = Game(mock_sync_client)
        params = {"category": "pistol"}
        resource.balance_report(params)
        mock_sync_client.get.assert_called_once_with("/v1/game/balance-report", query=params)

    def test_balance_report_no_params(self, mock_sync_client):
        resource = Game(mock_sync_client)
        resource.balance_report()
        mock_sync_client.get.assert_called_once_with("/v1/game/balance-report", query=None)

    def test_tier_list(self, mock_sync_client):
        resource = Game(mock_sync_client)
        params = {"version": "1.0"}
        resource.tier_list(params)
        mock_sync_client.get.assert_called_once_with("/v1/game/tier-list", query=params)

    def test_tier_list_no_params(self, mock_sync_client):
        resource = Game(mock_sync_client)
        resource.tier_list()
        mock_sync_client.get.assert_called_once_with("/v1/game/tier-list", query=None)

    def test_matchups(self, mock_sync_client):
        resource = Game(mock_sync_client)
        params = {"firearm_a": "glock-g17", "firearm_b": "sig-p320"}
        resource.matchups(params)
        mock_sync_client.get.assert_called_once_with("/v1/game/matchups", query=params)

    def test_role_roster(self, mock_sync_client):
        resource = Game(mock_sync_client)
        params = {"role": "assault"}
        resource.role_roster(params)
        mock_sync_client.get.assert_called_once_with("/v1/game/role-roster", query=params)

    def test_stat_distribution(self, mock_sync_client):
        resource = Game(mock_sync_client)
        params = {"stat": "damage"}
        resource.stat_distribution(params)
        mock_sync_client.get.assert_called_once_with("/v1/game/stat-distribution", query=params)


class TestAsyncGame:
    """Async Game resource tests."""

    async def test_balance_report(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        params = {"category": "pistol"}
        await resource.balance_report(params)
        mock_async_client.get.assert_called_once_with("/v1/game/balance-report", query=params)

    async def test_balance_report_no_params(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        await resource.balance_report()
        mock_async_client.get.assert_called_once_with("/v1/game/balance-report", query=None)

    async def test_tier_list(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        params = {"version": "1.0"}
        await resource.tier_list(params)
        mock_async_client.get.assert_called_once_with("/v1/game/tier-list", query=params)

    async def test_tier_list_no_params(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        await resource.tier_list()
        mock_async_client.get.assert_called_once_with("/v1/game/tier-list", query=None)

    async def test_matchups(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        params = {"firearm_a": "glock-g17", "firearm_b": "sig-p320"}
        await resource.matchups(params)
        mock_async_client.get.assert_called_once_with("/v1/game/matchups", query=params)

    async def test_role_roster(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        params = {"role": "assault"}
        await resource.role_roster(params)
        mock_async_client.get.assert_called_once_with("/v1/game/role-roster", query=params)

    async def test_stat_distribution(self, mock_async_client):
        resource = AsyncGame(mock_async_client)
        params = {"stat": "damage"}
        await resource.stat_distribution(params)
        mock_async_client.get.assert_called_once_with("/v1/game/stat-distribution", query=params)
