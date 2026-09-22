"""Attachment compatibility: mount standards, resolved interfaces and platforms."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from ..models.shared import _MODEL_CONFIG
from ..vocabulary import InterfaceSource


class InterfaceStandard(BaseModel):
    """A mount standard the vocabulary knows: ``thread:1/2x28``, ``mag:stanag``."""

    model_config = _MODEL_CONFIG

    id: str
    kind: str
    name: str
    aliases: List[str] = []
    notes: Optional[str] = None


class FirearmInterface(BaseModel):
    """One position on a firearm and the standard it exposes there."""

    model_config = _MODEL_CONFIG

    position: str
    standard_id: str
    name: str
    kind: str
    source: InterfaceSource
    confidence: float
    inherited_from: Optional[str] = None
    notes: Optional[str] = None


class PlatformSummary(BaseModel):
    model_config = _MODEL_CONFIG

    id: str
    name: str


class Platform(PlatformSummary):
    """``GET /v1/platforms`` row."""

    description: Optional[str] = None
    member_count: int = 0


class PlatformInterface(BaseModel):
    """A position a platform defines for every member."""

    model_config = _MODEL_CONFIG

    position: str
    standard_id: str
    name: str
    kind: str
    confidence: float
    notes: Optional[str] = None


class PlatformDetail(PlatformSummary):
    """``GET /v1/platforms/{id}``."""

    description: Optional[str] = None
    interfaces: List[PlatformInterface] = []
    members: List[PlatformSummary] = []


class FirearmInterfaces(BaseModel):
    """``GET /v1/firearms/{id}/interfaces``."""

    model_config = _MODEL_CONFIG

    firearm: PlatformSummary
    platforms: List[PlatformSummary] = []
    interfaces: List[FirearmInterface] = []


class AttachmentManufacturer(BaseModel):
    """A ``{id, name}`` reference to a manufacturer or an adapter."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
