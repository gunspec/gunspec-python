"""Tests for gunspec._core._etag_cache."""

from __future__ import annotations

import hashlib
import threading
from typing import List

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
        assert len(fp) == 32 and int(fp, 16) >= 0

    def test_anon_without_key(self) -> None:
        assert credential_fingerprint(None) == "anon"
        assert credential_fingerprint("") == "anon"

    def test_is_sha256_truncated_to_128_bits(self) -> None:
        # A 32-bit FNV-1a fingerprint let two keys collide in a shared store.
        expected = hashlib.sha256(b"gsk_test").hexdigest()[:32]
        assert credential_fingerprint("gsk_test") == expected


class TestCacheKeyFor:
    def test_namespaces_by_fingerprint(self) -> None:
        assert cache_key_for("abc", "https://api/x") == "abc https://api/x"
        assert cache_key_for("abc", "https://api/x") != cache_key_for("def", "https://api/x")


class TestFingerprintSeparatesKeys:
    def test_many_keys_never_share_a_fingerprint(self) -> None:
        keys = [f"gsk_{i:06d}" for i in range(20_000)]
        assert len({credential_fingerprint(k) for k in keys}) == len(keys)

    def test_different_keys_never_share_an_entry(self) -> None:
        store = MemoryETagStore()
        url = "https://api.gunspec.io/v1/firearms/ak-47"
        store.set(cache_key_for(credential_fingerprint("gsk_paid"), url), _entry("paid"))
        assert store.get(cache_key_for(credential_fingerprint("gsk_free"), url)) is None
        assert store.get(cache_key_for(credential_fingerprint(None), url)) is None


class TestThreadSafety:
    def test_concurrent_get_and_evict_never_raise(self) -> None:
        # A tiny store and many threads keep eviction racing every get; before
        # the lock a get could lose its entry between lookup and reorder.
        store = MemoryETagStore(max_entries=4)
        errors: List[BaseException] = []
        start = threading.Barrier(8)

        def worker(seed: int) -> None:
            try:
                start.wait()
                for i in range(5_000):
                    key = f"k{(seed + i) % 16}"
                    store.set(key, _entry(key))
                    store.get(f"k{(seed * 3 + i) % 16}")
            except BaseException as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(n,)) for n in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert len(store) <= 4

    def test_get_holds_the_lock_across_lookup_and_reorder(self) -> None:
        # Deterministic form of the race: while a get runs, an eviction from
        # another thread must wait, so the reorder always finds its key.
        store = MemoryETagStore(max_entries=1)
        store.set("a", _entry("a"))
        entries = store._entries
        evicted = threading.Event()

        raced = threading.Event()

        class Racing(type(entries)):  # type: ignore[misc]
            def move_to_end(self, key: str, last: bool = True) -> None:
                if not raced.is_set():
                    raced.set()
                    t = threading.Thread(target=lambda: (store.set("b", _entry("b")), evicted.set()))
                    t.start()
                    # The evicting thread is blocked on the lock, so this stays unset.
                    assert not evicted.wait(0.05)
                super().move_to_end(key, last)

        store._entries = Racing(entries)
        assert store.get("a") == _entry("a")
        assert evicted.wait(1.0)
        store._entries = type(entries)(store._entries)
        assert store.get("b") == _entry("b")
