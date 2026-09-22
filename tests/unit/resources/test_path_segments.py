"""An id that is empty, ``.`` or ``..`` is refused before it reaches a path,
because httpx would resolve it and the request would go to another endpoint."""

from __future__ import annotations

import pytest

from gunspec._resources._ammunition import Ammunition
from gunspec._resources._content import AsyncContent
from gunspec._resources._firearms import AsyncFirearms, Firearms
from gunspec._resources._path import _seg
from gunspec._resources._webhooks import Webhooks

BAD = ["", ".", ".."]


class TestSeg:
    @pytest.mark.parametrize("value", BAD)
    def test_refuses_dot_and_empty_segments(self, value: str) -> None:
        with pytest.raises(ValueError, match="not a valid id"):
            _seg(value)

    def test_encodes_everything_else(self) -> None:
        assert _seg("ak-47") == "ak-47"
        assert _seg("a/b") == "a%2Fb"
        assert _seg("...") == "..."
        assert _seg("%2e%2e") == "%252e%252e"
        assert _seg(42) == "42"


@pytest.mark.parametrize("value", BAD)
class TestResourcesRefuse:
    def test_firearm_variants(self, mock_sync_client, value: str) -> None:
        with pytest.raises(ValueError):
            Firearms(mock_sync_client).get_variants(value)
        mock_sync_client.get.assert_not_called()

    def test_webhook_test(self, mock_sync_client, value: str) -> None:
        with pytest.raises(ValueError):
            Webhooks(mock_sync_client).test(value)
        mock_sync_client.post.assert_not_called()

    def test_firearm_model_download(self, mock_sync_client, value: str) -> None:
        with pytest.raises(ValueError):
            Firearms(mock_sync_client).get_model(value)
        mock_sync_client.get_bytes.assert_not_called()

    def test_media_selector(self, mock_sync_client, value: str) -> None:
        with pytest.raises(ValueError):
            Firearms(mock_sync_client).get_media("ak-47", value)
        mock_sync_client.get.assert_not_called()

    def test_bullet_svg(self, mock_sync_client, value: str) -> None:
        with pytest.raises(ValueError):
            Ammunition(mock_sync_client).get_bullet_svg(value)
        mock_sync_client.get_text.assert_not_called()

    async def test_async_firearm_get(self, mock_async_client, value: str) -> None:
        with pytest.raises(ValueError):
            await AsyncFirearms(mock_async_client).get(value)
        mock_async_client.get.assert_not_called()

    async def test_async_blog_post(self, mock_async_client, value: str) -> None:
        with pytest.raises(ValueError):
            await AsyncContent(mock_async_client).get_blog_post(value)
        mock_async_client.get.assert_not_called()
