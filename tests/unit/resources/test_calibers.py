"""Tests for the Calibers and AsyncCalibers resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._calibers import AsyncCalibers, Calibers


class TestCalibers:
    """Sync Calibers resource tests."""

    def test_list(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/calibers", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/calibers", query=None)

    def test_compare(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        params = {"ids": "9mm,45acp"}
        resource.compare(params)
        mock_sync_client.get.assert_called_once_with("/v1/calibers/compare", query=params)

    def test_ballistics(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        params = {"caliber_id": "9mm"}
        resource.ballistics(params)
        mock_sync_client.get.assert_called_once_with("/v1/calibers/ballistics", query=params)

    def test_get(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        resource.get("9mm-luger")
        mock_sync_client.get.assert_called_once_with(f"/v1/calibers/{quote('9mm-luger', safe='')}")

    def test_get_firearms(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        params = {"page": 1}
        resource.get_firearms("9mm-luger", params)
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/firearms", query=params
        )

    def test_get_firearms_no_params(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        resource.get_firearms("9mm-luger")
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/firearms", query=None
        )

    def test_get_parent_chain(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        resource.get_parent_chain("9mm-luger")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/parent-chain"
        )

    def test_get_family(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        resource.get_family("9mm-luger")
        mock_sync_client.get.assert_called_once_with(f"/v1/calibers/{quote('9mm-luger', safe='')}/family")

    def test_get_ammunition(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        params = {"page": 1}
        resource.get_ammunition("9mm-luger", params)
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/ammunition", query=params
        )

    def test_get_ammunition_no_params(self, mock_sync_client):
        resource = Calibers(mock_sync_client)
        resource.get_ammunition("9mm-luger")
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/ammunition", query=None
        )


class TestAsyncCalibers:
    """Async Calibers resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/calibers", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/calibers", query=None)

    async def test_compare(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        params = {"ids": "9mm,45acp"}
        await resource.compare(params)
        mock_async_client.get.assert_called_once_with("/v1/calibers/compare", query=params)

    async def test_ballistics(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        params = {"caliber_id": "9mm"}
        await resource.ballistics(params)
        mock_async_client.get.assert_called_once_with("/v1/calibers/ballistics", query=params)

    async def test_get(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        await resource.get("9mm-luger")
        mock_async_client.get.assert_called_once_with(f"/v1/calibers/{quote('9mm-luger', safe='')}")

    async def test_get_firearms(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        params = {"page": 1}
        await resource.get_firearms("9mm-luger", params)
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/firearms", query=params
        )

    async def test_get_firearms_no_params(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        await resource.get_firearms("9mm-luger")
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/firearms", query=None
        )

    async def test_get_parent_chain(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        await resource.get_parent_chain("9mm-luger")
        mock_async_client.get.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/parent-chain"
        )

    async def test_get_family(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        await resource.get_family("9mm-luger")
        mock_async_client.get.assert_called_once_with(f"/v1/calibers/{quote('9mm-luger', safe='')}/family")

    async def test_get_ammunition(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        params = {"page": 1}
        await resource.get_ammunition("9mm-luger", params)
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/ammunition", query=params
        )

    async def test_get_ammunition_no_params(self, mock_async_client):
        resource = AsyncCalibers(mock_async_client)
        await resource.get_ammunition("9mm-luger")
        mock_async_client.get_paginated.assert_called_once_with(
            f"/v1/calibers/{quote('9mm-luger', safe='')}/ammunition", query=None
        )
