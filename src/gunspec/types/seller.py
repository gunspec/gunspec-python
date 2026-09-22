"""Seller (vendor) models and parameters.

Mirrors ``packages/sdk/src/types/seller.ts``. There is no such thing as a
vendor key: a shop names an ordinary Enterprise key in Profile > Seller, and
that mapping is the entire vendor scope.
"""

from __future__ import annotations

from typing import List, Optional, TypedDict

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .vocabulary import OfferStatus, OfferTargetKind

_MODEL_CONFIG = ConfigDict(frozen=True, populate_by_name=True, alias_generator=to_camel)


class VendorShop(BaseModel):
    """A shop the calling key may act for (``GET /v1/vendor/shops``)."""

    model_config = _MODEL_CONFIG

    id: str
    name: str
    website: Optional[str] = None
    currency: Optional[str] = None
    approved: bool = False


class VendorOffer(BaseModel):
    """One of your own listings as the API holds it, private fields included."""

    model_config = _MODEL_CONFIG

    sku: str
    target_kind: OfferTargetKind
    target_id: str
    price_cents: int
    currency: str
    url: str
    in_stock: bool = True
    stock_qty: Optional[int] = None
    status: OfferStatus = "draft"
    source: str = "feed"
    clicks: int = 0
    updated_at: Optional[str] = None


class UnmatchedOffer(BaseModel):
    """A pushed row whose target id the catalog does not hold."""

    model_config = _MODEL_CONFIG

    sku: str
    target_kind: str
    target_id: str


class PushOffersResult(BaseModel):
    """Result of a push. Unknown ids are reported rather than failing the batch."""

    model_config = _MODEL_CONFIG

    written: int
    unmatched: List[UnmatchedOffer] = []


class ListVendorOffersParams(TypedDict, total=False):
    """Parameters for ``GET /v1/vendor/offers``."""

    page: int
    per_page: int
    vendor: str
    kind: OfferTargetKind
    status: OfferStatus
    q: str


class _OfferInputRequired(TypedDict):
    sku: str
    price_cents: int
    currency: str
    url: str


class OfferInput(_OfferInputRequired, total=False):
    """One row of ``PUT /v1/vendor/offers``. Names exactly one of
    ``attachment_id`` or ``firearm_id``. ``price_cents`` is integer minor units."""

    attachment_id: str
    firearm_id: str
    in_stock: bool
    region: Optional[str]


class PushOffersInput(TypedDict):
    """Body for ``PUT /v1/vendor/offers``: up to 500 rows keyed by your SKU."""

    offers: List[OfferInput]


class UpdateOfferInput(TypedDict, total=False):
    """Body for ``PATCH /v1/vendor/offers/{sku}``. Absent means unchanged. Send
    ``stock_qty`` (the count) or ``in_stock`` (the flag), never both."""

    price_cents: int
    currency: str
    url: str
    stock_qty: int
    in_stock: bool
    region: Optional[str]
    status: OfferStatus


class VendorScope(TypedDict, total=False):
    """``vendor=`` selector shared by the seller write routes."""

    vendor: str
