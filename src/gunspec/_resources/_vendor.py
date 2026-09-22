from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import quote

from ..types import ListVendorOffersParams, PushOffersInput, UpdateOfferInput, VendorScope

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Vendor:
    """Sync vendor (seller) resource.

    Wraps ``/v1/vendor/*`` and the outbound click route. A seller holds an
    Enterprise plan and names one of their ordinary keys in Profile > Seller;
    that mapping is the whole vendor scope. A key no shop names answers 403
    ``KEY_NOT_LINKED_TO_SHOP``.
    """

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def shops(self) -> APIResponse[List[Dict[str, Any]]]:
        """The shops this key may act for."""
        return self._client.get("/v1/vendor/shops")

    def list_offers(
        self, params: Optional[ListVendorOffersParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        """Your listings as the API holds them, ``stockQty`` and clicks included."""
        return self._client.get_paginated("/v1/vendor/offers", query=params)

    def push_offers(
        self, body: PushOffersInput, scope: Optional[PushOffersInput] = None
    ) -> APIResponse[Dict[str, Any]]:
        """Upsert up to 500 listings keyed by your SKU. Unknown ids come back as ``unmatched``."""
        return self._client.put("/v1/vendor/offers", body=body, query=scope)

    def update_offer(
        self, sku: str, body: UpdateOfferInput, scope: Optional[UpdateOfferInput] = None
    ) -> APIResponse[Dict[str, Any]]:
        """Change one listing. Absent fields are unchanged."""
        return self._client.patch(f"/v1/vendor/offers/{quote(sku, safe='')}", body=body, query=scope)

    def delete_offer(self, sku: str, scope: Optional[VendorScope] = None) -> APIResponse[Dict[str, Any]]:
        """Withdraw one listing."""
        return self._client.delete(f"/v1/vendor/offers/{quote(sku, safe='')}", query=scope)

    def click_url(self, click_id: str, locale: Optional[str] = None) -> str:
        """The tracked outbound link for an offer's ``clickId``. Render this as
        the href: the API counts the visit and 302s to the shop, so the seller
        can check our figure against their own analytics.

        Builds the URL rather than fetching it, since the reader's browser makes
        the request, but it is still that endpoint, and the reference documents
        the pair together.

        @endpoint GET /v1/out/{clickId}
        """
        return self._client.url_for(f"/v1/out/{quote(click_id, safe='')}", {"l": locale} if locale else None)

    def resolve_click(self, click_id: str) -> Optional[str]:
        """Follow a click server-side and return the shop URL. Counts as a visit.

        @endpoint GET /v1/out/{clickId}
        """
        return self._client.resolve_redirect(f"/v1/out/{quote(click_id, safe='')}")


class AsyncVendor:
    """Async vendor (seller) resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def shops(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/vendor/shops")

    async def list_offers(
        self, params: Optional[ListVendorOffersParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/vendor/offers", query=params)

    async def push_offers(
        self, body: PushOffersInput, scope: Optional[PushOffersInput] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.put("/v1/vendor/offers", body=body, query=scope)

    async def update_offer(
        self, sku: str, body: UpdateOfferInput, scope: Optional[UpdateOfferInput] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.patch(f"/v1/vendor/offers/{quote(sku, safe='')}", body=body, query=scope)

    async def delete_offer(
        self, sku: str, scope: Optional[VendorScope] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.delete(f"/v1/vendor/offers/{quote(sku, safe='')}", query=scope)

    def click_url(self, click_id: str, locale: Optional[str] = None) -> str:
        return self._client.url_for(f"/v1/out/{quote(click_id, safe='')}", {"l": locale} if locale else None)

    async def resolve_click(self, click_id: str) -> Optional[str]:
        return await self._client.resolve_redirect(f"/v1/out/{quote(click_id, safe='')}")
