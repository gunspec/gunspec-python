from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import (
    ActionTypesParams,
    AdoptionByCountryParams,
    AdoptionByTypeParams,
    ByEraParams,
    CaliberPopularityByEraParams,
    FeatureFrequencyParams,
    PopularCalibersParams,
    ProlificManufacturersParams,
)

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, SyncHttpClient


class Stats:
    """Sync statistics resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def summary(self) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/stats/summary")

    def production_status(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/production-status")

    def catalog_coverage(self) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/stats/catalog-coverage")

    def field_coverage(self) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/stats/field-coverage")

    def popular_calibers(
        self, params: Optional[PopularCalibersParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/calibers/popular", query=params)

    def prolific_manufacturers(
        self, params: Optional[ProlificManufacturersParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/manufacturers/prolific", query=params)

    def by_category(self) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/by-category")

    def by_era(self, params: ByEraParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/stats/by-era", query=params)

    def materials(self) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/stats/materials")

    def adoption_by_country(self, params: AdoptionByCountryParams) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/adoption/by-country", query=params)

    def adoption_by_type(self, params: AdoptionByTypeParams) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/adoption/by-type", query=params)

    def action_types(self, params: Optional[ActionTypesParams] = None) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/action-types", query=params)

    def feature_frequency(
        self, params: Optional[FeatureFrequencyParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/feature-frequency", query=params)

    def caliber_popularity_by_era(
        self, params: Optional[CaliberPopularityByEraParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/stats/caliber-popularity-by-era", query=params)


class AsyncStats:
    """Async statistics resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def summary(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/stats/summary")

    async def production_status(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/production-status")

    async def catalog_coverage(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/stats/catalog-coverage")

    async def field_coverage(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/stats/field-coverage")

    async def popular_calibers(
        self, params: Optional[PopularCalibersParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/calibers/popular", query=params)

    async def prolific_manufacturers(
        self, params: Optional[ProlificManufacturersParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/manufacturers/prolific", query=params)

    async def by_category(self) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/by-category")

    async def by_era(self, params: ByEraParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/stats/by-era", query=params)

    async def materials(self) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/stats/materials")

    async def adoption_by_country(self, params: AdoptionByCountryParams) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/adoption/by-country", query=params)

    async def adoption_by_type(self, params: AdoptionByTypeParams) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/adoption/by-type", query=params)

    async def action_types(
        self, params: Optional[ActionTypesParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/action-types", query=params)

    async def feature_frequency(
        self, params: Optional[FeatureFrequencyParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/feature-frequency", query=params)

    async def caliber_popularity_by_era(
        self, params: Optional[CaliberPopularityByEraParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/stats/caliber-popularity-by-era", query=params)
