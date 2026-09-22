"""Integration suite against a running API.

Skipped unless ``GUNSPEC_INTEGRATION_BASE_URL`` and ``GUNSPEC_INTEGRATION_API_KEY``
are set; point them at the local worker (``pnpm dev:api``) and the dev
enterprise key that ``db:seed:dev-key`` creates. Every assertion is on the
shape the SDK promises, never on catalog figures, so a reseed cannot fail it.
Mirrors ``packages/sdk/tests/integration/local-api.test.ts``.
"""

from __future__ import annotations

import os
import time
from typing import Any

import pytest

from gunspec import (
    AuthenticationError,
    BadRequestError,
    ConfigurationError,
    GunSpec,
    GunSpecError,
    NotFoundError,
    PermissionDeniedError,
    RetryConfig,
)
from gunspec.types import (
    FIT_SOURCES,
    SOURCE_KINDS,
    AttachmentDetail,
    AttachmentFirearmFit,
    Caliber,
    FirearmAttachments,
    FirearmDetail,
)

BASE_URL = os.environ.get("GUNSPEC_INTEGRATION_BASE_URL")
API_KEY = os.environ.get("GUNSPEC_INTEGRATION_API_KEY")

pytestmark = pytest.mark.skipif(
    not (BASE_URL and API_KEY),
    reason="GUNSPEC_INTEGRATION_BASE_URL and GUNSPEC_INTEGRATION_API_KEY are not set",
)

NO_RETRY = RetryConfig(max_retries=0)


@pytest.fixture(scope="module")
def client() -> GunSpec:
    return GunSpec(api_key=API_KEY, base_url=BASE_URL, retry=NO_RETRY)


@pytest.fixture(scope="module")
def cached() -> GunSpec:
    return GunSpec(api_key=API_KEY, base_url=BASE_URL, retry=NO_RETRY, etag_cache=True)


@pytest.fixture(scope="module")
def firearm_id(client: GunSpec) -> str:
    data = client.firearms.list({"per_page": 1, "sort": "name"}).data
    assert len(data) == 1
    return str(data[0]["id"])


@pytest.fixture(scope="module")
def attachment_id(client: GunSpec) -> str:
    data = client.attachments.list({"per_page": 1}).data
    return str(data[0]["id"]) if data else ""


class TestCatalogReads:
    def test_list_carries_pagination_and_cache_metadata(self, client: GunSpec) -> None:
        res = client.firearms.list({"per_page": 2})
        assert res.pagination.limit == 2
        assert res.pagination.per_page == 2
        assert res.pagination.total and res.pagination.total > 0
        assert res.etag and res.etag.lstrip("W/").startswith('"')
        assert res.cache_control and "max-age" in res.cache_control
        assert res.request_id
        for f in res.data:
            assert isinstance(f["updatedAt"], str)
            assert "version" in f

    def test_get_returns_version_and_updated_at(self, client: GunSpec, firearm_id: str) -> None:
        data = client.firearms.get(firearm_id).data
        assert data["id"] == firearm_id
        assert isinstance(data["updatedAt"], str)

    def test_search_similar_variants_media(self, client: GunSpec, firearm_id: str) -> None:
        assert isinstance(client.firearms.search({"q": firearm_id.split("-")[0], "per_page": 3}).data, list)
        assert isinstance(client.firearms.get_similar(firearm_id).data, list)
        assert isinstance(client.firearms.get_variants(firearm_id).data, list)
        for m in client.firearms.list_media(firearm_id).data:
            assert m["url"].startswith(("http://", "https://"))
            assert m["kind"] in ("silhouette", "render", "photo", "schematic", "model")

    def test_resolve_turns_a_name_into_an_id(self, client: GunSpec, firearm_id: str) -> None:
        name = client.firearms.get(firearm_id).data["name"]
        data = client.firearms.resolve(name).data
        assert data["status"] in ("resolved", "ambiguous", "unresolved")
        assert data["query"] == name
        assert len(client.firearms.resolve_many([name, "not a real gun 123"]).data["results"]) == 2

    def test_media_catalog_pages(self, client: GunSpec) -> None:
        res = client.firearms.media_catalog({"per_page": 2})
        assert res.pagination.per_page == 2
        for row in res.data:
            assert isinstance(row["images"], list)

    def test_reference_resources_answer(self, client: GunSpec) -> None:
        assert len(client.manufacturers.list({"per_page": 1}).data) == 1
        assert len(client.calibers.list({"per_page": 1}).data) == 1
        assert len(client.categories.list().data) > 0
        assert isinstance(client.stats.summary().data, dict)

    def test_bullet_svg_is_text(self, client: GunSpec) -> None:
        ammo = client.ammunition.list({"per_page": 1}).data
        if not ammo:
            pytest.skip("no ammunition seeded")
        svg = client.ammunition.get_bullet_svg(ammo[0]["id"])
        assert svg.lstrip().startswith("<") and "svg" in svg

    def test_binary_as_json_names_the_right_method(self, client: GunSpec) -> None:
        ammo = client.ammunition.list({"per_page": 1}).data
        if not ammo:
            pytest.skip("no ammunition seeded")
        with pytest.raises(GunSpecError, match=r"get_text\(\)"):
            client.http.get(f"/v1/ammunition/{ammo[0]['id']}/bullet.svg")

    def test_public_content_needs_no_key(self, client: GunSpec) -> None:
        anon = GunSpec(api_key=None, base_url=BASE_URL, retry=NO_RETRY)
        assert isinstance(client.content.list_notices().data["notices"], list)
        assert isinstance(anon.content.list_changelog({"per_page": 1}).data, list)


class TestConditionalRequests:
    def test_second_get_is_from_cache(self, cached: GunSpec, firearm_id: str) -> None:
        first = cached.firearms.get(firearm_id)
        assert first.from_cache is False and first.etag
        second = cached.firearms.get(firearm_id)
        assert second.status == 304 and second.from_cache is True
        assert second.data == first.data

    def test_request_conditional_surfaces_304(self, client: GunSpec, firearm_id: str) -> None:
        fresh = client.firearms.get(firearm_id)
        assert fresh.etag
        res = client.http.request_conditional(f"/v1/firearms/{firearm_id}", if_none_match=fresh.etag)
        assert res.not_modified and res.status == 304


class TestCompatibility:
    def test_interfaces_and_platforms(self, client: GunSpec) -> None:
        standards = client.interfaces.list().data
        assert standards and ":" in standards[0]["id"]
        platforms = client.platforms.list().data
        assert isinstance(platforms, list)
        if platforms:
            assert isinstance(client.platforms.get(platforms[0]["id"]).data["interfaces"], list)

    def test_attachments_list_get_fit(self, client: GunSpec, attachment_id: str) -> None:
        if not attachment_id:
            pytest.skip("no attachments seeded")
        detail = client.attachments.get(attachment_id).data
        assert detail["id"] == attachment_id and isinstance(detail["requires"], list)
        assert isinstance(detail["provenance"]["sources"], list)
        AttachmentDetail.model_validate(detail)
        fits = client.attachments.get_firearms(attachment_id, {"per_page": 2}).data
        assert isinstance(fits, list)
        for fit in fits:
            assert isinstance(fit["source"], str) and fit["source"] in FIT_SOURCES
            AttachmentFirearmFit.model_validate(fit)

    def test_firearm_interfaces_and_fits(self, client: GunSpec, firearm_id: str) -> None:
        interfaces = client.firearms.get_interfaces(firearm_id).data
        assert interfaces["firearm"]["id"] == firearm_id
        assert isinstance(interfaces["interfaces"], list)
        fits = client.firearms.get_attachments(firearm_id, {"with_offers": True}).data
        assert isinstance(fits["groups"], list) and isinstance(fits["total"], int)
        for group in fits["groups"]:
            for item in group["items"]:
                assert isinstance(item["source"], str) and item["source"] in FIT_SOURCES
        FirearmAttachments.model_validate(fits)

    def test_standard_id_with_colon_and_slash_round_trips(self, client: GunSpec) -> None:
        standards = client.interfaces.list({"kind": "thread"}).data
        pick = next((s for s in standards if "/" in s["id"]), standards[0] if standards else None)
        if not pick:
            pytest.skip("no thread standards")
        assert isinstance(client.interfaces.get_firearms(pick["id"], {"per_page": 1}).data, list)


class TestSeller:
    sku = f"sdk-py-int-{int(time.time() * 1000)}"

    def test_dev_key_acts_for_dev_shop(self, client: GunSpec) -> None:
        shops = client.vendor.shops().data
        assert shops and isinstance(shops[0]["id"], str) and isinstance(shops[0]["approved"], bool)

    def test_push_read_patch_public_withdraw(self, client: GunSpec, firearm_id: str) -> None:
        push = client.vendor.push_offers(
            {
                "offers": [
                    {
                        "sku": self.sku,
                        "firearm_id": firearm_id,
                        "price_cents": 129900,
                        "currency": "AUD",
                        "url": "https://dev-shop.example/x",
                        "in_stock": True,
                    }
                ]
            }
        ).data
        assert push["written"] == 1 and push["unmatched"] == []
        try:
            row = next(o for o in client.vendor.list_offers({"q": self.sku}).data if o["sku"] == self.sku)
            assert (
                row["targetKind"] == "firearm"
                and row["targetId"] == firearm_id
                and row["priceCents"] == 129900
            )
            assert (
                client.vendor.update_offer(self.sku, {"price_cents": 119900, "status": "published"}).data[
                    "sku"
                ]
                == self.sku
            )
            mine: Any = next(
                (o for o in client.firearms.get_offers(firearm_id).data if o["sku"] == self.sku), None
            )
            assert mine and mine["priceCents"] == 119900
            if mine.get("clickId"):
                assert client.vendor.click_url(mine["clickId"]) == f"{BASE_URL}/v1/out/{mine['clickId']}"
                assert client.vendor.resolve_click(mine["clickId"]) == "https://dev-shop.example/x"
        finally:
            assert client.vendor.delete_offer(self.sku).data["removed"] is True

    def test_unmatched_reported_and_float_price_refused(self, client: GunSpec, firearm_id: str) -> None:
        push = client.vendor.push_offers(
            {
                "offers": [
                    {
                        "sku": f"{self.sku}-x",
                        "firearm_id": "no-such-firearm-xyz",
                        "price_cents": 100,
                        "currency": "AUD",
                        "url": "https://dev-shop.example/y",
                    }
                ]
            }
        ).data
        assert push["written"] == 0 and push["unmatched"][0]["targetId"] == "no-such-firearm-xyz"
        with pytest.raises(BadRequestError):
            client.vendor.push_offers(
                {
                    "offers": [
                        {
                            "sku": f"{self.sku}-f",
                            "firearm_id": firearm_id,
                            "price_cents": 10.5,
                            "currency": "AUD",
                            "url": "https://dev-shop.example/z",
                        }
                    ]
                }
            )


class TestAccount:
    def test_favorites_add_remove_ids(self, client: GunSpec, firearm_id: str) -> None:
        had = firearm_id in client.favorites.list_ids().data["ids"]
        assert client.favorites.add(firearm_id).data == {"firearmId": firearm_id, "favorited": True}
        assert firearm_id in client.favorites.list_ids().data["ids"]
        assert client.favorites.remove(firearm_id).data == {"firearmId": firearm_id, "favorited": False}
        assert firearm_id not in client.favorites.list_ids().data["ids"]
        if had:
            client.favorites.add(firearm_id)

    def test_usage(self, client: GunSpec) -> None:
        assert isinstance(client.usage.get().data, dict)

    def test_webhooks_create_test_delete(self, client: GunSpec) -> None:
        created = client.webhooks.create(
            {"url": "https://example.com/gunspec-sdk-py-int", "events": ["firearm.updated"]}
        )
        endpoint_id = created.data["id"]
        try:
            assert any(e["id"] == endpoint_id for e in client.webhooks.list().data)
            assert isinstance(client.webhooks.test(endpoint_id).data, dict)
        finally:
            client.webhooks.delete(endpoint_id)


class TestErrorReasons:
    def test_no_key(self, firearm_id: str) -> None:
        anon = GunSpec(api_key=None, base_url=BASE_URL, retry=NO_RETRY)
        with pytest.raises(AuthenticationError) as exc:
            anon.firearms.get(firearm_id)
        assert exc.value.reason in ("AUTH_REQUIRED", "KEY_MISSING")
        assert exc.value.action

    def test_wrong_key(self, firearm_id: str) -> None:
        bad = GunSpec(api_key=f"{API_KEY}-wrong", base_url=BASE_URL, retry=NO_RETRY)
        with pytest.raises(AuthenticationError) as exc:
            bad.firearms.get(firearm_id)
        assert exc.value.reason == "KEY_INVALID"

    def test_unknown_id(self, client: GunSpec) -> None:
        with pytest.raises(NotFoundError) as exc:
            client.firearms.get("no-such-firearm-xyz")
        assert exc.value.reason == "RESOURCE_NOT_FOUND" and exc.value.request_id

    def test_bad_parameter(self, client: GunSpec) -> None:
        with pytest.raises(BadRequestError) as exc:
            client.firearms.list({"per_page": 100000})
        assert exc.value.reason in ("INVALID_PARAMETER", "INVALID_REQUEST")

    def test_seller_write_on_unknown_sku_is_typed(self, client: GunSpec) -> None:
        with pytest.raises((NotFoundError, PermissionDeniedError)) as exc:
            client.vendor.update_offer("no-such-sku-xyz", {"price_cents": 1})
        assert isinstance(exc.value.reason, str)


class TestAuthAndTransport:
    def test_bearer_accepted(self, firearm_id: str) -> None:
        bearer = GunSpec(api_key=API_KEY, base_url=BASE_URL, auth_scheme="bearer", retry=NO_RETRY)
        assert bearer.firearms.get(firearm_id).data["id"] == firearm_id

    def test_http_localhost_allowed_remote_refused(self) -> None:
        GunSpec(api_key=API_KEY, base_url=BASE_URL).close()
        with pytest.raises(ConfigurationError):
            GunSpec(api_key=API_KEY, base_url="http://api.example.com")


class TestExactShapes:
    """One real response per resource family, asserted on its keys, so a
    renamed field on the API is caught here rather than by a customer."""

    def test_firearm_detail_keys(self, client: GunSpec, firearm_id: str) -> None:
        data = client.firearms.get(firearm_id).data
        assert {"id", "name", "version", "updatedAt", "manufacturerId", "categoryId"} <= set(data)
        assert isinstance(data["provenance"]["sources"], list)
        assert [s["url"] for s in data["provenance"]["sourceKinds"]] == data["provenance"]["sources"]
        assert all(s["kind"] in SOURCE_KINDS for s in data["provenance"]["sourceKinds"])
        if data["provenance"]["sources"]:
            assert data["provenance"]["bestSourceKind"] in SOURCE_KINDS
        else:
            assert data["provenance"]["bestSourceKind"] is None
        assert data["provenance"]["version"] == data["version"]
        detail = FirearmDetail.model_validate(data)
        assert detail.provenance is not None
        assert [c.url for c in detail.provenance.source_kinds] == data["provenance"]["sources"]
        assert detail.provenance.best_source_kind == data["provenance"]["bestSourceKind"]

    def test_caliber_carries_provenance(self, client: GunSpec) -> None:
        row = client.calibers.list({"per_page": 1}).data[0]
        data = client.calibers.get(row["id"]).data
        assert isinstance(data["provenance"]["sources"], list)
        Caliber.model_validate(data)

    def test_firearm_list_row_keys(self, client: GunSpec) -> None:
        row = client.firearms.list({"per_page": 1}).data[0]
        assert {"id", "name", "updatedAt", "version"} <= set(row)

    def test_attachment_detail_keys(self, client: GunSpec, attachment_id: str) -> None:
        if not attachment_id:
            pytest.skip("no attachments seeded")
        data = client.attachments.get(attachment_id).data
        assert {"id", "name", "category", "requires", "provides", "caliberRatings", "version"} <= set(data)

    def test_interface_and_platform_keys(self, client: GunSpec) -> None:
        standard = client.interfaces.list().data[0]
        assert {"id", "kind", "name", "aliases"} <= set(standard)
        platforms = client.platforms.list().data
        if platforms:
            assert {"id", "name", "memberCount"} <= set(platforms[0])

    def test_vendor_offer_row_keys(self, client: GunSpec, firearm_id: str) -> None:
        sku = f"sdk-py-shape-{int(time.time() * 1000)}"
        client.vendor.push_offers(
            {
                "offers": [
                    {
                        "sku": sku,
                        "firearm_id": firearm_id,
                        "price_cents": 1000,
                        "currency": "AUD",
                        "url": "https://dev-shop.example/shape",
                    }
                ]
            }
        )
        try:
            row = next(o for o in client.vendor.list_offers({"q": sku}).data if o["sku"] == sku)
            assert {
                "sku",
                "targetKind",
                "targetId",
                "priceCents",
                "currency",
                "url",
                "inStock",
                "stockQty",
                "status",
                "clicks",
                "updatedAt",
            } <= set(row)
            shop = client.vendor.shops().data[0]
            assert {"id", "name", "approved"} <= set(shop)
        finally:
            client.vendor.delete_offer(sku)

    def test_public_offer_keys(self, client: GunSpec, firearm_id: str) -> None:
        for offer in client.firearms.get_offers(firearm_id).data:
            assert {"vendor", "sku", "priceCents", "currency", "url", "inStock", "clickId"} <= set(offer)

    def test_media_and_resolve_keys(self, client: GunSpec, firearm_id: str) -> None:
        for m in client.firearms.list_media(firearm_id).data:
            assert {"kind", "url", "credit"} <= set(m)
        resolved = client.firearms.resolve("Glock 19").data
        assert {"query", "status", "firearmId", "score", "alternatives"} <= set(resolved)

    def test_manufacturer_caliber_category_keys(self, client: GunSpec) -> None:
        assert {"id", "name"} <= set(client.manufacturers.list({"per_page": 1}).data[0])
        assert {"id", "name"} <= set(client.calibers.list({"per_page": 1}).data[0])
        assert {"id", "name"} <= set(client.categories.list().data[0])

    def test_favorites_usage_webhook_keys(self, client: GunSpec, firearm_id: str) -> None:
        assert set(client.favorites.list_ids().data) == {"ids"}
        assert isinstance(client.usage.get().data, dict)
        created = client.webhooks.create(
            {"url": "https://example.com/gunspec-sdk-py-shape", "events": ["firearm.updated"]}
        )
        try:
            assert {"id", "url", "events"} <= set(created.data)
        finally:
            client.webhooks.delete(created.data["id"])

    def test_error_body_has_reason_and_request_id(self, client: GunSpec) -> None:
        with pytest.raises(NotFoundError) as exc:
            client.firearms.get("no-such-firearm-xyz")
        err = exc.value
        assert err.request_id and err.reason == "RESOURCE_NOT_FOUND"
        assert (
            str(err) == f"NotFoundError(404 RESOURCE_NOT_FOUND): {err.message} [request_id={err.request_id}]"
        )
        assert "headers" not in repr(err)

    def test_client_repr_masks_key(self, client: GunSpec) -> None:
        text = repr(client)
        assert API_KEY not in text
        assert text.startswith("GunSpec(SyncHttpClient(base_url=")
        assert "etag_cache=False" in text
