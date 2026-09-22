"""Tests for the firearms extras mixin (resolve, media, offers, compatibility)
and the content notices endpoint."""

from __future__ import annotations

from gunspec._resources._content import AsyncContent, Content
from gunspec._resources._firearms import AsyncFirearms, Firearms
from tests.conftest import make_raw_response


class TestFirearmsExtras:
    def test_resolve(self, mock_sync_client):
        Firearms(mock_sync_client).resolve("G19 gen 5")
        mock_sync_client.get.assert_called_once_with("/v1/firearms/resolve", query={"q": "G19 gen 5"})

    def test_resolve_many_posts_batch(self, mock_sync_client):
        Firearms(mock_sync_client).resolve_many(["a", "b"])
        mock_sync_client.post.assert_called_once_with("/v1/firearms/resolve", body={"queries": ["a", "b"]})

    def test_media_catalog_pages(self, mock_sync_client):
        Firearms(mock_sync_client).media_catalog({"kind": "photo", "per_page": 50})
        mock_sync_client.get_paginated.assert_called_once_with(
            "/v1/firearms/media", query={"kind": "photo", "per_page": 50}
        )

    def test_list_media_and_get_media(self, mock_sync_client):
        r = Firearms(mock_sync_client)
        r.list_media("ak-47", {"kind": "silhouette"})
        mock_sync_client.get.assert_called_with("/v1/firearms/ak-47/media", query={"kind": "silhouette"})
        r.get_media("ak-47", "silhouette", {"stroke_width": 2})
        mock_sync_client.get.assert_called_with(
            "/v1/firearms/ak-47/media/silhouette", query={"stroke_width": 2, "format": "json"}
        )
        r.get_media("ak-47", 12)
        mock_sync_client.get.assert_called_with("/v1/firearms/ak-47/media/12", query={"format": "json"})

    def test_download_media_and_get_model_read_bytes(self, mock_sync_client):
        mock_sync_client.get_bytes.return_value = make_raw_response("bytes", "model/gltf-binary")
        r = Firearms(mock_sync_client)
        r.download_media("ak-47", "render", {"size": "thumb"})
        mock_sync_client.get_bytes.assert_called_with(
            "/v1/firearms/ak-47/media/render", query={"size": "thumb", "format": "raw"}
        )
        raw = r.get_model("ak/47")
        mock_sync_client.get_bytes.assert_called_with("/v1/firearms/ak%2F47/model")
        assert raw.body == b"bytes"

    def test_get_image_asset_asks_for_data_uri(self, mock_sync_client):
        Firearms(mock_sync_client).get_image_asset("ak-47", 7, {"variant": "thumb"})
        mock_sync_client.get.assert_called_once_with(
            "/v1/firearms/ak-47/images/7", query={"variant": "thumb", "format": "datauri"}
        )

    def test_offers_interfaces_attachments(self, mock_sync_client):
        r = Firearms(mock_sync_client)
        r.get_offers("ak-47", {"region": "DE"})
        mock_sync_client.get.assert_called_with("/v1/firearms/ak-47/offers", query={"region": "DE"})
        r.get_interfaces("ak-47")
        mock_sync_client.get.assert_called_with("/v1/firearms/ak-47/interfaces")
        r.get_attachments("ak-47", {"include": "all", "with_offers": True})
        mock_sync_client.get.assert_called_with(
            "/v1/firearms/ak-47/attachments", query={"include": "all", "with_offers": True}
        )


class TestAsyncFirearmsExtras:
    async def test_resolve_and_media(self, mock_async_client):
        r = AsyncFirearms(mock_async_client)
        await r.resolve("M4A1")
        mock_async_client.get.assert_called_with("/v1/firearms/resolve", query={"q": "M4A1"})
        await r.resolve_many(["x"])
        mock_async_client.post.assert_called_once_with("/v1/firearms/resolve", body={"queries": ["x"]})
        await r.get_media("ak-47", "photo")
        mock_async_client.get.assert_called_with("/v1/firearms/ak-47/media/photo", query={"format": "json"})
        await r.get_model("ak-47")
        mock_async_client.get_bytes.assert_called_with("/v1/firearms/ak-47/model")

    async def test_compat(self, mock_async_client):
        r = AsyncFirearms(mock_async_client)
        await r.get_interfaces("ak-47")
        mock_async_client.get.assert_called_with("/v1/firearms/ak-47/interfaces")
        await r.get_attachments("ak-47")
        mock_async_client.get.assert_called_with("/v1/firearms/ak-47/attachments", query=None)


class TestContentNotices:
    def test_list_notices(self, mock_sync_client):
        Content(mock_sync_client).list_notices()
        mock_sync_client.get.assert_called_once_with("/v1/notices")

    async def test_async_list_notices(self, mock_async_client):
        await AsyncContent(mock_async_client).list_notices()
        mock_async_client.get.assert_called_once_with("/v1/notices")
