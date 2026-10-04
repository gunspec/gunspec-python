"""Pydantic response models: provenance."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

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
    #: The original address when ``url`` is a Wayback Machine capture of it.
    archived_from: Optional[str] = None
    #: The kind's place in the source hierarchy: 0 is the maker, the strongest.
    rank: int = 0
    #: Where the site stands in the source registry.
    tier: Literal["authority", "classified", "unclassified"] = "unclassified"
    #: What the class rests on: a person, a catalogued maker's own site, a .gov or .mil
    #: domain, or nothing yet.
    basis: Literal["declared", "maker", "rule", "unclassified"] = "unclassified"
    #: The words the site was classed on, where a person recorded them.
    evidence: Optional[str] = None


class ProvenanceReview(BaseModel):
    """A person's decision on a proposal; the reviewer is never named."""

    model_config = _MODEL_CONFIG

    decision: Optional[Literal["accepted", "rejected"]] = None
    at: Optional[str] = None


class ProvenanceFinding(BaseModel):
    """What a check found: its own line for the record and the figures it measured."""

    model_config = _MODEL_CONFIG

    why: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None


class ProvenanceCheck(BaseModel):
    """One data-quality task on a record."""

    model_config = _MODEL_CONFIG

    task: str
    number: Optional[int] = None
    check: Optional[str] = None
    kind: str
    agent: Optional[str] = None
    worker: Optional[str] = None
    status: str
    decided_at: Optional[str] = None
    #: What the agent proposed, in its own words; None while the task is open.
    proposed: Optional[str] = None
    fields: List[str] = []
    #: The pages it read.
    sources: List[str] = []
    #: None until a person has reviewed it.
    review: Optional[ProvenanceReview] = None
    #: None where no check raised the task.
    finding: Optional[ProvenanceFinding] = None


class ProvenanceChecks(BaseModel):
    """A record's task trail: the totals and the latest twenty tasks, newest first."""

    model_config = _MODEL_CONFIG

    raised: int = 0
    open: int = 0
    history: List[ProvenanceCheck] = []


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
    #: The first cited page on the record's own manufacturer's website, or None when it cites none.
    #: Cited from the maker is not the same as checked against it: see ``verified_fields``.
    maker_source: Optional[str] = None
    #: How far the figures have been checked, strongest first: ``verified``, ``maker``,
    #: ``authority``, ``secondary`` or ``none``.
    evidence: Literal["verified", "maker", "authority", "secondary", "none"] = "none"
    #: The record's data-quality task trail.
    checks: Optional[ProvenanceChecks] = None
    data_confidence: Optional[float] = None
    verified_at: Optional[str] = None
    verified_fields: Optional[List[str]] = None
    spec_source: Optional[str] = None
    updated_at: str
    version: Optional[str] = None
