"""Tests for the Attachments, Interfaces and Platforms resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._attachments import AsyncAttachments, Attachments
from gunspec._resources._compat import AsyncInterfaces, AsyncPlatforms, Interfaces, Platforms
from tests.conftest import make_paginated_response


class TestAttachments:
    def test_list_forwards_fit_engine_filters(self, mock_sync_client):
        params = {"fits": "ak-74m", "category": "suppressor", "only_offered": True, "vendor": "me"}
        Attachments(mock_sync_client).list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/attachments", query=params)

    def test_get_encodes_id(self, mock_sync_client):
        Attachments(mock_sync_client).get("a/b")
        mock_sync_client.get.assert_called_once_with("/v1/attachments/a%2Fb")

    def test_get_firearms_pages(self, mock_sync_client):
        Attachments(mock_sync_client).get_firearms("surefire-socom556", {"page": 2})
        mock_sync_client.get_paginated.assert_called_once_with(
            "/v1/attachments/surefire-socom556/firearms", query={"page": 2}
        )

    def test_get_offers_forwards_region(self, mock_sync_client):
        Attachments(mock_sync_client).get_offers("x", {"region": "AU"})
        mock_sync_client.get.assert_called_once_with("/v1/attachments/x/offers", query={"region": "AU"})

    def test_list_auto_paging_walks_pages(self, mock_sync_client):
        mock_sync_client.get_paginated.side_effect = [
            make_paginated_response([{"id": "a"}, {"id": "b"}], page=1, total_pages=2),
            make_paginated_response([{"id": "c"}], page=2, total_pages=2),
        ]
        ids = [i["id"] for i in Attachments(mock_sync_client).list_auto_paging({"category": "optic"})]
        assert ids == ["a", "b", "c"]
        assert mock_sync_client.get_paginated.call_count == 2


class TestAsyncAttachments:
    async def test_list_and_get(self, mock_async_client):
        r = AsyncAttachments(mock_async_client)
        await r.list({"q": "socom"})
        mock_async_client.get_paginated.assert_called_once_with("/v1/attachments", query={"q": "socom"})
        await r.get("x")
        mock_async_client.get.assert_called_once_with("/v1/attachments/x")

    async def test_list_auto_paging(self, mock_async_client):
        mock_async_client.get_paginated.side_effect = [
            make_paginated_response([{"id": "a"}], page=1, total_pages=2),
            make_paginated_response([{"id": "b"}], page=2, total_pages=2),
        ]
        ids = [i["id"] async for i in AsyncAttachments(mock_async_client).list_auto_paging()]
        assert ids == ["a", "b"]


class TestInterfaces:
    def test_list_forwards_kind(self, mock_sync_client):
        Interfaces(mock_sync_client).list({"kind": "thread"})
        mock_sync_client.get.assert_called_once_with("/v1/interfaces", query={"kind": "thread"})

    def test_get_firearms_encodes_colon_and_slash(self, mock_sync_client):
        Interfaces(mock_sync_client).get_firearms("thread:1/2x28")
        mock_sync_client.get_paginated.assert_called_once_with(
            f"/v1/interfaces/{quote('thread:1/2x28', safe='')}/firearms", query=None
        )
        assert "thread%3A1%2F2x28" in mock_sync_client.get_paginated.call_args.args[0]

    async def test_async(self, mock_async_client):
        await AsyncInterfaces(mock_async_client).get_firearms("mag:stanag", {"per_page": 1})
        mock_async_client.get_paginated.assert_called_once_with(
            "/v1/interfaces/mag%3Astanag/firearms", query={"per_page": 1}
        )


class TestPlatforms:
    def test_list_and_get(self, mock_sync_client):
        r = Platforms(mock_sync_client)
        r.list()
        mock_sync_client.get.assert_called_with("/v1/platforms")
        r.get("ak-100")
        mock_sync_client.get.assert_called_with("/v1/platforms/ak-100")

    async def test_async(self, mock_async_client):
        await AsyncPlatforms(mock_async_client).get("ar-15")
        mock_async_client.get.assert_called_once_with("/v1/platforms/ar-15")
