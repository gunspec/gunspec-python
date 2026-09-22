"""Pydantic response models: shared."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

# Shared config

_MODEL_CONFIG = ConfigDict(
    frozen=True,
    populate_by_name=True,
    alias_generator=to_camel,
)


# Generic Response Wrappers


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    model_config = _MODEL_CONFIG

    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponseModel(BaseModel):
    """Standard paginated API response wrapper."""

    model_config = _MODEL_CONFIG

    success: bool
    data: list[Any] = []
    pagination: PaginationMeta


class SuccessResponseModel(BaseModel):
    """Standard single-item API response wrapper."""

    model_config = _MODEL_CONFIG

    success: bool
    data: Any = None
