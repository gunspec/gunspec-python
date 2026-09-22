"""Request parameter TypedDicts: content."""

from __future__ import annotations

from typing import Literal, TypedDict


class ListChangelogParams(TypedDict, total=False):
    """Parameters for ``GET /v1/changelog``."""

    page: int
    per_page: int
    category: Literal["feature", "fix", "improvement", "data", "breaking"]


class ListBlogPostsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/blog``."""

    page: int
    per_page: int
    category: str
