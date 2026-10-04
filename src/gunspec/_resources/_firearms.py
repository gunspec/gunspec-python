from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, List, Mapping, Optional

from ..types import (
    AmmoLoadParams,
    ByActionParams,
    ByConflictParams,
    ByDesignerParams,
    ByFeatureParams,
    ByMaterialParams,
    CalculateBallisticsParams,
    CompareFirearmsParams,
    GameMetaParams,
    HeadToHeadParams,
    ListFirearmsParams,
    LoadCarriageParams,
    LoadFirearmParams,
    PointBlankParams,
    PowerRatingParams,
    RandomFirearmParams,
    RecoilParams,
    SearchFirearmsParams,
    SilhouetteParams,
    TimelineParams,
    TopFirearmsParams,
)
from ._firearms_extras import AsyncFirearmsExtrasMixin, FirearmsExtrasMixin
from ._path import _seg

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Firearms(FirearmsExtrasMixin):
    """Sync firearms resource.

    Name resolution, media, offers and compatibility live on the mixin in
    ``_firearms_extras.py``.
    """

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    # -- Collection endpoints --------------------------------------------------

    def list(self, params: Optional[ListFirearmsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms", query=params)

    def list_auto_paging(self, params: Optional[ListFirearmsParams] = None) -> Iterator[Dict[str, Any]]:
        page = (params or {}).get("page", 1)
        while True:
            query: Dict[str, Any] = dict(params or {})
            query["page"] = page
            result = self.list(query)  # type: ignore[arg-type]
            yield from result.data
            if not result.pagination.total_pages or page >= result.pagination.total_pages:
                break
            page += 1

    def search(self, params: SearchFirearmsParams) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/search", query=params)

    def compare(self, params: CompareFirearmsParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/firearms/compare", query=params)

    def load_carriage(self, params: LoadCarriageParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/firearms/load-carriage", query=params)

    def recoil(self, params: RecoilParams) -> APIResponse[Dict[str, Any]]:
        """Free recoil of up to 5 firearms by SAAMI's formula; a lower bound without a powder charge."""
        return self._client.get("/v1/firearms/recoil", query=params)

    def point_blank(self, params: PointBlankParams) -> APIResponse[Dict[str, Any]]:
        """Maximum point-blank range and supersonic range of up to 5 firearms."""
        return self._client.get("/v1/firearms/point-blank", query=params)

    def ammo_load(self, params: AmmoLoadParams) -> APIResponse[Dict[str, Any]]:
        """Rounds per kilogram, a weight budget and an estimated basic load for up to 5 firearms."""
        return self._client.get("/v1/firearms/ammo-load", query=params)

    def game_meta(self, params: Optional[GameMetaParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/firearms/game-meta", query=params)

    def action_types(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/firearms/action-types")

    def filter_options(self) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/firearms/filter-options")

    def random(self, params: Optional[RandomFirearmParams] = None) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/firearms/random", query=params)

    def top(self, params: TopFirearmsParams) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/firearms/top", query=params)

    def head_to_head(self, params: HeadToHeadParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/firearms/head-to-head", query=params)

    def by_feature(self, params: ByFeatureParams) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/by-feature", query=params)

    def by_action(self, params: ByActionParams) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/by-action", query=params)

    def by_material(self, params: ByMaterialParams) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/by-material", query=params)

    def by_designer(self, params: ByDesignerParams) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/by-designer", query=params)

    def power_rating(self, params: Optional[PowerRatingParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/power-rating", query=params)

    def timeline(self, params: Optional[TimelineParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/timeline", query=params)

    def by_conflict(self, params: ByConflictParams) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/firearms/by-conflict", query=params)

    # -- Single-resource endpoints ---------------------------------------------

    def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}")

    def get_variants(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/variants")

    def get_images(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/images")

    def get_game_stats(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/game-stats")

    def get_dimensions(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/dimensions")

    def get_schematics(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/schematics")

    def popular(self, params: Optional[Mapping[str, Any]] = None) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/popular/firearms", query=params)

    def get_users(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/users")

    def get_family_tree(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/family-tree")

    def get_similar(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/similar")

    def get_adoption_map(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/adoption-map")

    def get_game_profile(self, id: str) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/game-profile")

    def get_silhouette(
        self, id: str, params: Optional[SilhouetteParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/silhouette", query=params)

    def calculate(self, id: str, params: CalculateBallisticsParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/calculate", query=params)

    def load(self, id: str, params: Optional[LoadFirearmParams] = None) -> APIResponse[Dict[str, Any]]:
        return self._client.get(f"/v1/firearms/{_seg(id)}/load", query=params)


class AsyncFirearms(AsyncFirearmsExtrasMixin):
    """Async firearms resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    # -- Collection endpoints --------------------------------------------------

    async def list(self, params: Optional[ListFirearmsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms", query=params)

    async def list_auto_paging(
        self, params: Optional[ListFirearmsParams] = None
    ) -> AsyncIterator[Dict[str, Any]]:
        page = (params or {}).get("page", 1)
        while True:
            query: Dict[str, Any] = dict(params or {})
            query["page"] = page
            result = await self.list(query)  # type: ignore[arg-type]
            for item in result.data:
                yield item
            if not result.pagination.total_pages or page >= result.pagination.total_pages:
                break
            page += 1

    async def search(self, params: SearchFirearmsParams) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/search", query=params)

    async def compare(self, params: CompareFirearmsParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/firearms/compare", query=params)

    async def load_carriage(self, params: LoadCarriageParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/firearms/load-carriage", query=params)

    async def recoil(self, params: RecoilParams) -> APIResponse[Dict[str, Any]]:
        """Free recoil of up to 5 firearms by SAAMI's formula; a lower bound without a powder charge."""
        return await self._client.get("/v1/firearms/recoil", query=params)

    async def point_blank(self, params: PointBlankParams) -> APIResponse[Dict[str, Any]]:
        """Maximum point-blank range and supersonic range of up to 5 firearms."""
        return await self._client.get("/v1/firearms/point-blank", query=params)

    async def ammo_load(self, params: AmmoLoadParams) -> APIResponse[Dict[str, Any]]:
        """Rounds per kilogram, a weight budget and an estimated basic load for up to 5 firearms."""
        return await self._client.get("/v1/firearms/ammo-load", query=params)

    async def game_meta(self, params: Optional[GameMetaParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/firearms/game-meta", query=params)

    async def action_types(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/firearms/action-types")

    async def filter_options(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/firearms/filter-options")

    async def random(self, params: Optional[RandomFirearmParams] = None) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/firearms/random", query=params)

    async def top(self, params: TopFirearmsParams) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/firearms/top", query=params)

    async def head_to_head(self, params: HeadToHeadParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/firearms/head-to-head", query=params)

    async def by_feature(self, params: ByFeatureParams) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/by-feature", query=params)

    async def by_action(self, params: ByActionParams) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/by-action", query=params)

    async def by_material(self, params: ByMaterialParams) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/by-material", query=params)

    async def by_designer(self, params: ByDesignerParams) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/by-designer", query=params)

    async def power_rating(
        self, params: Optional[PowerRatingParams] = None
    ) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/power-rating", query=params)

    async def timeline(self, params: Optional[TimelineParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/timeline", query=params)

    async def by_conflict(self, params: ByConflictParams) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/firearms/by-conflict", query=params)

    # -- Single-resource endpoints ---------------------------------------------

    async def get(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}")

    async def get_variants(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/variants")

    async def get_images(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/images")

    async def get_game_stats(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/game-stats")

    async def get_dimensions(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/dimensions")

    async def get_schematics(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/schematics")

    async def popular(self, params: Optional[Mapping[str, Any]] = None) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/popular/firearms", query=params)

    async def get_users(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/users")

    async def get_family_tree(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/family-tree")

    async def get_similar(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/similar")

    async def get_adoption_map(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/adoption-map")

    async def get_game_profile(self, id: str) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/game-profile")

    async def get_silhouette(
        self, id: str, params: Optional[SilhouetteParams] = None
    ) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/silhouette", query=params)

    async def calculate(self, id: str, params: CalculateBallisticsParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/calculate", query=params)

    async def load(self, id: str, params: Optional[LoadFirearmParams] = None) -> APIResponse[Dict[str, Any]]:
        return await self._client.get(f"/v1/firearms/{_seg(id)}/load", query=params)
