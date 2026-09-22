"""Request parameter TypedDicts: ammunition."""

from __future__ import annotations

from typing import TypedDict

from .shared import PaginationParams

# Ammunition


class ListAmmunitionParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/ammunition``."""

    caliber_id: str
    bullet_type: str
    is_common: int


class AmmunitionBallisticsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/ammunition/:id/ballistics``."""

    barrel_length_mm: int
    distances: str
