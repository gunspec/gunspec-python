"""Request parameter TypedDicts: catalog."""

from __future__ import annotations

from typing import TypedDict

from .shared import PaginationParams

# Manufacturers


class ListManufacturersParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/manufacturers``."""

    country: str


# Calibers


class ListCalibersParams(PaginationParams, total=False):
    """Parameters for ``GET /v1/calibers``."""

    cartridge_type: str
    primer_type: str


class _CompareCalibersRequired(TypedDict):
    ids: str


class CompareCalibersParams(_CompareCalibersRequired, total=False):
    """Parameters for ``GET /v1/calibers/compare``."""


class CaliberBallisticsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/calibers/:id/ballistics``."""

    distance: int


# Countries


class _CountryCodeRequired(TypedDict):
    code: str


class CountryCodeParam(_CountryCodeRequired, total=False):
    """Path parameter for ``GET /v1/countries/:code/arsenal``."""


# Conflicts


class ConflictNameQuery(TypedDict, total=False):
    """Parameters for ``GET /v1/conflicts``."""

    name: str
