"""Tests for the Ammunition and AsyncAmmunition resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._ammunition import Ammunition, AsyncAmmunition


class TestAmmunition:
    """Sync Ammunition resource tests."""

    def test_list(self, mock_sync_client):
        resource = Ammunition(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/ammunition", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Ammunition(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/ammunition", query=None)

    def test_get(self, mock_sync_client):
        resource = Ammunition(mock_sync_client)
        resource.get("federal-hst-9mm")
        mock_sync_client.get.assert_called_once_with(f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}")

    def test_get_bullet_svg(self, mock_sync_client):
        resource = Ammunition(mock_sync_client)
        mock_sync_client.get_text.return_value = "<svg/>"
        assert resource.get_bullet_svg("federal-hst-9mm") == "<svg/>"
        mock_sync_client.get_text.assert_called_once_with(
            f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}/bullet.svg"
        )
        mock_sync_client.get.assert_not_called()

    def test_ballistics(self, mock_sync_client):
        resource = Ammunition(mock_sync_client)
        params = {"range": 100}
        resource.ballistics("federal-hst-9mm", params)
        mock_sync_client.get.assert_called_once_with(
            f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}/ballistics",
            query=params,
        )

    def test_ballistics_no_params(self, mock_sync_client):
        resource = Ammunition(mock_sync_client)
        resource.ballistics("federal-hst-9mm")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}/ballistics",
            query=None,
        )


class TestAsyncAmmunition:
    """Async Ammunition resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncAmmunition(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/ammunition", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncAmmunition(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/ammunition", query=None)

    async def test_get(self, mock_async_client):
        resource = AsyncAmmunition(mock_async_client)
        await resource.get("federal-hst-9mm")
        mock_async_client.get.assert_called_once_with(f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}")

    async def test_get_bullet_svg(self, mock_async_client):
        resource = AsyncAmmunition(mock_async_client)
        mock_async_client.get_text.return_value = "<svg/>"
        assert await resource.get_bullet_svg("federal-hst-9mm") == "<svg/>"
        mock_async_client.get_text.assert_called_once_with(
            f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}/bullet.svg"
        )
        mock_async_client.get.assert_not_called()

    async def test_ballistics(self, mock_async_client):
        resource = AsyncAmmunition(mock_async_client)
        params = {"range": 100}
        await resource.ballistics("federal-hst-9mm", params)
        mock_async_client.get.assert_called_once_with(
            f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}/ballistics",
            query=params,
        )

    async def test_ballistics_no_params(self, mock_async_client):
        resource = AsyncAmmunition(mock_async_client)
        await resource.ballistics("federal-hst-9mm")
        mock_async_client.get.assert_called_once_with(
            f"/v1/ammunition/{quote('federal-hst-9mm', safe='')}/ballistics",
            query=None,
        )
