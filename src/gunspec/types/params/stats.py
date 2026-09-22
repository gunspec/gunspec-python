"""Request parameter TypedDicts: stats."""

from __future__ import annotations

from typing import TypedDict

from .shared import PaginationParams

# Stats


class PopularCalibersParams(TypedDict, total=False):
    """Parameters for ``GET /v1/stats/popular-calibers``."""

    limit: int


class ProlificManufacturersParams(TypedDict, total=False):
    """Parameters for ``GET /v1/stats/prolific-manufacturers``."""

    limit: int
    category: str


class _ByEraRequired(TypedDict):
    decade: str


class ByEraParams(_ByEraRequired, total=False):
    """Parameters for ``GET /v1/stats/by-era``."""


class _AdoptionByCountryRequired(TypedDict):
    code: str


class AdoptionByCountryParams(_AdoptionByCountryRequired, total=False):
    """Parameters for ``GET /v1/stats/adoption/country``."""


class _AdoptionByTypeRequired(TypedDict):
    type: str


class AdoptionByTypeParams(_AdoptionByTypeRequired, total=False):
    """Parameters for ``GET /v1/stats/adoption/type``."""


class ActionTypesParams(TypedDict, total=False):
    """Parameters for ``GET /v1/stats/action-types``."""

    category: str


class FeatureFrequencyParams(TypedDict, total=False):
    """Parameters for ``GET /v1/stats/feature-frequency``."""

    category: str
    limit: int


class CaliberPopularityByEraParams(TypedDict, total=False):
    """Parameters for ``GET /v1/stats/caliber-popularity-by-era``."""

    from_decade: str
    to_decade: str


# Data Quality


class ConfidenceParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/data/confidence``."""

    below: float
