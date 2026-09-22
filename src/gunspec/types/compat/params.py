"""Parameters for the compatibility endpoints."""

from __future__ import annotations

from typing import TypedDict

from ..vocabulary import AttachmentStatus


class ListAttachmentsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/attachments``."""

    page: int
    per_page: int
    category: str
    manufacturer: str
    fits: str
    requires: str
    q: str
    factory: bool
    status: AttachmentStatus
    vendor: str
    only_offered: bool


class FirearmAttachmentsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/{id}/attachments``."""

    category: str
    manufacturer: str
    include: str
    min_confidence: float
    vendor: str
    only_offered: bool
    with_offers: bool


class ListInterfacesParams(TypedDict, total=False):
    """Parameters for ``GET /v1/interfaces``."""

    kind: str


class OffersParams(TypedDict, total=False):
    """Parameters for ``GET /v1/{firearms|attachments}/{id}/offers``."""

    region: str
