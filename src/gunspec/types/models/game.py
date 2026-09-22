"""Pydantic response models: game."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .shared import _MODEL_CONFIG

# Game Stats


class GameStats(BaseModel):
    """Extracted game statistics for a firearm (0-100 scale per stat)."""

    model_config = _MODEL_CONFIG

    damage: Optional[float] = None
    accuracy: Optional[float] = None
    range: Optional[float] = None
    fire_rate: Optional[float] = None
    mobility: Optional[float] = None
    recoil_control: Optional[float] = None
    reload_speed: Optional[float] = None
    concealment: Optional[float] = None


class GameProfile(BaseModel):
    """Firearm game profile including archetype classification."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    game_damage: Optional[float] = None
    game_accuracy: Optional[float] = None
    game_range: Optional[float] = None
    game_fire_rate: Optional[float] = None
    game_mobility: Optional[float] = None
    game_recoil_control: Optional[float] = None
    game_reload_speed: Optional[float] = None
    game_concealment: Optional[float] = None
    archetype: str
    strengths: list[str] = []
    weaknesses: list[str] = []


class GameMetaItem(BaseModel):
    """A firearm in the game meta listing."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    archetype: str
    game_damage: Optional[float] = None
    game_accuracy: Optional[float] = None
    game_range: Optional[float] = None
    game_fire_rate: Optional[float] = None
    game_mobility: Optional[float] = None
    game_recoil_control: Optional[float] = None
    game_reload_speed: Optional[float] = None
    game_concealment: Optional[float] = None


# Game Endpoints


class BalanceDeviation(BaseModel):
    """A single stat deviation in a balance report."""

    model_config = _MODEL_CONFIG

    stat: str
    value: float
    mean: float
    std_dev: float
    z_score: float


class BalanceEntry(BaseModel):
    """Balance report entry flagging statistical outliers."""

    model_config = _MODEL_CONFIG

    firearm_id: str
    firearm_name: str
    deviations: list[BalanceDeviation] = []


class TierItem(BaseModel):
    """An item within a tier."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    category_id: Optional[str] = None
    value: float


class TierListTiers(BaseModel):
    """Tier groupings (S/A/B/C/D)."""

    model_config = _MODEL_CONFIG

    S: list[TierItem] = []
    A: list[TierItem] = []
    B: list[TierItem] = []
    C: list[TierItem] = []
    D: list[TierItem] = []


class TierList(BaseModel):
    """Tier list grouping for a single game stat."""

    model_config = _MODEL_CONFIG

    stat: str
    tiers: TierListTiers


class MatchupFirearm(BaseModel):
    """A firearm entry in a matchup result."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    stats: GameStats


class MatchupResult(BaseModel):
    """Game matchup result comparing two firearms' game stats."""

    model_config = _MODEL_CONFIG

    a: MatchupFirearm
    b: MatchupFirearm
    verdicts: dict[str, str] = {}
    a_wins: int
    b_wins: int
    draws: int


class RoleRosterItem(BaseModel):
    """A firearm in a role roster."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    role_score: float
    stats: GameStats


class StatDistributionPercentiles(BaseModel):
    """Key percentiles for stat distribution."""

    model_config = _MODEL_CONFIG

    p10: float
    p25: float
    p50: float
    p75: float
    p90: float


class StatDistributionHistogramBucket(BaseModel):
    """A bucket in a stat distribution histogram."""

    model_config = _MODEL_CONFIG

    bucket: str
    count: int


class StatDistribution(BaseModel):
    """Stat distribution / histogram for a single game stat."""

    model_config = _MODEL_CONFIG

    stat: str
    count: int
    mean: float
    median: float
    std_dev: float
    min: float
    max: float
    percentiles: StatDistributionPercentiles
    histogram: list[StatDistributionHistogramBucket] = []


# Game Stats Snapshots


class GameStatsVersion(BaseModel):
    """A versioned snapshot of game stats for all firearms."""

    model_config = _MODEL_CONFIG

    id: int
    version: str
    description: Optional[str] = None
    firearm_count: int
    created_at: str


class GameStatsSnapshotEntry(BaseModel):
    """A single entry in a game-stats snapshot."""

    model_config = _MODEL_CONFIG

    id: int
    snapshot_id: int
    firearm_id: str
    firearm_name: str
    game_damage: Optional[float] = None
    game_accuracy: Optional[float] = None
    game_range: Optional[float] = None
    game_fire_rate: Optional[float] = None
    game_mobility: Optional[float] = None
    game_recoil_control: Optional[float] = None
    game_reload_speed: Optional[float] = None
    game_concealment: Optional[float] = None


# Balance Report


class BalanceReport(BaseModel):
    """Game balance report identifying outlier firearms."""

    model_config = _MODEL_CONFIG

    threshold: float
    total_analyzed: int
    overpowered: list[BalanceEntry] = []
    underpowered: list[BalanceEntry] = []
    deviations: Optional[list[BalanceDeviation]] = None


# Role Roster


class RoleRoster(BaseModel):
    """A roster of firearms suited for a specific game role."""

    model_config = _MODEL_CONFIG

    role: str
    total_considered: int
    firearms: list[RoleRosterItem] = []
