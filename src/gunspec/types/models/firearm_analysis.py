"""Pydantic response models: firearm analysis."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel

from .catalog import Caliber
from .firearm import Firearm, FirearmDetail
from .shared import _MODEL_CONFIG

# Firearm Comparisons


class FirearmComparison(BaseModel):
    """Comparison result for multiple firearms."""

    model_config = _MODEL_CONFIG

    items: list[FirearmDetail] = []
    deltas: dict[str, Any] = {}


class CaliberComparison(BaseModel):
    """Comparison result for multiple calibers."""

    model_config = _MODEL_CONFIG

    items: list[Caliber] = []
    deltas: dict[str, Any] = {}


# Head-to-Head


class HeadToHeadVerdict(BaseModel):
    """Per-field verdict in a head-to-head comparison."""

    model_config = _MODEL_CONFIG

    winner: str
    a: Optional[float] = None
    b: Optional[float] = None
    better: str


class HeadToHead(BaseModel):
    """Head-to-head comparison of two firearms on numeric specs."""

    model_config = _MODEL_CONFIG

    a: dict[str, Any] = {}
    b: dict[str, Any] = {}
    verdicts: dict[str, HeadToHeadVerdict] = {}


# Family Tree


class FamilyTree(BaseModel):
    """Firearm family tree (ancestors + current + descendants)."""

    model_config = _MODEL_CONFIG

    ancestors: list[dict[str, Any]] = []
    current: Firearm
    descendants: list[dict[str, Any]] = []


# Similar Firearms


class SimilarFirearm(BaseModel):
    """A similar firearm with a computed similarity score."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    score: float


# Adoption Map


class AdoptionMapUser(BaseModel):
    """A user entry in an adoption map country."""

    model_config = _MODEL_CONFIG

    name: str
    type: Optional[str] = None
    year: Optional[int] = None
    designation: Optional[str] = None


class AdoptionMapCountry(BaseModel):
    """A country group in an adoption map."""

    model_config = _MODEL_CONFIG

    code: Optional[str] = None
    users: list[AdoptionMapUser] = []


class AdoptionMap(BaseModel):
    """Adoption map for a firearm, grouped by country."""

    model_config = _MODEL_CONFIG

    firearm_id: str
    firearm_name: str
    countries: list[AdoptionMapCountry] = []


# Top Firearms


class TopFirearmItem(BaseModel):
    """A firearm in a 'top N' ranking."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    manufacturer_id: str
    category_id: str
    value: float
    unit: str


# Power Rating


class PowerRatingBreakdown(BaseModel):
    """Per-component breakdown of a power rating."""

    model_config = _MODEL_CONFIG

    energy: float
    range: float
    fire_rate: float
    capacity: float
    mobility: float


class PowerRating(BaseModel):
    """A firearm's computed power rating with breakdown."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    manufacturer_id: str
    category_id: str
    power_rating: float
    breakdown: PowerRatingBreakdown


# Timeline


class TimelineItem(BaseModel):
    """A firearm in a chronological timeline listing."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    manufacturer_id: str
    category_id: str
    year_introduced: Optional[int] = None
    year_discontinued: Optional[int] = None
    status: Optional[str] = None
    country_of_origin: Optional[str] = None


# Dimensions


class DimensionsMetric(BaseModel):
    """Metric measurements for a firearm."""

    model_config = _MODEL_CONFIG

    weight_empty_g: Optional[float] = None
    weight_loaded_g: Optional[float] = None
    overall_length_mm: Optional[float] = None
    barrel_length_mm: Optional[float] = None
    height_mm: Optional[float] = None
    width_mm: Optional[float] = None
    folded_length_mm: Optional[float] = None


class DimensionsImperial(BaseModel):
    """Imperial measurements for a firearm (converted from metric)."""

    model_config = _MODEL_CONFIG

    weight_empty_lbs: Optional[float] = None
    weight_loaded_lbs: Optional[float] = None
    overall_length_in: Optional[float] = None
    barrel_length_in: Optional[float] = None
    height_in: Optional[float] = None
    width_in: Optional[float] = None
    folded_length_in: Optional[float] = None


class Dimensions(BaseModel):
    """Firearm dimensions in both metric and imperial units."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    metric: DimensionsMetric
    imperial: DimensionsImperial


# Filter Options


class FilterOptionCategory(BaseModel):
    """A category option in filter dropdowns."""

    model_config = _MODEL_CONFIG

    slug: str
    name: str


class FilterOptionItem(BaseModel):
    """A generic filter option (manufacturer, caliber, action type)."""

    model_config = _MODEL_CONFIG

    id: str
    name: str


class FilterOptions(BaseModel):
    """Available filter dropdown options."""

    model_config = _MODEL_CONFIG

    categories: list[FilterOptionCategory] = []
    manufacturers: list[FilterOptionItem] = []
    calibers: list[FilterOptionItem] = []
    action_types: list[FilterOptionItem] = []


# Silhouette


class Silhouette(BaseModel):
    """SVG silhouette data for a firearm."""

    model_config = _MODEL_CONFIG

    slug: str
    svg: Optional[str] = None
    data_uri: Optional[str] = None
    stroke_width: Optional[float] = None
    stroke_color: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
