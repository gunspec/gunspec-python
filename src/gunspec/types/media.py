"""Media, name resolution and notice models.

Mirrors ``packages/sdk/src/types/media.ts``.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .vocabulary import MediaKind, NoticeVariant

__all__ = [
    "FirearmMedia",
    "GetFirearmMediaParams",
    "ImageAsset",
    "ImageAssetParams",
    "InlineMediaItem",
    "ListFirearmMediaParams",
    "MediaCatalogItem",
    "MediaCatalogParams",
    "MediaCredit",
    "MediaKind",
    "ResolveAlternative",
    "ResolveResult",
    "ResolveManyResult",
    "SiteNotice",
]

_MODEL_CONFIG = ConfigDict(frozen=True, populate_by_name=True, alias_generator=to_camel)


class InlineMediaItem(BaseModel):
    """An image as it rides inline on a list row: id, URL, kind and dimensions."""

    model_config = _MODEL_CONFIG

    id: int
    url: str
    kind: MediaKind
    alt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class MediaCredit(BaseModel):
    model_config = _MODEL_CONFIG

    source: Optional[str] = None
    author: Optional[str] = None
    source_url: Optional[str] = None
    license: Optional[str] = None


class FirearmMedia(BaseModel):
    """One asset on a firearm (``GET /v1/firearms/{id}/media``)."""

    model_config = _MODEL_CONFIG

    id: Optional[int] = None
    kind: MediaKind
    mime_type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    alt: Optional[str] = None
    url: str
    sizes: Optional[Dict[str, str]] = None
    credit: MediaCredit = MediaCredit()


class MediaCatalogItem(BaseModel):
    """One firearm and its imagery (``GET /v1/firearms/media``)."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    images: List[InlineMediaItem] = []


class ImageAsset(BaseModel):
    """``GET /v1/firearms/{id}/images/{imageId}?format=datauri``."""

    model_config = _MODEL_CONFIG

    id: str
    image_id: int
    variant: str
    format: str
    mime_type: str
    data_uri: str


class ResolveAlternative(BaseModel):
    model_config = _MODEL_CONFIG

    firearm_id: str
    name: str
    manufacturer_name: Optional[str] = None
    match: str
    matched_alias: Optional[str] = None
    score: float


class ResolveResult(BaseModel):
    """``GET /v1/firearms/resolve?q=`` and each row of the batch form."""

    model_config = _MODEL_CONFIG

    query: str
    status: str
    firearm_id: Optional[str] = None
    match: Optional[str] = None
    score: float = 0.0
    matched_tokens: List[str] = []
    unresolved_tokens: List[str] = []
    alternatives: List[ResolveAlternative] = []


class ResolveManyResult(BaseModel):
    """``POST /v1/firearms/resolve``."""

    model_config = _MODEL_CONFIG

    results: List[ResolveResult] = []


class SiteNotice(BaseModel):
    """A banner the website shows (``GET /v1/notices``)."""

    model_config = _MODEL_CONFIG

    id: str
    label: str
    highlight: str
    detail: Optional[str] = None
    variant: NoticeVariant
    cta_label: Optional[str] = None
    cta_url: Optional[str] = None
    priority: Optional[int] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None


class MediaCatalogParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/media``."""

    page: int
    per_page: int
    kind: MediaKind


class ListFirearmMediaParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/{id}/media``."""

    kind: MediaKind


class GetFirearmMediaParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/{id}/media/{selector}``."""

    size: Literal["full", "display", "thumb"]
    stroke_width: int
    stroke_color: str


class ImageAssetParams(TypedDict, total=False):
    """Parameters for ``GET /v1/firearms/{id}/images/{imageId}``."""

    variant: Literal["original", "display", "thumb"]
