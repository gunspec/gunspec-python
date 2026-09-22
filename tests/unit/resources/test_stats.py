"""Tests for the Stats and AsyncStats resource classes."""

from __future__ import annotations

from gunspec._resources._stats import AsyncStats, Stats


class TestStats:
    """Sync Stats resource tests."""

    def test_summary(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.summary()
        mock_sync_client.get.assert_called_once_with("/v1/stats/summary")

    def test_production_status(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.production_status()
        mock_sync_client.get.assert_called_once_with("/v1/stats/production-status")

    def test_field_coverage(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.field_coverage()
        mock_sync_client.get.assert_called_once_with("/v1/stats/field-coverage")

    def test_popular_calibers(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"limit": 10}
        resource.popular_calibers(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/calibers/popular", query=params)

    def test_popular_calibers_no_params(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.popular_calibers()
        mock_sync_client.get.assert_called_once_with("/v1/stats/calibers/popular", query=None)

    def test_prolific_manufacturers(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"limit": 5}
        resource.prolific_manufacturers(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/manufacturers/prolific", query=params)

    def test_prolific_manufacturers_no_params(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.prolific_manufacturers()
        mock_sync_client.get.assert_called_once_with("/v1/stats/manufacturers/prolific", query=None)

    def test_by_category(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.by_category()
        mock_sync_client.get.assert_called_once_with("/v1/stats/by-category")

    def test_by_era(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"era": "modern"}
        resource.by_era(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/by-era", query=params)

    def test_materials(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.materials()
        mock_sync_client.get.assert_called_once_with("/v1/stats/materials")

    def test_adoption_by_country(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"country": "US"}
        resource.adoption_by_country(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/adoption/by-country", query=params)

    def test_adoption_by_type(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"type": "military"}
        resource.adoption_by_type(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/adoption/by-type", query=params)

    def test_action_types(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"category": "pistol"}
        resource.action_types(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/action-types", query=params)

    def test_action_types_no_params(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.action_types()
        mock_sync_client.get.assert_called_once_with("/v1/stats/action-types", query=None)

    def test_feature_frequency(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"min_count": 5}
        resource.feature_frequency(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/feature-frequency", query=params)

    def test_feature_frequency_no_params(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.feature_frequency()
        mock_sync_client.get.assert_called_once_with("/v1/stats/feature-frequency", query=None)

    def test_caliber_popularity_by_era(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        params = {"era": "cold-war"}
        resource.caliber_popularity_by_era(params)
        mock_sync_client.get.assert_called_once_with("/v1/stats/caliber-popularity-by-era", query=params)

    def test_caliber_popularity_by_era_no_params(self, mock_sync_client):
        resource = Stats(mock_sync_client)
        resource.caliber_popularity_by_era()
        mock_sync_client.get.assert_called_once_with("/v1/stats/caliber-popularity-by-era", query=None)


class TestAsyncStats:
    """Async Stats resource tests."""

    async def test_summary(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        await resource.summary()
        mock_async_client.get.assert_called_once_with("/v1/stats/summary")

    async def test_production_status(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        await resource.production_status()
        mock_async_client.get.assert_called_once_with("/v1/stats/production-status")

    async def test_field_coverage(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        await resource.field_coverage()
        mock_async_client.get.assert_called_once_with("/v1/stats/field-coverage")

    async def test_popular_calibers(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"limit": 10}
        await resource.popular_calibers(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/calibers/popular", query=params)

    async def test_prolific_manufacturers(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"limit": 5}
        await resource.prolific_manufacturers(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/manufacturers/prolific", query=params)

    async def test_by_category(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        await resource.by_category()
        mock_async_client.get.assert_called_once_with("/v1/stats/by-category")

    async def test_by_era(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"era": "modern"}
        await resource.by_era(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/by-era", query=params)

    async def test_materials(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        await resource.materials()
        mock_async_client.get.assert_called_once_with("/v1/stats/materials")

    async def test_adoption_by_country(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"country": "US"}
        await resource.adoption_by_country(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/adoption/by-country", query=params)

    async def test_adoption_by_type(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"type": "military"}
        await resource.adoption_by_type(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/adoption/by-type", query=params)

    async def test_action_types(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"category": "pistol"}
        await resource.action_types(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/action-types", query=params)

    async def test_feature_frequency(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"min_count": 5}
        await resource.feature_frequency(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/feature-frequency", query=params)

    async def test_caliber_popularity_by_era(self, mock_async_client):
        resource = AsyncStats(mock_async_client)
        params = {"era": "cold-war"}
        await resource.caliber_popularity_by_era(params)
        mock_async_client.get.assert_called_once_with("/v1/stats/caliber-popularity-by-era", query=params)
