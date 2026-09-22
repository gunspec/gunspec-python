"""Pydantic response models: ammunition."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .provenance import Provenance
from .shared import _MODEL_CONFIG

# Ammunition


class Ammunition(BaseModel):
    """A specific ammunition load for a caliber."""

    model_config = _MODEL_CONFIG

    id: str
    caliber_id: str
    name: str
    designation: Optional[str] = None
    manufacturer: Optional[str] = None
    country_of_origin: Optional[str] = None
    bullet_weight_g: float
    bullet_type: str
    ballistic_coefficient_g1: Optional[float] = Field(default=None, alias="ballisticCoefficientG1")
    ballistic_coefficient_g7: Optional[float] = Field(default=None, alias="ballisticCoefficientG7")
    reference_velocity_mps: float
    reference_barrel_length_mm: float
    velocity_retention_exponent: Optional[float] = None
    sectional_density: Optional[float] = None
    description: Optional[str] = None
    year_introduced: Optional[int] = None
    is_common: int
    is_military: int
    bullet_svg_url: Optional[str] = None
    created_at: str
    updated_at: str
    sources: Optional[List[str]] = None
    """Where the figures came from. Null on every load today: nothing is cited yet."""
    data_confidence: Optional[float] = None
    """How well specified the load is, 0 to 1. Null until there are sources behind it."""
    provenance: Optional[Provenance] = None
    """Sources, confidence and verification state."""
    version: Optional[str] = None
    """Opaque fingerprint of the record; equal values mean equal data."""


class TrajectoryPoint(BaseModel):
    """A single point along a ballistic trajectory."""

    model_config = _MODEL_CONFIG

    distance_m: float
    velocity_mps: float
    energy_j: float
    drop_cm: float
    time_of_flight_s: float
    mach_number: float
    momentum_kg_ms: float
    tko_factor: float
    energy_density_j_cm2: float = Field(alias="energyDensityJCm2")


class TerminalBallistics(BaseModel):
    """Muzzle-level terminal ballistics summary."""

    model_config = _MODEL_CONFIG

    tko_factor: float
    momentum_kg_ms: float
    sectional_density: float
    hatcher_rsp: float = Field(alias="hatcherRSP")
    energy_density_j_cm2: float = Field(alias="energyDensityJCm2")


class BallisticProfileAmmo(BaseModel):
    """Nested ammunition summary inside BallisticProfile."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    caliber_id: str


class BallisticProfile(BaseModel):
    """Full ballistic profile for an ammunition load."""

    model_config = _MODEL_CONFIG

    ammunition: BallisticProfileAmmo
    barrel_length_mm: float
    muzzle_velocity_mps: float
    muzzle_energy_j: float
    effective_range_m: float
    terminal_ballistics: TerminalBallistics
    trajectory: list[TrajectoryPoint] = []


class FirearmCalculationFirearm(BaseModel):
    """Nested firearm summary inside FirearmCalculation."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    barrel_length_mm: Optional[float] = None


class FirearmCalculationAmmo(BaseModel):
    """Nested ammunition summary inside FirearmCalculation."""

    model_config = _MODEL_CONFIG

    id: str
    name: str


class FirearmCalculationCalculated(BaseModel):
    """Calculated ballistic values inside FirearmCalculation."""

    model_config = _MODEL_CONFIG

    muzzle_velocity_mps: float
    muzzle_energy_j: float
    terminal_ballistics: TerminalBallistics


class FirearmCalculationSourceReported(BaseModel):
    """Source-reported ballistic values inside FirearmCalculation."""

    model_config = _MODEL_CONFIG

    muzzle_velocity_mps: Optional[float] = None
    muzzle_energy_j: Optional[float] = None


class FirearmCalculationDelta(BaseModel):
    """Delta between calculated and source-reported values."""

    model_config = _MODEL_CONFIG

    velocity_mps: Optional[float] = None
    energy_j: Optional[float] = None


class FirearmCalculation(BaseModel):
    """Firearm ballistic calculation result."""

    model_config = _MODEL_CONFIG

    firearm: FirearmCalculationFirearm
    ammunition: Optional[FirearmCalculationAmmo] = None
    calculated: Optional[FirearmCalculationCalculated] = None
    source_reported: Optional[FirearmCalculationSourceReported] = None
    delta: Optional[FirearmCalculationDelta] = None
    error: Optional[str] = None


class FirearmLoadProfileAmmo(BaseModel):
    """Nested ammunition detail inside FirearmLoadProfile."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    caliber_id: str
    bullet_weight_g: float
    bullet_type: str


class FirearmLoadProfileCalculated(BaseModel):
    """Calculated values inside FirearmLoadProfile."""

    model_config = _MODEL_CONFIG

    muzzle_velocity_mps: float
    muzzle_energy_j: float
    effective_range_m: float
    terminal_ballistics: TerminalBallistics


class FirearmLoadProfileSourceReported(BaseModel):
    """Source-reported values inside FirearmLoadProfile."""

    model_config = _MODEL_CONFIG

    muzzle_velocity_mps: Optional[float] = None
    muzzle_energy_j: Optional[float] = None
    effective_range_m: Optional[float] = None


class FirearmLoadProfile(BaseModel):
    """Firearm load profile including full trajectory."""

    model_config = _MODEL_CONFIG

    firearm: FirearmCalculationFirearm
    ammunition: Optional[FirearmLoadProfileAmmo] = None
    calculated: Optional[FirearmLoadProfileCalculated] = None
    source_reported: Optional[FirearmLoadProfileSourceReported] = None
    trajectory: Optional[list[TrajectoryPoint]] = None
    error: Optional[str] = None


# Ballistics Result


class BallisticsResult(BaseModel):
    """Ballistics data for a caliber at a given distance."""

    model_config = _MODEL_CONFIG

    caliber_id: str
    distance_m: float
    velocity_fps: float
    energy_ft_lbs: float
    drop_inches: float
    drift_inches: Optional[float] = None
    time_of_flight_s: Optional[float] = None
