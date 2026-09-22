"""Tests for gunspec._core._etag_cache."""

from __future__ import annotations

import pytest

from gunspec._core._etag_cache import (
    CachedEntry,
    MemoryETagStore,
    cache_key_for,
    credential_fingerprint,
)


def _entry(etag: str) -> CachedEntry:
    return CachedEntry(etag=etag, body=f'{{"data":"{etag}"}}', stored_at=0.0)


class TestMemoryETagStore:
    def test_get_returns_what_was_set(self) -> None:
        store = MemoryETagStore()
        store.set("a", _entry('"1"'))
        assert store.get("a") is not None and store.get("a").etag == '"1"'
        assert store.get("b") is None

    def test_evicts_least_recently_used(self) -> None:
        store = MemoryETagStore(2)
        store.set("a", _entry('"a"'))
        store.set("b", _entry('"b"'))
        store.get("a")
        store.set("c", _entry('"c"'))
        assert store.get("b") is None
        assert store.get("a") is not None
        assert store.get("c") is not None
        assert len(store) == 2

    def test_replaces_without_growing(self) -> None:
        store = MemoryETagStore(1)
        store.set("a", _entry('"1"'))
        store.set("a", _entry('"2"'))
        assert len(store) == 1
        assert store.get("a").etag == '"2"'

    def test_refuses_non_positive_bound(self) -> None:
        with pytest.raises(ValueError):
            MemoryETagStore(0)

    def test_clear(self) -> None:
        store = MemoryETagStore()
        store.set("a", _entry('"1"'))
        store.clear()
        assert len(store) == 0


class TestCredentialFingerprint:
    def test_stable_and_distinct(self) -> None:
        assert credential_fingerprint("gsk_abc") == credential_fingerprint("gsk_abc")
        assert credential_fingerprint("gsk_abc") != credential_fingerprint("gsk_abd")

    def test_never_contains_the_key(self) -> None:
        key = "gsk_72ee457ac9ccc5b2b5bc788f5269feca"
        fp = credential_fingerprint(key)
        assert "gsk_" not in fp
        assert len(fp) == 8 and int(fp, 16) >= 0

    def test_anon_without_key(self) -> None:
        assert credential_fingerprint(None) == "anon"
        assert credential_fingerprint("") == "anon"

    def test_matches_typescript_fnv1a(self) -> None:
        # Same algorithm as packages/sdk/src/core/etag-cache.ts so a shared
        # persistent store keys identically from both SDKs.
        assert credential_fingerprint("gsk_test") == "32736be1"


class TestCacheKeyFor:
    def test_namespaces_by_fingerprint(self) -> None:
        assert cache_key_for("abc", "https://api/x") == "abc https://api/x"
        assert cache_key_for("abc", "https://api/x") != cache_key_for("def", "https://api/x")
