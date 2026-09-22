"""Name resolution, media, offers and compatibility methods for the firearms
resource, as mixins so ``_firearms.py`` stays a table of contents.

Every method here builds its path from ``_slug(id)``, which the reference
generator cannot read out of the source, so each states its own endpoint with
``@endpoint``, the same tag the TypeScript SDK uses. Without it the generator
drops the method, and the docs then tell a Python reader it does not exist.
``scripts/sdk-python-reference.py`` reads the tag; the docs test asserts every
TypeScript method has a Python counterpart or a note saying why not."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..types import (
    FirearmAttachmentsParams,
    GetFirearmMediaParams,
    ImageAssetParams,
    ListFirearmMediaParams,
    MediaCatalogParams,
    OffersParams,
)
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import (
        APIResponse,
        AsyncHttpClient,
        PaginatedResponse,
        RawResponse,
        SyncHttpClient,
    )


def _slug(id: str) -> str:
    return f"/v1/firearms/{_seg(id)}"


class FirearmsExtrasMixin:
    """Sync extras. Expects ``self._client`` to be a ``SyncHttpClient``."""

    _client: SyncHttpClient

    # -- Name resolution -------------------------------------------------------

    def resolve(self, q: str) -> APIResponse[Dict[str, Any]]:
        """Resolve one free-text name ("G19 gen 5") to a firearm id. Builder."""
        return self._client.get("/v1/firearms/resolve", query={"q": q})

    def resolve_many(self, queries: List[str]) -> APIResponse[Dict[str, Any]]:
        """Resolve many names in one call. Studio."""
        return self._client.post("/v1/firearms/resolve", body={"queries": queries})

    # -- Media -----------------------------------------------------------------

    def media_catalog(self, params: Optional[MediaCatalogParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        """Every firearm that has imagery, one row each."""
        return self._client.get_paginated("/v1/firearms/media", query=params)

    def list_media(
        self, id: str, params: Optional[ListFirearmMediaParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        """Every asset on one firearm, with credit and derivative sizes.

        @endpoint GET /v1/firearms/{id}/media
        """
        return self._client.get(f"{_slug(id)}/media", query=params)

    def get_media(
        self, id: str, selector: Union[str, int], params: Optional[GetFirearmMediaParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        """Metadata for one asset, by kind or by row id. Builder.

        @endpoint GET /v1/firearms/{id}/media/{selector}
        """
        return self._client.get(
            f"{_slug(id)}/media/{_seg(selector)}",
            query={**(params or {}), "format": "json"},
        )

    def download_media(
        self, id: str, selector: Union[str, int], params: Optional[GetFirearmMediaParams] = None
    ) -> RawResponse:
        """The bytes of one asset, following the redirect to the CDN. Builder.

        @endpoint GET /v1/firearms/{id}/media/{selector}
        """
        return self._client.get_bytes(
            f"{_slug(id)}/media/{_seg(selector)}",
            query={**(params or {}), "format": "raw"},
        )

    def get_image_asset(
        self, id: str, image_id: Union[str, int], params: Optional[ImageAssetParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        """One image as a base64 data URI. Builder.

        @endpoint GET /v1/firearms/{id}/images/{imageId}
        """
        return self._client.get(
            f"{_slug(id)}/images/{_seg(image_id)}",
            query={**(params or {}), "format": "datauri"},
        )

    def get_model(self, id: str) -> RawResponse:
        """The 3D model as GLB bytes. Builder.

        @endpoint GET /v1/firearms/{id}/model
        """
        return self._client.get_bytes(f"{_slug(id)}/model")

    # -- Sellers and compatibility ---------------------------------------------

    def get_offers(self, id: str, params: Optional[OffersParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        """Sellers stocking this firearm; link out through ``vendor.click_url``.

        @endpoint GET /v1/firearms/{id}/offers
        """
        return self._client.get(f"{_slug(id)}/offers", query=params)

    def get_interfaces(self, id: str) -> APIResponse[Dict[str, Any]]:
        """The mount interfaces a firearm exposes. Studio.

        @endpoint GET /v1/firearms/{id}/interfaces
        """
        return self._client.get(f"{_slug(id)}/interfaces")

    def get_attachments(
        self, id: str, params: Optional[FirearmAttachmentsParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        """Attachments that fit, grouped by category, with the evidence. Studio.

        @endpoint GET /v1/firearms/{id}/attachments
        """
        return self._client.get(f"{_slug(id)}/attachments", query=params)


class AsyncFirearmsExtrasMixin:
    """Async extras. Expects ``self._client`` to be an ``AsyncHttpClient``."""

    _client: AsyncHttpClient

    async def resolve(self, q: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/firearms/resolve", query={"q": q})

    async def resolve_many(self, queries: List[str]) -> APIResponse[Dict[str, Any]]:
        return await self._client.post("/v1/firearms/resolve", body={"queries": queries})

    async def media_catalog(
        self, params: Optional[MediaCatalogParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/media", query=params)

    async def list_media(
        self, id: str, params: Optional[ListFirearmMediaParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"{_slug(id)}/media", query=params)

    async def get_media(
        self, id: str, selector: Union[str, int], params: Optional[GetFirearmMediaParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(
            f"{_slug(id)}/media/{_seg(selector)}",
            query={**(params or {}), "format": "json"},
        )

    async def download_media(
        self, id: str, selector: Union[str, int], params: Optional[GetFirearmMediaParams] = None
    ) -> RawResponse:
        return await self._client.get_bytes(
            f"{_slug(id)}/media/{_seg(selector)}",
            query={**(params or {}), "format": "raw"},
        )

    async def get_image_asset(
        self, id: str, image_id: Union[str, int], params: Optional[ImageAssetParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(
            f"{_slug(id)}/images/{_seg(image_id)}",
            query={**(params or {}), "format": "datauri"},
        )

    async def get_model(self, id: str) -> RawResponse:
        return await self._client.get_bytes(f"{_slug(id)}/model")

    async def get_offers(
        self, id: str, params: Optional[OffersParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"{_slug(id)}/offers", query=params)

    async def get_interfaces(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"{_slug(id)}/interfaces")

    async def get_attachments(
        self, id: str, params: Optional[FirearmAttachmentsParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"{_slug(id)}/attachments", query=params)
