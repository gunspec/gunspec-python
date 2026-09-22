"""Attachment compatibility models and parameters.

Mirrors ``packages/sdk/src/types/compat.ts``. What fits a firearm is computed
from mount interfaces, never from names; the shapes carry the evidence
(``source``, ``confidence``, ``via``) so a caller can show why. Import from
here; the submodules are an implementation detail.
"""

from __future__ import annotations

from ..vocabulary import AttachmentStatus as AttachmentStatus
from ..vocabulary import FitSource as FitSource
from ..vocabulary import FitType as FitType
from ..vocabulary import InterfaceSource as InterfaceSource
from .attachments import Attachment as Attachment
from .attachments import AttachmentDetail as AttachmentDetail
from .attachments import AttachmentFirearmFit as AttachmentFirearmFit
from .attachments import AttachmentFit as AttachmentFit
from .attachments import CaliberRating as CaliberRating
from .attachments import FirearmAttachments as FirearmAttachments
from .attachments import FirearmAttachmentsGroup as FirearmAttachmentsGroup
from .attachments import FitVia as FitVia
from .attachments import InterfaceFirearm as InterfaceFirearm
from .attachments import StandardRef as StandardRef
from .offers import OfferVendor as OfferVendor
from .offers import PublicOffer as PublicOffer
from .params import FirearmAttachmentsParams as FirearmAttachmentsParams
from .params import ListAttachmentsParams as ListAttachmentsParams
from .params import ListInterfacesParams as ListInterfacesParams
from .params import OffersParams as OffersParams
from .standards import AttachmentManufacturer as AttachmentManufacturer
from .standards import FirearmInterface as FirearmInterface
from .standards import FirearmInterfaces as FirearmInterfaces
from .standards import InterfaceStandard as InterfaceStandard
from .standards import Platform as Platform
from .standards import PlatformDetail as PlatformDetail
from .standards import PlatformInterface as PlatformInterface
from .standards import PlatformSummary as PlatformSummary

__all__ = [
    "Attachment",
    "AttachmentDetail",
    "AttachmentFirearmFit",
    "AttachmentFit",
    "AttachmentManufacturer",
    "AttachmentStatus",
    "CaliberRating",
    "FirearmAttachments",
    "FirearmAttachmentsGroup",
    "FirearmAttachmentsParams",
    "FirearmInterface",
    "FirearmInterfaces",
    "FitSource",
    "FitType",
    "FitVia",
    "InterfaceFirearm",
    "InterfaceSource",
    "InterfaceStandard",
    "ListAttachmentsParams",
    "ListInterfacesParams",
    "OffersParams",
    "OfferVendor",
    "Platform",
    "PlatformDetail",
    "PlatformInterface",
    "PlatformSummary",
    "PublicOffer",
    "StandardRef",
]
