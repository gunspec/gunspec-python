"""Tests for the Firearms and AsyncFirearms resource classes."""

from __future__ import annotations

from urllib.parse import quote

from gunspec._resources._firearms import AsyncFirearms, Firearms


class TestFirearms:
    """Sync Firearms resource tests."""

    def test_list(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"page": 1, "limit": 10}
        resource.list(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms", query=params)

    def test_list_no_params(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.list()
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms", query=None)

    def test_search(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"q": "glock"}
        resource.search(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/search", query=params)

    def test_compare(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"ids": "glock-g17,sig-p320"}
        resource.compare(params)
        mock_sync_client.get.assert_called_once_with("/v1/firearms/compare", query=params)

    def test_game_meta(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"category": "pistol"}
        resource.game_meta(params)
        mock_sync_client.get.assert_called_once_with("/v1/firearms/game-meta", query=params)

    def test_action_types(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.action_types()
        mock_sync_client.get.assert_called_once_with("/v1/firearms/action-types")

    def test_filter_options(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.filter_options()
        mock_sync_client.get.assert_called_once_with("/v1/firearms/filter-options")

    def test_random(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"count": 5}
        resource.random(params)
        mock_sync_client.get.assert_called_once_with("/v1/firearms/random", query=params)

    def test_top(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"metric": "popularity", "limit": 10}
        resource.top(params)
        mock_sync_client.get.assert_called_once_with("/v1/firearms/top", query=params)

    def test_head_to_head(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"a": "glock-g17", "b": "sig-p320"}
        resource.head_to_head(params)
        mock_sync_client.get.assert_called_once_with("/v1/firearms/head-to-head", query=params)

    def test_by_feature(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"feature": "rail"}
        resource.by_feature(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/by-feature", query=params)

    def test_by_action(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"action": "semi-automatic"}
        resource.by_action(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/by-action", query=params)

    def test_by_material(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"material": "polymer"}
        resource.by_material(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/by-material", query=params)

    def test_by_designer(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"designer": "John Browning"}
        resource.by_designer(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/by-designer", query=params)

    def test_power_rating(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"min": 5}
        resource.power_rating(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/power-rating", query=params)

    def test_timeline(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"start": 1900, "end": 2000}
        resource.timeline(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/timeline", query=params)

    def test_by_conflict(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"conflict": "ww2"}
        resource.by_conflict(params)
        mock_sync_client.get_paginated.assert_called_once_with("/v1/firearms/by-conflict", query=params)

    def test_get(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}")

    def test_get_variants(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_variants("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/variants")

    def test_get_images(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_images("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/images")

    def test_get_game_stats(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_game_stats("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/game-stats")

    def test_get_dimensions(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_dimensions("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/dimensions")

    def test_get_users(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_users("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/users")

    def test_get_family_tree(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_family_tree("glock-g17")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/family-tree"
        )

    def test_get_similar(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_similar("glock-g17")
        mock_sync_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/similar")

    def test_get_adoption_map(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_adoption_map("glock-g17")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/adoption-map"
        )

    def test_get_game_profile(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_game_profile("glock-g17")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/game-profile"
        )

    def test_get_silhouette(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"format": "svg"}
        resource.get_silhouette("glock-g17", params)
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/silhouette", query=params
        )

    def test_get_silhouette_no_params(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        resource.get_silhouette("glock-g17")
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/silhouette", query=None
        )

    def test_calculate(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"range": 100}
        resource.calculate("glock-g17", params)
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/calculate", query=params
        )

    def test_load(self, mock_sync_client):
        resource = Firearms(mock_sync_client)
        params = {"type": "full"}
        resource.load("glock-g17", params)
        mock_sync_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/load", query=params
        )


class TestAsyncFirearms:
    """Async Firearms resource tests."""

    async def test_list(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"page": 1, "limit": 10}
        await resource.list(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms", query=params)

    async def test_list_no_params(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.list()
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms", query=None)

    async def test_search(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"q": "glock"}
        await resource.search(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/search", query=params)

    async def test_compare(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"ids": "glock-g17,sig-p320"}
        await resource.compare(params)
        mock_async_client.get.assert_called_once_with("/v1/firearms/compare", query=params)

    async def test_game_meta(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"category": "pistol"}
        await resource.game_meta(params)
        mock_async_client.get.assert_called_once_with("/v1/firearms/game-meta", query=params)

    async def test_action_types(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.action_types()
        mock_async_client.get.assert_called_once_with("/v1/firearms/action-types")

    async def test_filter_options(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.filter_options()
        mock_async_client.get.assert_called_once_with("/v1/firearms/filter-options")

    async def test_random(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"count": 5}
        await resource.random(params)
        mock_async_client.get.assert_called_once_with("/v1/firearms/random", query=params)

    async def test_top(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"metric": "popularity", "limit": 10}
        await resource.top(params)
        mock_async_client.get.assert_called_once_with("/v1/firearms/top", query=params)

    async def test_head_to_head(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"a": "glock-g17", "b": "sig-p320"}
        await resource.head_to_head(params)
        mock_async_client.get.assert_called_once_with("/v1/firearms/head-to-head", query=params)

    async def test_by_feature(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"feature": "rail"}
        await resource.by_feature(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/by-feature", query=params)

    async def test_by_action(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"action": "semi-automatic"}
        await resource.by_action(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/by-action", query=params)

    async def test_by_material(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"material": "polymer"}
        await resource.by_material(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/by-material", query=params)

    async def test_by_designer(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"designer": "John Browning"}
        await resource.by_designer(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/by-designer", query=params)

    async def test_power_rating(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"min": 5}
        await resource.power_rating(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/power-rating", query=params)

    async def test_timeline(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"start": 1900, "end": 2000}
        await resource.timeline(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/timeline", query=params)

    async def test_by_conflict(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"conflict": "ww2"}
        await resource.by_conflict(params)
        mock_async_client.get_paginated.assert_called_once_with("/v1/firearms/by-conflict", query=params)

    async def test_get(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get("glock-g17")
        mock_async_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}")

    async def test_get_variants(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_variants("glock-g17")
        mock_async_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/variants")

    async def test_get_images(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_images("glock-g17")
        mock_async_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/images")

    async def test_get_game_stats(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_game_stats("glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/game-stats"
        )

    async def test_get_dimensions(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_dimensions("glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/dimensions"
        )

    async def test_get_users(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_users("glock-g17")
        mock_async_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/users")

    async def test_get_family_tree(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_family_tree("glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/family-tree"
        )

    async def test_get_similar(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_similar("glock-g17")
        mock_async_client.get.assert_called_once_with(f"/v1/firearms/{quote('glock-g17', safe='')}/similar")

    async def test_get_adoption_map(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_adoption_map("glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/adoption-map"
        )

    async def test_get_game_profile(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_game_profile("glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/game-profile"
        )

    async def test_get_silhouette(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"format": "svg"}
        await resource.get_silhouette("glock-g17", params)
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/silhouette", query=params
        )

    async def test_get_silhouette_no_params(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        await resource.get_silhouette("glock-g17")
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/silhouette", query=None
        )

    async def test_calculate(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"range": 100}
        await resource.calculate("glock-g17", params)
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/calculate", query=params
        )

    async def test_load(self, mock_async_client):
        resource = AsyncFirearms(mock_async_client)
        params = {"type": "full"}
        await resource.load("glock-g17", params)
        mock_async_client.get.assert_called_once_with(
            f"/v1/firearms/{quote('glock-g17', safe='')}/load", query=params
        )
