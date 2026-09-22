"""Closed vocabularies the cartridge illustration is drawn from.

These are inline enums on the API's ``Caliber`` and ``FirearmCaliber`` schemas
rather than entries in ``apps/api/src/config/vocab.ts``, so they are kept here
by hand; ``tests/unit/test_types_mirror.py`` fails when one drifts.
"""

from __future__ import annotations

from typing import Literal

CaseShape = Literal["straight", "tapered", "bottleneck", "none"]
"""The outline the cartridge illustration is drawn with. ``none`` is caseless or a blank."""
CaseMaterial = Literal[
    "brass",
    "nickel_brass",
    "steel",
    "lacquered_steel",
    "aluminium",
    "polymer",
    "paper",
    "caseless",
    "none",
]
ProjectileKind = Literal[
    "bullet",
    "none",
    "shot",
    "slug",
    "round_ball",
    "flechette",
    "dart",
    "pellet",
    "rocket",
    "grenade",
    "signal",
]
"""``none`` is a blank; ``closure`` says what seals the mouth instead."""
BulletProfile = Literal[
    "spitzer",
    "spitzer_boat_tail",
    "round_nose",
    "flat_nose",
    "wadcutter",
    "semi_wadcutter",
    "hollow_point",
    "truncated_cone",
    "round_ball",
]
Closure = Literal["bullet", "star_crimp", "rosette_crimp", "roll_crimp", "fold_crimp", "wad", "paper", "none"]
"""What seals the case mouth."""
MarkingColor = Literal[
    "black",
    "white",
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "brown",
    "grey",
    "silver",
    "gold",
]
"""The paint a load is bought by; null for an ordinary sporting cartridge."""
SpecStandard = Literal["saami", "cip", "nato", "proprietary", "none"]
"""Which body's drawing the dimensions follow."""
