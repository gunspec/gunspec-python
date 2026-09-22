"""A seller's public listing as it appears on a firearm or attachment."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from ..models.shared import _MODEL_CONFIG


class OfferVendor(BaseModel):
    model_config = _MODEL_CONFIG

    id: str
    name: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    verified_domain: Optional[str] = None
    """The domain the shop has proved it controls, re-checked daily. None when it
    has not, which is not a sign the shop is untrustworthy."""


class PublicOffer(BaseModel):
    """A seller's public listing for a firearm or attachment.

    ``price_cents`` is integer minor units; format with the currency, never
    divide first. Link through ``click_id`` so the seller sees the visit.
    """

    model_config = _MODEL_CONFIG

    vendor: OfferVendor
    sku: str
    price_cents: int
    currency: str
    url: str
    in_stock: bool = True
    click_id: Optional[str] = None
    region: Optional[str] = None
    updated_at: Optional[str] = None
