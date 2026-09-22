"""Request parameter TypedDicts: firearm."""

from __future__ import annotations

from typing import TypedDict

from .shared import PaginationParams

# Firearms


class ListFirearmsParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms``."""

    manufacturer: str
    caliber: str
    category: str
    action_type: str
    country_of_origin: str
    year_introduced_min: int
    year_introduced_max: int
    weight_min: float
    weight_max: float
    barrel_length_min: float
    status: str
    has_3d_model: str
    fields: str


class _SearchFirearmsRequired(TypedDict):
    q: str


class SearchFirearmsParams(_SearchFirearmsRequired, PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/search``."""


class _CompareFirearmsRequired(TypedDict):
    ids: str


class CompareFirearmsParams(_CompareFirearmsRequired, total=False):
    """Parameters for ``GET /v1/firearms/compare``."""


class GameMetaParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/:id/game/meta``."""

    archetype: str


class RandomFirearmParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/random``."""

    category: str
    country: str


class _TopFirearmsRequired(TypedDict):
    stat: str


class TopFirearmsParams(_TopFirearmsRequired, total=False):
    """Parameters for ``GET /v1/firearms/top``."""

    category: str
    limit: int


class _HeadToHeadRequired(TypedDict):
    a: str
    b: str


class HeadToHeadParams(_HeadToHeadRequired, total=False):
    """Parameters for ``GET /v1/firearms/head-to-head``."""


class _ByFeatureRequired(TypedDict):
    feature: str


class ByFeatureParams(_ByFeatureRequired, PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/by-feature``."""

    category: str


class _ByActionRequired(TypedDict):
    action: str


class ByActionParams(_ByActionRequired, PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/by-action``."""


class _ByMaterialRequired(TypedDict):
    material: str
    component: str


class ByMaterialParams(_ByMaterialRequired, PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/by-material``."""


class _ByDesignerRequired(TypedDict):
    designer: str


class ByDesignerParams(_ByDesignerRequired, PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/by-designer``."""


class PowerRatingParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/power-rating``."""

    category: str


class TimelineParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/timeline``."""

    page: int
    per_page: int
    sort: str
    order: str
    from_: int  # 'from' is a reserved word
    to: int
    category: str


class _ByConflictRequired(TypedDict):
    conflict: str


class ByConflictParams(_ByConflictRequired, PaginationParams, total=False):
    """Parameters for ``GET /v1/firearms/by-conflict``."""


class _CalculateBallisticsRequired(TypedDict):
    ammo_id: str


class CalculateBallisticsParams(_CalculateBallisticsRequired, total=False):
    """Parameters for ``GET /v1/firearms/:id/calculate``."""


class LoadFirearmParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/:id/load``."""

    ammo_id: str


class PopularFirearmsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/popular/firearms``."""

    days: int
    limit: int
