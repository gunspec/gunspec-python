"""Pydantic response models: provenance."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from ..vocabulary import SourceKind
from .shared import _MODEL_CONFIG


class SourceCitation(BaseModel):
    """One cited page and what kind of source it is.

    ``kind`` is on the hierarchy ``SourceKind`` defines, strongest first; a
    host the API has not classed is ``other``, never guessed.
    """

    model_config = _MODEL_CONFIG

    url: str
    kind: SourceKind


class Provenance(BaseModel):
    """Where a record's figures came from and how far they have been checked.

    Carried as ``provenance`` on a firearm detail, a caliber and an attachment
    detail. Check a specific figure against ``sources`` rather than against
    ``data_confidence``; a null ``verified_at`` means the row is still seed
    model knowledge that nobody has checked against the maker's page.
    """

    model_config = _MODEL_CONFIG

    sources: List[str] = []
    #: Each cited page and its kind, in ``sources`` order.
    source_kinds: List[SourceCitation] = []
    #: The strongest kind among the citations, or None when nothing is cited.
    #: Weigh a figure by this, never by ``len(sources)``.
    best_source_kind: Optional[SourceKind] = None
    data_confidence: Optional[float] = None
    verified_at: Optional[str] = None
    verified_fields: Optional[List[str]] = None
    spec_source: Optional[str] = None
    updated_at: str
    version: Optional[str] = None
