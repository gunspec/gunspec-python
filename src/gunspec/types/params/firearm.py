"""Request parameter TypedDicts: firearm."""

from __future__ import annotations

from typing import Literal, TypedDict

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


class _LoadCarriageRequired(TypedDict):
    #: Comma-separated firearm slugs, maximum 5.
    ids: str


class LoadCarriageParams(_LoadCarriageRequired, total=False):
    """Parameters for ``GET /v1/firearms/load-carriage``.

    Every field but ``ids`` has a default; the answer's ``march.defaulted``
    names the ones it assumed.
    """

    body_mass_kg: float
    body_fat_pct: float
    #: Everything else carried, in kg: armour, pack, water.
    kit_kg: float
    #: Full magazines in total, the one in the firearm included. 0 carries it unloaded.
    magazines: int
    #: Comma-separated attachment slugs, maximum 10.
    attachments: str
    speed_kmh: float
    #: Rise over run as a percentage; negative is downhill.
    grade_pct: float
    terrain: Literal["paved", "dirt_road", "light_brush", "heavy_brush", "swampy_bog", "loose_sand"]
    distance_km: float
    #: ``lcda`` (default) or ``pandolf``, which refuses a downhill grade.
    model: Literal["lcda", "pandolf"]


class _RecoilRequired(TypedDict):
    #: Comma-separated firearm slugs, maximum 5.
    ids: str


class RecoilParams(_RecoilRequired, total=False):
    """Parameters for ``GET /v1/firearms/recoil``.

    Without ``powder_charge_g`` only the bullet is counted and every figure is
    a lower bound.
    """

    #: The load every firearm fires; default, the load each one's ballistic profile uses.
    ammo_id: str
    #: Which recorded weight recoils; default ``loaded``.
    mass: Literal["loaded", "empty"]
    #: The load's powder charge in grams. Needs ``ammo_id``.
    powder_charge_g: float
    #: The SAAMI class whose gas velocity factor applies; default, read from the category.
    gas_class: Literal["rifle", "shotgun", "shotgun_long_barrel", "handgun"]


class _PointBlankRequired(TypedDict):
    #: Comma-separated firearm slugs, maximum 5.
    ids: str


class PointBlankParams(_PointBlankRequired, total=False):
    """Parameters for ``GET /v1/firearms/point-blank``."""

    ammo_id: str
    #: Target diameter in mm; default 200.
    target_mm: float
    #: Sight height above the bore in mm; default, the height assumed for the category.
    sight_height_mm: float


class _AmmoLoadRequired(TypedDict):
    #: Comma-separated firearm slugs, maximum 5.
    ids: str


class AmmoLoadParams(_AmmoLoadRequired, total=False):
    """Parameters for ``GET /v1/firearms/ammo-load``."""

    #: A load whose bullet the estimate uses; default, each cartridge's typical bullet.
    ammo_id: str
    #: A weight of full magazines to fill, in kg; default 5.
    budget_kg: float
    #: Full magazines in the estimated basic load; default 7.
    magazines: int
    #: Rounds in the estimated basic load; default ``magazines`` times the capacity.
    rounds: int


class PopularFirearmsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/popular/firearms``."""

    days: int
    limit: int
