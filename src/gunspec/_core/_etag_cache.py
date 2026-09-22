"""Conditional-request cache for the GunSpec SDK.

The API answers ``304 Not Modified`` on its cacheable GETs when the client
sends the ``ETag`` it holds, and a 304 does not count against the plan's daily
cap. This module remembers the last body and tag per URL so the HTTP client
can send ``If-None-Match`` and serve the held copy on a 304.

The API shapes a body per plan, so a tag is only valid for the key that fetched
it. Every cache key therefore carries a fingerprint of the API key, and a store
shared between two differently keyed clients cannot cross-serve a paid-tier
body to a cheaper key.
"""

from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class CachedEntry:
    """One held response."""

    etag: str
    body: str
    stored_at: float


class ETagStore(Protocol):
    """Where held responses live. Implement to persist across processes."""

    def get(self, key: str) -> Optional[CachedEntry]: ...

    def set(self, key: str, entry: CachedEntry) -> None: ...


class MemoryETagStore:
    """Bounded in-memory store with least-recently-used eviction."""

    def __init__(self, max_entries: int = 500) -> None:
        if not isinstance(max_entries, int) or max_entries < 1:
            raise ValueError("max_entries must be a positive integer")
        self._max = max_entries
        self._entries: OrderedDict[str, CachedEntry] = OrderedDict()

    def get(self, key: str) -> Optional[CachedEntry]:
        entry = self._entries.get(key)
        if entry is None:
            return None
        self._entries.move_to_end(key)
        return entry

    def set(self, key: str, entry: CachedEntry) -> None:
        self._entries[key] = entry
        self._entries.move_to_end(key)
        while len(self._entries) > self._max:
            self._entries.popitem(last=False)

    def __len__(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()


def credential_fingerprint(api_key: Optional[str]) -> str:
    """Non-reversible fingerprint of a credential for namespacing cache keys.

    FNV-1a over the key. Not a secret-grade hash and not meant to be: it only
    has to keep two keys' entries apart inside one process.
    """
    if not api_key:
        return "anon"
    h = 0x811C9DC5
    for ch in api_key:
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def cache_key_for(fingerprint: str, url: str) -> str:
    """Build the store key for one GET."""
    return f"{fingerprint} {url}"


def now() -> float:
    return time.time()
