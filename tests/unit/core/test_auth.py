"""Tests for gunspec._core._auth - API key resolution and header building."""

from __future__ import annotations

import pytest

from gunspec._core._auth import build_auth_headers, resolve_api_key

# ---------------------------------------------------------------------------
# resolve_api_key
# ---------------------------------------------------------------------------


class TestResolveApiKey:
    """Tests for resolve_api_key()."""

    def test_explicit_key_returned(self) -> None:
        assert resolve_api_key(api_key="gs_test") == "gs_test"

    def test_env_var_used_when_no_explicit_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GUNSPEC_API_KEY", "gs_env")
        assert resolve_api_key() == "gs_env"

    def test_none_when_no_key_and_no_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GUNSPEC_API_KEY", raising=False)
        assert resolve_api_key() is None

    def test_empty_string_falls_through_to_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """An empty string is treated as 'not provided' so the env var wins."""
        monkeypatch.setenv("GUNSPEC_API_KEY", "gs_env_fallback")
        assert resolve_api_key(api_key="") == "gs_env_fallback"

    def test_empty_string_with_no_env_returns_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GUNSPEC_API_KEY", raising=False)
        assert resolve_api_key(api_key="") is None

    def test_explicit_key_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GUNSPEC_API_KEY", "gs_env_ignored")
        assert resolve_api_key(api_key="gs_explicit") == "gs_explicit"


# ---------------------------------------------------------------------------
# build_auth_headers
# ---------------------------------------------------------------------------


class TestBuildAuthHeaders:
    """Tests for build_auth_headers()."""

    def test_returns_header_when_key_provided(self) -> None:
        assert build_auth_headers("gs_test") == {"X-API-Key": "gs_test"}

    def test_returns_empty_dict_when_none(self) -> None:
        assert build_auth_headers(None) == {}

    def test_returns_empty_dict_when_empty_string(self) -> None:
        assert build_auth_headers("") == {}

    def test_returns_empty_dict_with_default_arg(self) -> None:
        """Calling with no argument at all should also return empty."""
        assert build_auth_headers() == {}
