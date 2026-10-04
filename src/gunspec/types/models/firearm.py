"""Pydantic response models: firearm."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..media import InlineMediaItem
from ..vocabulary import FirearmStatus, ImageType, MediaKind, SchematicType
from .caliber_geometry import (
    BulletProfile,
    CaseMaterial,
    CaseShape,
    Closure,
    MarkingColor,
    ProjectileKind,
)
from .catalog import Category, Manufacturer
from .provenance import Provenance
from .shared import _MODEL_CONFIG

# Firearms


class Firearm(BaseModel):
    """A firearm specification record."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    manufacturer_id: str
    category_id: str
    parent_firearm_id: Optional[str] = None
    variant_type: Optional[str] = None
    year_introduced: Optional[int] = None
    year_discontinued: Optional[int] = None
    status: Optional[FirearmStatus] = None
    country_of_origin: Optional[str] = None

    # Physical dimensions
    weight_empty_g: Optional[float] = None
    weight_loaded_g: Optional[float] = None
    overall_length_mm: Optional[float] = None
    barrel_length_mm: Optional[float] = None
    height_mm: Optional[float] = None
    width_mm: Optional[float] = None
    sight_radius_mm: Optional[float] = None
    folded_length_mm: Optional[float] = None

    # Mechanical
    action_type: Optional[str] = None
    firing_mechanism: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_pull_n: Optional[float] = None
    magazine_capacity: Optional[int] = None
    magazine_type: Optional[str] = None

    # Ballistic
    muzzle_velocity_mps: Optional[float] = None
    muzzle_energy_j: Optional[float] = None
    effective_range_m: Optional[float] = None
    max_range_m: Optional[float] = None
    rate_of_fire_rpm: Optional[int] = None

    # Barrel details
    barrel_rifling: Optional[str] = None
    rifling_twist_mm: Optional[float] = None
    number_of_grooves: Optional[int] = None

    # Materials
    frame_material: Optional[str] = None
    slide_material: Optional[str] = None
    barrel_material: Optional[str] = None
    stock_material: Optional[str] = None
    finish: Optional[str] = None

    # Stored as JSON text in D1, served as the value it represents. These were
    # handed out as strings for the caller to parse; a cell that does not parse
    # is now None rather than the raw text.
    safety_mechanisms: Optional[List[str]] = None
    features: Optional[List[str]] = None
    feed_systems: Optional[List[str]] = None
    alternate_names: Optional[List[str]] = None
    firing_modes: Optional[List[str]] = None
    conflicts: Optional[List[Dict[str, Any]]] = None
    production_numbers: Optional[Dict[str, Any]] = None
    sources: Optional[List[str]] = None

    # Game stats (0-100)
    game_damage: Optional[float] = None
    game_accuracy: Optional[float] = None
    game_range: Optional[float] = None
    game_fire_rate: Optional[float] = None
    game_mobility: Optional[float] = None
    game_recoil_control: Optional[float] = None
    game_reload_speed: Optional[float] = None
    game_concealment: Optional[float] = None

    # Content
    description: Optional[str] = None
    notes: Optional[str] = None
    designer: Optional[str] = None
    lore: Optional[str] = None

    # Ballistic source
    source_muzzle_velocity_mps: Optional[float] = None
    source_muzzle_energy_j: Optional[float] = None
    source_effective_range_m: Optional[float] = None
    source_max_range_m: Optional[float] = None
    ballistics_source: Optional[str] = None
    ballistics_source_url: Optional[str] = None
    default_ammo_id: Optional[str] = None

    # Media
    has_3d_model: int = Field(default=0, alias="has3dModel")
    svg_line_art_url: Optional[str] = None
    model_3d_url: Optional[str] = Field(default=None, alias="model3dUrl")

    # Data quality
    data_confidence: Optional[float] = None
    #: When a source was last read against the record's figures; None until one has been.
    verified_at: Optional[str] = None
    #: The figures a source confirmed, read off the maker's own page and accepted by a person.
    verified_fields: Optional[List[str]] = None

    # Timestamps and cache signals
    created_at: str
    updated_at: str
    version: Optional[str] = None

    # Sources, confidence and verification state (detail endpoint)
    provenance: Optional[Provenance] = None


class FirearmListItem(BaseModel):
    """Summarised firearm returned by list / search endpoints."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    manufacturer_id: str
    category_id: str
    year_introduced: Optional[int] = None
    status: Optional[FirearmStatus] = None
    country_of_origin: Optional[str] = None
    action_type: Optional[str] = None
    weight_empty_g: Optional[float] = None
    barrel_length_mm: Optional[float] = None
    images: List[InlineMediaItem] = []
    svg_line_art_url: Optional[str] = None
    model_3d_url: Optional[str] = Field(default=None, alias="model3dUrl")
    created_at: Optional[str] = None
    favorite_count: Optional[int] = None
    updated_at: Optional[str] = None
    version: Optional[str] = None


class FirearmCaliberEntry(BaseModel):
    """A caliber entry on a firearm detail, joined from the junction table."""

    model_config = _MODEL_CONFIG

    caliber_id: str
    is_primary: int
    name: str
    nato_designation: Optional[str] = None
    bullet_diameter_mm: Optional[float] = None
    case_length_mm: Optional[float] = None
    cartridge_type: Optional[str] = None
    neck_diameter_mm: Optional[float] = None
    shoulder_diameter_mm: Optional[float] = None
    base_diameter_mm: Optional[float] = None
    rim_diameter_mm: Optional[float] = None
    rim_thickness_mm: Optional[float] = None
    overall_length_mm: Optional[float] = None
    bullet_length_mm: Optional[float] = None
    typical_bullet_weight_g: Optional[float] = None
    primer_type: Optional[str] = None
    case_shape: Optional[CaseShape] = None
    case_material: Optional[CaseMaterial] = None
    projectile_kind: Optional[ProjectileKind] = None
    bullet_profile: Optional[BulletProfile] = None
    closure: Optional[Closure] = None
    marking_color: Optional[MarkingColor] = None


class FirearmDetail(Firearm):
    """Full firearm detail including related entities."""

    manufacturer: Optional[Manufacturer] = None
    category: Optional[Category] = None
    calibers: list[FirearmCaliberEntry] = []
    images: list[FirearmImage] = []
    users: list[FirearmUser] = []
    schematics: Optional[list[FirearmSchematic]] = None


class FirearmVariant(BaseModel):
    """A firearm variant summary."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    variant_type: Optional[str] = None
    year_introduced: Optional[int] = None
    status: Optional[FirearmStatus] = None


# Firearm Images


class FirearmImage(BaseModel):
    """An image associated with a firearm."""

    model_config = _MODEL_CONFIG

    id: int
    firearm_id: str
    url: str
    type: Optional[ImageType] = None
    source: Optional[str] = None
    license: Optional[str] = None
    kind: Optional[MediaKind] = None
    storage: Optional[str] = None
    author: Optional[str] = None
    source_url: Optional[str] = None
    alt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int = 0


class FirearmSchematic(BaseModel):
    """A technical drawing or document for a firearm."""

    model_config = _MODEL_CONFIG

    id: int
    firearm_id: str
    title: str
    type: SchematicType
    url: str
    format: Optional[str] = None
    version: Optional[str] = None
    manufacturer: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = None
    created_at: Optional[str] = None


# Firearm Users (adopters)


class FirearmUser(BaseModel):
    """A military, law-enforcement, or other institutional user of a firearm."""

    model_config = _MODEL_CONFIG

    id: int
    firearm_id: str
    user_name: str
    user_type: Optional[str] = None
    country_code: Optional[str] = None
    adopted_year: Optional[int] = None
    designation: Optional[str] = None
