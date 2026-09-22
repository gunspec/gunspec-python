"""Request parameter TypedDicts: firearm analysis."""

from __future__ import annotations

from typing import Literal, TypedDict

# Silhouette


class SilhouetteParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/:id/silhouette``."""

    #: ``raw`` (the SVG file; ``svg`` means the same), ``datauri`` or ``json``.
    format: Literal["raw", "svg", "datauri", "json"]
    stroke_width: float
    stroke_color: str
