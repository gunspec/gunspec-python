"""Request parameter TypedDicts: shared."""

from __future__ import annotations

from typing import TypedDict

# Pagination (shared base)


class PaginationParams(TypedDict, total=False):
    """Common pagination parameters accepted by all list endpoints."""

    page: int
    per_page: int
    sort: str
    order: str  # "asc" | "desc"
