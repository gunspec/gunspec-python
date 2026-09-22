"""Pydantic response models: stats."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .shared import _MODEL_CONFIG

# Statistics


class StatsSummary(BaseModel):
    """Database summary statistics."""

    model_config = _MODEL_CONFIG

    total_firearms: int
    total_manufacturers: int
    total_calibers: int
    countries_of_origin: int
    avg_confidence: Optional[float] = None
    total_variants: int


class ProductionStatusItem(BaseModel):
    """Production status breakdown."""

    model_config = _MODEL_CONFIG

    status: str
    count: int


class FieldCoverage(BaseModel):
    """Field coverage percentage for a single field."""

    model_config = _MODEL_CONFIG

    field: str
    percentage: float


class PopularCaliber(BaseModel):
    """Popular caliber with firearm count."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    nato_designation: Optional[str] = None
    firearm_count: int


class ProlificManufacturer(BaseModel):
    """Prolific manufacturer with firearm count."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    country_code: Optional[str] = None
    firearm_count: int


class CategoryStats(BaseModel):
    """Category statistics with averages."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    firearm_count: int
    avg_weight_g: Optional[float] = None
    avg_magazine_capacity: Optional[float] = None
    avg_barrel_length_mm: Optional[float] = None


class EraStats(BaseModel):
    """Era (decade) statistics."""

    model_config = _MODEL_CONFIG

    firearm_count: int
    avg_weight_g: Optional[float] = None
    avg_magazine_capacity: Optional[float] = None
    avg_barrel_length_mm: Optional[float] = None
    earliest_year: Optional[int] = None
    latest_year: Optional[int] = None


class MaterialStatsEntry(BaseModel):
    """A material with its usage count."""

    model_config = _MODEL_CONFIG

    material: str
    count: int


class MaterialStats(BaseModel):
    """Material usage breakdown per component."""

    model_config = _MODEL_CONFIG

    frame: list[MaterialStatsEntry] = []
    slide: list[MaterialStatsEntry] = []
    barrel: list[MaterialStatsEntry] = []
    stock: list[MaterialStatsEntry] = []


class AdoptionByCountryItem(BaseModel):
    """Adoption record by country."""

    model_config = _MODEL_CONFIG

    id: int
    user_name: str
    user_type: Optional[str] = None
    adopted_year: Optional[int] = None
    designation: Optional[str] = None
    firearm_id: str
    firearm_name: str


class AdoptionByTypeItem(BaseModel):
    """Adoption record by user type."""

    model_config = _MODEL_CONFIG

    firearm_id: str
    firearm_name: str
    adoption_count: int
    countries: list[str] = []


class ActionTypeStats(BaseModel):
    """Action type frequency."""

    model_config = _MODEL_CONFIG

    action_type: str
    count: int


class FeatureFrequency(BaseModel):
    """Feature frequency item."""

    model_config = _MODEL_CONFIG

    feature: str
    count: int


class CaliberPopularityByEraCaliberEntry(BaseModel):
    """A caliber entry within a decade's popularity ranking."""

    model_config = _MODEL_CONFIG

    caliber_id: str
    caliber_name: str
    firearm_count: int


class CaliberPopularityByEra(BaseModel):
    """Caliber popularity within a decade."""

    model_config = _MODEL_CONFIG

    decade: str
    calibers: list[CaliberPopularityByEraCaliberEntry] = []


# Data Quality


class DataCoverage(BaseModel):
    """Data coverage summary."""

    model_config = _MODEL_CONFIG

    field: str
    percentage: float


class ConfidenceEntry(BaseModel):
    """A firearm record with its computed data confidence score."""

    model_config = _MODEL_CONFIG

    slug: str
    name: str
    confidence_score: float
    filled_fields: int
    total_fields: int
