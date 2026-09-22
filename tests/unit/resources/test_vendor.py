"""Tests for the Vendor and AsyncVendor resource classes."""

from __future__ import annotations

from gunspec._resources._vendor import AsyncVendor, Vendor


class TestVendor:
    def test_shops(self, mock_sync_client):
        Vendor(mock_sync_client).shops()
        mock_sync_client.get.assert_called_once_with("/v1/vendor/shops")

    def test_list_offers(self, mock_sync_client):
        params = {"vendor": "shop_1", "status": "published", "q": "sku"}
        Vendor(mock_sync_client).list_offers(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/vendor/offers", query=params)

    def test_push_offers_puts_batch_with_scope(self, mock_sync_client):
        body = {
            "offers": [
                {
                    "sku": "A1",
                    "attachment_id": "x",
                    "price_cents": 1999,
                    "currency": "AUD",
                    "url": "https://shop.example/a1",
                }
            ]
        }
        Vendor(mock_sync_client).push_offers(body, {"vendor": "shop_1"})
        mock_sync_client.put.assert_called_once_with(
            "/v1/vendor/offers", body=body, query={"vendor": "shop_1"}
        )

    def test_update_offer_patches_encoded_sku(self, mock_sync_client):
        Vendor(mock_sync_client).update_offer("A/1", {"price_cents": 1899})
        mock_sync_client.patch.assert_called_once_with(
            "/v1/vendor/offers/A%2F1", body={"price_cents": 1899}, query=None
        )

    def test_delete_offer(self, mock_sync_client):
        Vendor(mock_sync_client).delete_offer("A1", {"vendor": "shop_2"})
        mock_sync_client.delete.assert_called_once_with("/v1/vendor/offers/A1", query={"vendor": "shop_2"})

    def test_click_url_builds_link_without_a_request(self, mock_sync_client):
        v = Vendor(mock_sync_client)
        assert v.click_url("clk_abc") == "https://api.gunspec.io/v1/out/clk_abc"
        assert v.click_url("clk/abc", "de") == "https://api.gunspec.io/v1/out/clk%2Fabc?l=de"
        mock_sync_client.get.assert_not_called()

    def test_resolve_click(self, mock_sync_client):
        mock_sync_client.resolve_redirect.return_value = "https://shop.example/x"
        assert Vendor(mock_sync_client).resolve_click("clk_abc") == "https://shop.example/x"
        mock_sync_client.resolve_redirect.assert_called_once_with("/v1/out/clk_abc")


class TestAsyncVendor:
    async def test_shops_and_offers(self, mock_async_client):
        v = AsyncVendor(mock_async_client)
        await v.shops()
        mock_async_client.get.assert_called_once_with("/v1/vendor/shops")
        await v.push_offers({"offers": []})
        mock_async_client.put.assert_called_once_with("/v1/vendor/offers", body={"offers": []}, query=None)
        await v.update_offer("A1", {"in_stock": False})
        mock_async_client.patch.assert_called_once_with(
            "/v1/vendor/offers/A1", body={"in_stock": False}, query=None
        )
        await v.delete_offer("A1")
        mock_async_client.delete.assert_called_once_with("/v1/vendor/offers/A1", query=None)

    async def test_click_url_and_resolve(self, mock_async_client):
        v = AsyncVendor(mock_async_client)
        assert v.click_url("clk_1") == "https://api.gunspec.io/v1/out/clk_1"
        mock_async_client.resolve_redirect.return_value = "https://shop.example/y"
        assert await v.resolve_click("clk_1") == "https://shop.example/y"
