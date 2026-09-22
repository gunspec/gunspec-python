"""Request parameter TypedDicts: game."""

from __future__ import annotations

from typing import TypedDict

from .shared import PaginationParams

# Game


class BalanceReportParams(TypedDict, total=False):
    """Parameters for ``GET /v1/game/balance``."""

    threshold: int


class TierListParams(TypedDict, total=False):
    """Parameters for ``GET /v1/game/tier-list``."""

    category: str
    stat: str


class _MatchupsRequired(TypedDict):
    a: str
    b: str


class MatchupsParams(_MatchupsRequired, total=False):
    """Parameters for ``GET /v1/game/matchups``."""


class _RoleRosterRequired(TypedDict):
    role: str


class RoleRosterParams(_RoleRosterRequired, total=False):
    """Parameters for ``GET /v1/game/role-roster``."""

    count: int


class _StatDistributionRequired(TypedDict):
    stat: str


class StatDistributionParams(_StatDistributionRequired, total=False):
    """Parameters for ``GET /v1/game/stat-distribution``."""


# Game Stats Snapshots


class ListSnapshotFirearmsParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/game-stats/:version/firearms``."""
