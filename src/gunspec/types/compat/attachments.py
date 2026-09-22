"""Attachment compatibility: attachments, fit verdicts and the firearms they fit."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from ..media import InlineMediaItem
from ..models.provenance import Provenance
from ..models.shared import _MODEL_CONFIG
from ..vocabulary import AttachmentStatus, FitSource, FitType, InterfaceSource
from .offers import PublicOffer
from .standards import AttachmentManufacturer, FirearmInterfaces


class Attachment(BaseModel):
    """An attachment as it appears in lists and fit results."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    category: str
    manufacturer: Optional[AttachmentManufacturer] = None
    model_number: Optional[str] = None
    weight_g: Optional[float] = None
    length_mm: Optional[float] = None
    capacity: Optional[int] = None
    bore_diameter_mm: Optional[float] = None
    requires_position: Optional[str] = None
    is_factory_part: bool = False
    factory_for: Optional[str] = None
    stat_mods: Optional[Dict[str, int]] = None
    spec_deltas: Optional[Dict[str, Optional[float]]] = None
    image_url: Optional[str] = None
    status: AttachmentStatus = "in_production"
    data_confidence: Optional[float] = None
    provides: List[str] = []
    provenance: Optional[Provenance] = None
    """Sources, confidence and verification state."""
    updated_at: Optional[str] = None
    version: Optional[str] = None


class StandardRef(BaseModel):
    """An interface standard named on an attachment."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    kind: str


class CaliberRating(BaseModel):
    """What a suppressor or magazine is rated for."""

    model_config = _MODEL_CONFIG

    caliber_id: str
    caliber_name: Optional[str] = None
    min_barrel_length_mm: Optional[float] = None
    full_auto_rated: bool = False
    notes: Optional[str] = None


class AttachmentDetail(Attachment):
    """``GET /v1/attachments/{id}``."""

    description: Optional[str] = None
    specs: Dict[str, Any] = {}
    sources: List[str] = []
    source_url: Optional[str] = None
    year_introduced: Optional[int] = None
    requires: List[List[StandardRef]] = []
    provides: List[StandardRef] = []  # type: ignore[assignment]
    caliber_ratings: List[CaliberRating] = []
    curated_fits: int = 0
    created_at: Optional[str] = None


class FitVia(BaseModel):
    """How a fit was reached."""

    model_config = _MODEL_CONFIG

    position: str
    standard_id: str
    source: InterfaceSource
    adapter_id: Optional[str] = None


class AttachmentFit(Attachment):
    """An attachment with its fit verdict against one firearm."""

    fits: bool = True
    fit_type: Optional[FitType] = None
    source: Optional[FitSource] = None
    """The weakest evidence behind the fit: ``curated`` is a person's verdict,
    ``universal`` needs no interface, the rest name the least trustworthy
    interface row the fit passed through. Treat ``inferred`` as unverified."""
    via: List[FitVia] = []
    adapter: Optional[AttachmentManufacturer] = None
    confidence: float = 0.0
    reason: str = ""
    blocked_by: Optional[str] = None


class FirearmAttachmentsGroup(BaseModel):
    model_config = _MODEL_CONFIG

    category: str
    items: List[AttachmentFit] = []


class FirearmAttachments(FirearmInterfaces):
    """``GET /v1/firearms/{id}/attachments``."""

    groups: List[FirearmAttachmentsGroup] = []
    counts: Dict[str, int] = {}
    total: int = 0
    offers: Optional[Dict[str, List[PublicOffer]]] = None


class AttachmentFirearmFit(BaseModel):
    """A firearm an attachment fits (``GET /v1/attachments/{id}/firearms``)."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    fit_type: Optional[FitType] = None
    source: Optional[FitSource] = None
    confidence: float = 0.0
    reason: str = ""
    via: List[FitVia] = []
    adapter: Optional[AttachmentManufacturer] = None
    manufacturer: Optional[AttachmentManufacturer] = None
    category: Optional[str] = None
    images: List[InlineMediaItem] = []
    svg_line_art_url: Optional[str] = None
    year_introduced: Optional[int] = None


class InterfaceFirearm(BaseModel):
    """A firearm exposing a standard (``GET /v1/interfaces/{id}/firearms``)."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    position: str
    source: InterfaceSource
    confidence: float = 0.0
    manufacturer: Optional[AttachmentManufacturer] = None
    category: Optional[str] = None
    images: List[InlineMediaItem] = []
    svg_line_art_url: Optional[str] = None
    year_introduced: Optional[int] = None
