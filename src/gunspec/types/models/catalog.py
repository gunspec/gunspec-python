"""Pydantic response models: catalog."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional

from pydantic import BaseModel

from ..vocabulary import FirearmStatus
from .caliber_geometry import (
    BulletProfile,
    CaseMaterial,
    CaseShape,
    Closure,
    MarkingColor,
    ProjectileKind,
    SpecStandard,
)
from .provenance import Provenance
from .shared import _MODEL_CONFIG

if TYPE_CHECKING:
    # Resolved by ``CountryArsenalGroup.model_rebuild()`` in ``__init__``;
    # ``firearm`` imports ``Manufacturer`` and ``Category`` from here.
    from .firearm import Firearm

# Manufacturers


class Manufacturer(BaseModel):
    """A firearms manufacturer."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    country_code: Optional[str] = None
    founded_year: Optional[int] = None
    status: Optional[Literal["active", "defunct", "unknown"]] = None
    """Whether the company still trades. ``None`` means nobody has established it."""
    defunct_year: Optional[int] = None
    """Year it ceased trading, where established. ``None`` while it trades, and where the year is unknown."""
    state_owned: Optional[bool] = None
    """Government owned. ``None`` is not ``False``: it means nobody has established it."""
    makes_firearms: Optional[bool] = None
    """Builds what this catalog lists, as against importing, rebranding or customising it."""
    parent_id: Optional[str] = None
    """The manufacturer that owns this one today."""
    predecessor_id: Optional[str] = None
    """The manufacturer this one succeeded, which is not the same as being owned by it."""
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    created_at: str
    updated_at: str
    version: Optional[str] = None


class ManufacturerStatsManufacturer(BaseModel):
    """Nested manufacturer summary inside ManufacturerStats."""

    model_config = _MODEL_CONFIG

    id: str
    name: str


class ManufacturerStatsAggregates(BaseModel):
    """Aggregate statistics for a manufacturer."""

    model_config = _MODEL_CONFIG

    total_firearms: int
    avg_weight_g: Optional[float] = None
    avg_range_m: Optional[float] = None
    avg_capacity: Optional[float] = None
    active_count: int
    discontinued_count: int
    earliest_year: Optional[int] = None
    latest_year: Optional[int] = None


class ManufacturerStatsCategory(BaseModel):
    """Category breakdown inside ManufacturerStats."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    count: int


class ManufacturerStats(BaseModel):
    """Per-manufacturer aggregate statistics."""

    model_config = _MODEL_CONFIG

    manufacturer: ManufacturerStatsManufacturer
    stats: Optional[ManufacturerStatsAggregates] = None
    categories: list[ManufacturerStatsCategory] = []
    most_common_caliber: Optional[ManufacturerStatsCategory] = None


class ManufacturerTimelineFirearm(BaseModel):
    """A firearm entry in a manufacturer timeline year group."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    year_introduced: Optional[int] = None
    category_id: str
    status: Optional[FirearmStatus] = None


class ManufacturerTimelineYear(BaseModel):
    """A year group in a manufacturer timeline."""

    model_config = _MODEL_CONFIG

    year: Optional[int] = None
    firearms: list[ManufacturerTimelineFirearm] = []


class ManufacturerTimeline(BaseModel):
    """Manufacturer timeline grouping firearms by year introduced."""

    model_config = _MODEL_CONFIG

    manufacturer: ManufacturerStatsManufacturer
    timeline: list[ManufacturerTimelineYear] = []


# Calibers


class Caliber(BaseModel):
    """A cartridge / caliber specification."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    aliases: Optional[List[str]] = None
    nato_designation: Optional[str] = None
    bullet_diameter_mm: Optional[float] = None
    neck_diameter_mm: Optional[float] = None
    shoulder_diameter_mm: Optional[float] = None
    base_diameter_mm: Optional[float] = None
    rim_diameter_mm: Optional[float] = None
    rim_thickness_mm: Optional[float] = None
    case_length_mm: Optional[float] = None
    overall_length_mm: Optional[float] = None
    bullet_length_mm: Optional[float] = None
    max_pressure_mpa: Optional[float] = None
    max_pressure_psi: Optional[float] = None
    typical_bullet_weight_g: Optional[float] = None
    typical_muzzle_velocity_mps: Optional[float] = None
    typical_muzzle_energy_j: Optional[float] = None
    primer_type: Optional[str] = None
    cartridge_type: Optional[str] = None
    case_shape: Optional[CaseShape] = None
    case_material: Optional[CaseMaterial] = None
    projectile_kind: Optional[ProjectileKind] = None
    bullet_profile: Optional[BulletProfile] = None
    closure: Optional[Closure] = None
    marking_color: Optional[MarkingColor] = None
    marking_meaning: Optional[str] = None
    parent_cartridge_id: Optional[str] = None
    year_introduced: Optional[int] = None
    designer: Optional[str] = None
    spec_source: Optional[str] = None
    spec_standard: Optional[SpecStandard] = None
    data_confidence: Optional[float] = None
    verified_at: Optional[str] = None
    verified_fields: Optional[List[str]] = None
    created_at: str
    updated_at: str
    version: Optional[str] = None
    provenance: Optional[Provenance] = None


class CaliberBallisticsCaliber(BaseModel):
    """Nested caliber summary inside CaliberBallistics."""

    model_config = _MODEL_CONFIG

    id: str
    name: str


class CaliberBallistics(BaseModel):
    """Simplified ballistics result for a caliber at a given distance."""

    model_config = _MODEL_CONFIG

    caliber: CaliberBallisticsCaliber
    distance_m: float
    muzzle_velocity_mps: float
    muzzle_energy_j: float
    velocity_at_distance_mps: float
    energy_at_distance_j: float
    time_of_flight_s: float
    bullet_drop_cm: float


class CaliberFamily(BaseModel):
    """Caliber family tree (ancestors + current + descendants)."""

    model_config = _MODEL_CONFIG

    ancestors: list[Caliber] = []
    current: Caliber
    descendants: list[Caliber] = []


# Categories


class Category(BaseModel):
    """A firearm category."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    description: Optional[str] = None


# Feature icons


class FeatureIcon(BaseModel):
    """A drawn feature icon, from ``GET /v1/features/icons``."""

    model_config = _MODEL_CONFIG

    name: str
    label: str
    icon_url: str


# Countries


class Country(BaseModel):
    """A country with its firearm count."""

    model_config = _MODEL_CONFIG

    code: str
    firearm_count: int


class CountryArsenalGroup(BaseModel):
    """A usage-type group in a country's arsenal."""

    model_config = _MODEL_CONFIG

    type: str
    firearms: list[Firearm] = []


class CountryArsenal(BaseModel):
    """A country's firearm arsenal -- military and law enforcement holdings."""

    model_config = _MODEL_CONFIG

    country: Country
    total_firearms: int
    groups: list[CountryArsenalGroup] = []


# Conflicts


class ConflictFirearm(BaseModel):
    """A firearm entry within a conflict."""

    model_config = _MODEL_CONFIG

    id: str
    name: str


class Conflict(BaseModel):
    """A conflict with associated firearms."""

    model_config = _MODEL_CONFIG

    name: str
    firearm_count: int
    firearms: list[ConflictFirearm] = []
