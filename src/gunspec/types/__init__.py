"""GunSpec SDK type definitions - models, params, and errors."""

from gunspec.types.compat import Attachment as Attachment
from gunspec.types.compat import AttachmentDetail as AttachmentDetail
from gunspec.types.compat import AttachmentFirearmFit as AttachmentFirearmFit
from gunspec.types.compat import AttachmentFit as AttachmentFit
from gunspec.types.compat import AttachmentManufacturer as AttachmentManufacturer
from gunspec.types.compat import AttachmentStatus as AttachmentStatus
from gunspec.types.compat import CaliberRating as CaliberRating
from gunspec.types.compat import FirearmAttachments as FirearmAttachments
from gunspec.types.compat import FirearmAttachmentsGroup as FirearmAttachmentsGroup
from gunspec.types.compat import FirearmAttachmentsParams as FirearmAttachmentsParams
from gunspec.types.compat import FirearmInterface as FirearmInterface
from gunspec.types.compat import FirearmInterfaces as FirearmInterfaces
from gunspec.types.compat import FitRoute as FitRoute
from gunspec.types.compat import FitSource as FitSource
from gunspec.types.compat import FitType as FitType
from gunspec.types.compat import FitVia as FitVia
from gunspec.types.compat import InterfaceFirearm as InterfaceFirearm
from gunspec.types.compat import InterfaceSource as InterfaceSource
from gunspec.types.compat import InterfaceStandard as InterfaceStandard
from gunspec.types.compat import ListAttachmentsParams as ListAttachmentsParams
from gunspec.types.compat import ListInterfacesParams as ListInterfacesParams
from gunspec.types.compat import OffersParams as OffersParams
from gunspec.types.compat import OfferVendor as OfferVendor
from gunspec.types.compat import Platform as Platform
from gunspec.types.compat import PlatformDetail as PlatformDetail
from gunspec.types.compat import PlatformInterface as PlatformInterface
from gunspec.types.compat import PlatformSummary as PlatformSummary
from gunspec.types.compat import PublicOffer as PublicOffer
from gunspec.types.compat import StandardRef as StandardRef
from gunspec.types.error_reasons import ERROR_REASON_NAMES as ERROR_REASON_NAMES
from gunspec.types.error_reasons import ERROR_REASONS as ERROR_REASONS
from gunspec.types.error_reasons import ErrorReason as ErrorReason
from gunspec.types.error_reasons import is_error_reason as is_error_reason
from gunspec.types.errors import APIErrorResponse as APIErrorResponse
from gunspec.types.errors import ErrorDetail as ErrorDetail
from gunspec.types.media import FirearmMedia as FirearmMedia
from gunspec.types.media import GetFirearmMediaParams as GetFirearmMediaParams
from gunspec.types.media import ImageAsset as ImageAsset
from gunspec.types.media import ImageAssetParams as ImageAssetParams
from gunspec.types.media import InlineMediaItem as InlineMediaItem
from gunspec.types.media import ListFirearmMediaParams as ListFirearmMediaParams
from gunspec.types.media import MediaCatalogItem as MediaCatalogItem
from gunspec.types.media import MediaCatalogParams as MediaCatalogParams
from gunspec.types.media import MediaCredit as MediaCredit
from gunspec.types.media import MediaItemKind as MediaItemKind
from gunspec.types.media import MediaKind as MediaKind
from gunspec.types.media import ResolveAlternative as ResolveAlternative
from gunspec.types.media import ResolveManyResult as ResolveManyResult
from gunspec.types.media import ResolveResult as ResolveResult
from gunspec.types.media import SiteNotice as SiteNotice
from gunspec.types.models import ActionTypeStats as ActionTypeStats
from gunspec.types.models import AdoptionByCountryItem as AdoptionByCountryItem
from gunspec.types.models import AdoptionByTypeItem as AdoptionByTypeItem
from gunspec.types.models import AdoptionMap as AdoptionMap
from gunspec.types.models import AdoptionMapCountry as AdoptionMapCountry
from gunspec.types.models import AdoptionMapUser as AdoptionMapUser
from gunspec.types.models import Ammunition as Ammunition
from gunspec.types.models import BalanceDeviation as BalanceDeviation
from gunspec.types.models import BalanceEntry as BalanceEntry
from gunspec.types.models import BalanceReport as BalanceReport
from gunspec.types.models import BallisticProfile as BallisticProfile
from gunspec.types.models import BallisticProfileAmmo as BallisticProfileAmmo
from gunspec.types.models import BallisticsResult as BallisticsResult
from gunspec.types.models import BulletProfile as BulletProfile
from gunspec.types.models import Caliber as Caliber
from gunspec.types.models import CaliberBallistics as CaliberBallistics
from gunspec.types.models import CaliberBallisticsCaliber as CaliberBallisticsCaliber
from gunspec.types.models import CaliberComparison as CaliberComparison
from gunspec.types.models import CaliberFamily as CaliberFamily
from gunspec.types.models import (
    CaliberPopularityByEra as CaliberPopularityByEra,
)
from gunspec.types.models import (
    CaliberPopularityByEraCaliberEntry as CaliberPopularityByEraCaliberEntry,
)
from gunspec.types.models import CaseMaterial as CaseMaterial
from gunspec.types.models import CaseShape as CaseShape
from gunspec.types.models import Category as Category
from gunspec.types.models import CategoryStats as CategoryStats
from gunspec.types.models import Closure as Closure
from gunspec.types.models import ConfidenceEntry as ConfidenceEntry
from gunspec.types.models import Conflict as Conflict
from gunspec.types.models import ConflictFirearm as ConflictFirearm
from gunspec.types.models import Country as Country
from gunspec.types.models import CountryArsenal as CountryArsenal
from gunspec.types.models import CountryArsenalGroup as CountryArsenalGroup
from gunspec.types.models import DataCoverage as DataCoverage
from gunspec.types.models import DataReport as DataReport
from gunspec.types.models import Dimensions as Dimensions
from gunspec.types.models import DimensionsImperial as DimensionsImperial
from gunspec.types.models import DimensionsMetric as DimensionsMetric
from gunspec.types.models import EraStats as EraStats
from gunspec.types.models import FamilyTree as FamilyTree
from gunspec.types.models import Favorite as Favorite
from gunspec.types.models import FavoriteIds as FavoriteIds
from gunspec.types.models import FavoriteToggle as FavoriteToggle
from gunspec.types.models import FeatureFrequency as FeatureFrequency
from gunspec.types.models import FeatureIcon as FeatureIcon
from gunspec.types.models import FieldCoverage as FieldCoverage
from gunspec.types.models import FilterOptionCategory as FilterOptionCategory
from gunspec.types.models import FilterOptionItem as FilterOptionItem
from gunspec.types.models import FilterOptions as FilterOptions
from gunspec.types.models import Firearm as Firearm
from gunspec.types.models import FirearmCalculation as FirearmCalculation
from gunspec.types.models import FirearmCalculationAmmo as FirearmCalculationAmmo
from gunspec.types.models import (
    FirearmCalculationCalculated as FirearmCalculationCalculated,
)
from gunspec.types.models import FirearmCalculationDelta as FirearmCalculationDelta
from gunspec.types.models import (
    FirearmCalculationFirearm as FirearmCalculationFirearm,
)
from gunspec.types.models import (
    FirearmCalculationSourceReported as FirearmCalculationSourceReported,
)
from gunspec.types.models import FirearmCaliberEntry as FirearmCaliberEntry
from gunspec.types.models import FirearmComparison as FirearmComparison
from gunspec.types.models import FirearmDetail as FirearmDetail
from gunspec.types.models import FirearmImage as FirearmImage
from gunspec.types.models import FirearmListItem as FirearmListItem
from gunspec.types.models import FirearmLoadProfile as FirearmLoadProfile
from gunspec.types.models import FirearmLoadProfileAmmo as FirearmLoadProfileAmmo
from gunspec.types.models import (
    FirearmLoadProfileCalculated as FirearmLoadProfileCalculated,
)
from gunspec.types.models import (
    FirearmLoadProfileSourceReported as FirearmLoadProfileSourceReported,
)
from gunspec.types.models import FirearmSchematic as FirearmSchematic
from gunspec.types.models import FirearmUser as FirearmUser
from gunspec.types.models import FirearmVariant as FirearmVariant
from gunspec.types.models import GameMetaItem as GameMetaItem
from gunspec.types.models import GameProfile as GameProfile
from gunspec.types.models import GameStats as GameStats
from gunspec.types.models import GameStatsSnapshotEntry as GameStatsSnapshotEntry
from gunspec.types.models import GameStatsVersion as GameStatsVersion
from gunspec.types.models import HeadToHead as HeadToHead
from gunspec.types.models import HeadToHeadVerdict as HeadToHeadVerdict
from gunspec.types.models import Manufacturer as Manufacturer
from gunspec.types.models import ManufacturerStats as ManufacturerStats
from gunspec.types.models import (
    ManufacturerStatsAggregates as ManufacturerStatsAggregates,
)
from gunspec.types.models import (
    ManufacturerStatsCategory as ManufacturerStatsCategory,
)
from gunspec.types.models import (
    ManufacturerStatsManufacturer as ManufacturerStatsManufacturer,
)
from gunspec.types.models import ManufacturerTimeline as ManufacturerTimeline
from gunspec.types.models import (
    ManufacturerTimelineFirearm as ManufacturerTimelineFirearm,
)
from gunspec.types.models import (
    ManufacturerTimelineYear as ManufacturerTimelineYear,
)
from gunspec.types.models import MarkingColor as MarkingColor
from gunspec.types.models import MatchupFirearm as MatchupFirearm
from gunspec.types.models import MatchupResult as MatchupResult
from gunspec.types.models import MaterialStats as MaterialStats
from gunspec.types.models import MaterialStatsEntry as MaterialStatsEntry
from gunspec.types.models import PaginatedResponseModel as PaginatedResponseModel
from gunspec.types.models import PaginationMeta as PaginationMeta
from gunspec.types.models import PopularCaliber as PopularCaliber
from gunspec.types.models import PowerRating as PowerRating
from gunspec.types.models import PowerRatingBreakdown as PowerRatingBreakdown
from gunspec.types.models import ProductionStatusItem as ProductionStatusItem
from gunspec.types.models import ProjectileKind as ProjectileKind
from gunspec.types.models import ProlificManufacturer as ProlificManufacturer
from gunspec.types.models import Provenance as Provenance
from gunspec.types.models import ProvenanceCheck as ProvenanceCheck
from gunspec.types.models import ProvenanceChecks as ProvenanceChecks
from gunspec.types.models import ProvenanceFinding as ProvenanceFinding
from gunspec.types.models import ProvenanceReview as ProvenanceReview
from gunspec.types.models import RoleRoster as RoleRoster
from gunspec.types.models import RoleRosterItem as RoleRosterItem
from gunspec.types.models import Silhouette as Silhouette
from gunspec.types.models import SimilarFirearm as SimilarFirearm
from gunspec.types.models import SourceCitation as SourceCitation
from gunspec.types.models import SpecStandard as SpecStandard
from gunspec.types.models import StatDistribution as StatDistribution
from gunspec.types.models import (
    StatDistributionHistogramBucket as StatDistributionHistogramBucket,
)
from gunspec.types.models import (
    StatDistributionPercentiles as StatDistributionPercentiles,
)
from gunspec.types.models import StatsSummary as StatsSummary
from gunspec.types.models import SuccessResponseModel as SuccessResponseModel
from gunspec.types.models import SupportTicket as SupportTicket
from gunspec.types.models import SupportTicketDetail as SupportTicketDetail
from gunspec.types.models import SupportTicketReply as SupportTicketReply
from gunspec.types.models import TerminalBallistics as TerminalBallistics
from gunspec.types.models import TierItem as TierItem
from gunspec.types.models import TierList as TierList
from gunspec.types.models import TierListTiers as TierListTiers
from gunspec.types.models import TimelineItem as TimelineItem
from gunspec.types.models import TopFirearmItem as TopFirearmItem
from gunspec.types.models import TrajectoryPoint as TrajectoryPoint
from gunspec.types.models import UsageStats as UsageStats
from gunspec.types.models import UsageStatsCurrentMonth as UsageStatsCurrentMonth
from gunspec.types.models import UsageStatsDaily as UsageStatsDaily
from gunspec.types.models import UsageStatsDailyEntry as UsageStatsDailyEntry
from gunspec.types.models import UsageStatsDailyKey as UsageStatsDailyKey
from gunspec.types.models import UsageStatsEndpointCredit as UsageStatsEndpointCredit
from gunspec.types.models import UsageStatsEndpointCredits as UsageStatsEndpointCredits
from gunspec.types.models import UsageStatsMcp as UsageStatsMcp
from gunspec.types.models import UsageStatsMcpKey as UsageStatsMcpKey
from gunspec.types.models import UsageStatsPerKeyEntry as UsageStatsPerKeyEntry
from gunspec.types.models import UsageStatsProgress as UsageStatsProgress
from gunspec.types.models import UsageStatsTier as UsageStatsTier
from gunspec.types.models import WebhookEndpoint as WebhookEndpoint
from gunspec.types.models import WebhookEndpointCreated as WebhookEndpointCreated
from gunspec.types.models import WebhookTestResult as WebhookTestResult
from gunspec.types.params import ActionTypesParams as ActionTypesParams
from gunspec.types.params import AdoptionByCountryParams as AdoptionByCountryParams
from gunspec.types.params import AdoptionByTypeParams as AdoptionByTypeParams
from gunspec.types.params import AmmoLoadParams as AmmoLoadParams
from gunspec.types.params import AmmunitionBallisticsParams as AmmunitionBallisticsParams
from gunspec.types.params import BalanceReportParams as BalanceReportParams
from gunspec.types.params import ByActionParams as ByActionParams
from gunspec.types.params import ByConflictParams as ByConflictParams
from gunspec.types.params import ByDesignerParams as ByDesignerParams
from gunspec.types.params import ByEraParams as ByEraParams
from gunspec.types.params import ByFeatureParams as ByFeatureParams
from gunspec.types.params import ByMaterialParams as ByMaterialParams
from gunspec.types.params import (
    CalculateBallisticsParams as CalculateBallisticsParams,
)
from gunspec.types.params import CaliberBallisticsParams as CaliberBallisticsParams
from gunspec.types.params import (
    CaliberPopularityByEraParams as CaliberPopularityByEraParams,
)
from gunspec.types.params import CompareCalibersParams as CompareCalibersParams
from gunspec.types.params import CompareFirearmsParams as CompareFirearmsParams
from gunspec.types.params import ConfidenceParams as ConfidenceParams
from gunspec.types.params import ConflictNameQuery as ConflictNameQuery
from gunspec.types.params import CountryCodeParam as CountryCodeParam
from gunspec.types.params import CreateReplyParams as CreateReplyParams
from gunspec.types.params import CreateReportParams as CreateReportParams
from gunspec.types.params import CreateTicketParams as CreateTicketParams
from gunspec.types.params import (
    CreateWebhookEndpointParams as CreateWebhookEndpointParams,
)
from gunspec.types.params import FeatureFrequencyParams as FeatureFrequencyParams
from gunspec.types.params import GameMetaParams as GameMetaParams
from gunspec.types.params import HeadToHeadParams as HeadToHeadParams
from gunspec.types.params import ListAmmunitionParams as ListAmmunitionParams
from gunspec.types.params import ListBlogPostsParams as ListBlogPostsParams
from gunspec.types.params import ListCalibersParams as ListCalibersParams
from gunspec.types.params import ListChangelogParams as ListChangelogParams
from gunspec.types.params import ListFavoritesParams as ListFavoritesParams
from gunspec.types.params import ListFirearmsParams as ListFirearmsParams
from gunspec.types.params import ListManufacturersParams as ListManufacturersParams
from gunspec.types.params import ListReportsParams as ListReportsParams
from gunspec.types.params import (
    ListSnapshotFirearmsParams as ListSnapshotFirearmsParams,
)
from gunspec.types.params import ListTicketsParams as ListTicketsParams
from gunspec.types.params import (
    ListWebhookEndpointsParams as ListWebhookEndpointsParams,
)
from gunspec.types.params import LoadCarriageParams as LoadCarriageParams
from gunspec.types.params import LoadFirearmParams as LoadFirearmParams
from gunspec.types.params import MatchupsParams as MatchupsParams
from gunspec.types.params import PaginationParams as PaginationParams
from gunspec.types.params import PointBlankParams as PointBlankParams
from gunspec.types.params import PopularCalibersParams as PopularCalibersParams
from gunspec.types.params import PopularFirearmsParams as PopularFirearmsParams
from gunspec.types.params import PowerRatingParams as PowerRatingParams
from gunspec.types.params import (
    ProlificManufacturersParams as ProlificManufacturersParams,
)
from gunspec.types.params import RandomFirearmParams as RandomFirearmParams
from gunspec.types.params import RecoilParams as RecoilParams
from gunspec.types.params import RoleRosterParams as RoleRosterParams
from gunspec.types.params import SearchFirearmsParams as SearchFirearmsParams
from gunspec.types.params import SilhouetteParams as SilhouetteParams
from gunspec.types.params import StatDistributionParams as StatDistributionParams
from gunspec.types.params import TierListParams as TierListParams
from gunspec.types.params import TimelineParams as TimelineParams
from gunspec.types.params import TopFirearmsParams as TopFirearmsParams
from gunspec.types.params import (
    UpdateWebhookEndpointParams as UpdateWebhookEndpointParams,
)
from gunspec.types.params import UsageParams as UsageParams
from gunspec.types.seller import ListVendorOffersParams as ListVendorOffersParams
from gunspec.types.seller import OfferInput as OfferInput
from gunspec.types.seller import PushOffersInput as PushOffersInput
from gunspec.types.seller import PushOffersResult as PushOffersResult
from gunspec.types.seller import UnmatchedOffer as UnmatchedOffer
from gunspec.types.seller import UpdateOfferInput as UpdateOfferInput
from gunspec.types.seller import VendorOffer as VendorOffer
from gunspec.types.seller import VendorScope as VendorScope
from gunspec.types.seller import VendorShop as VendorShop
from gunspec.types.vocabulary import ADOPTION_TYPES as ADOPTION_TYPES
from gunspec.types.vocabulary import ATTACHMENT_STATUSES as ATTACHMENT_STATUSES
from gunspec.types.vocabulary import CHANGELOG_CATEGORIES as CHANGELOG_CATEGORIES
from gunspec.types.vocabulary import FIREARM_ACTION_TYPES as FIREARM_ACTION_TYPES
from gunspec.types.vocabulary import FIREARM_FIRING_MECHANISMS as FIREARM_FIRING_MECHANISMS
from gunspec.types.vocabulary import FIREARM_MAGAZINE_TYPES as FIREARM_MAGAZINE_TYPES
from gunspec.types.vocabulary import FIREARM_STATUSES as FIREARM_STATUSES
from gunspec.types.vocabulary import FIREARM_TRIGGER_TYPES as FIREARM_TRIGGER_TYPES
from gunspec.types.vocabulary import FIT_SOURCES as FIT_SOURCES
from gunspec.types.vocabulary import FIT_TYPES as FIT_TYPES
from gunspec.types.vocabulary import GAME_ARCHETYPES as GAME_ARCHETYPES
from gunspec.types.vocabulary import IMAGE_TYPES as IMAGE_TYPES
from gunspec.types.vocabulary import INTERFACE_SOURCES as INTERFACE_SOURCES
from gunspec.types.vocabulary import MEDIA_KINDS as MEDIA_KINDS
from gunspec.types.vocabulary import NOTICE_VARIANTS as NOTICE_VARIANTS
from gunspec.types.vocabulary import OFFER_STATUSES as OFFER_STATUSES
from gunspec.types.vocabulary import OFFER_TARGET_KINDS as OFFER_TARGET_KINDS
from gunspec.types.vocabulary import REPORT_ISSUE_TYPES as REPORT_ISSUE_TYPES
from gunspec.types.vocabulary import REPORT_STATUSES as REPORT_STATUSES
from gunspec.types.vocabulary import SCHEMATIC_TYPES as SCHEMATIC_TYPES
from gunspec.types.vocabulary import SOURCE_KINDS as SOURCE_KINDS
from gunspec.types.vocabulary import TICKET_CATEGORIES as TICKET_CATEGORIES
from gunspec.types.vocabulary import TICKET_PRIORITIES as TICKET_PRIORITIES
from gunspec.types.vocabulary import TICKET_STATUSES as TICKET_STATUSES
from gunspec.types.vocabulary import AdoptionType as AdoptionType
from gunspec.types.vocabulary import ChangelogCategory as ChangelogCategory
from gunspec.types.vocabulary import FirearmActionType as FirearmActionType
from gunspec.types.vocabulary import FirearmFiringMechanism as FirearmFiringMechanism
from gunspec.types.vocabulary import FirearmMagazineType as FirearmMagazineType
from gunspec.types.vocabulary import FirearmStatus as FirearmStatus
from gunspec.types.vocabulary import FirearmTriggerType as FirearmTriggerType
from gunspec.types.vocabulary import GameArchetype as GameArchetype
from gunspec.types.vocabulary import ImageType as ImageType
from gunspec.types.vocabulary import NoticeVariant as NoticeVariant
from gunspec.types.vocabulary import OfferStatus as OfferStatus
from gunspec.types.vocabulary import OfferTargetKind as OfferTargetKind
from gunspec.types.vocabulary import ReportIssueType as ReportIssueType
from gunspec.types.vocabulary import ReportStatus as ReportStatus
from gunspec.types.vocabulary import SchematicType as SchematicType
from gunspec.types.vocabulary import SourceKind as SourceKind
from gunspec.types.vocabulary import TicketCategory as TicketCategory
from gunspec.types.vocabulary import TicketPriority as TicketPriority
from gunspec.types.vocabulary import TicketStatus as TicketStatus
from gunspec.types.webhook_events import WEBHOOK_EVENT_TYPES as WEBHOOK_EVENT_TYPES
from gunspec.types.webhook_events import WebhookEventType as WebhookEventType
from gunspec.types.webhook_events import is_webhook_event_type as is_webhook_event_type

__all__ = [
    # Errors
    "APIErrorResponse",
    "ErrorDetail",
    # Models - Firearms
    "Firearm",
    "FirearmListItem",
    "FirearmCaliberEntry",
    "FirearmDetail",
    "FirearmVariant",
    # Models - Manufacturers
    "Manufacturer",
    "ManufacturerStats",
    "ManufacturerStatsManufacturer",
    "ManufacturerStatsAggregates",
    "ManufacturerStatsCategory",
    "ManufacturerTimeline",
    "ManufacturerTimelineFirearm",
    "ManufacturerTimelineYear",
    # Models - Calibers
    "Caliber",
    "CaliberBallistics",
    "CaliberBallisticsCaliber",
    "CaliberFamily",
    # Models - Ammunition
    "Ammunition",
    "TrajectoryPoint",
    "TerminalBallistics",
    "BallisticProfile",
    "BallisticProfileAmmo",
    "FirearmCalculation",
    "FirearmCalculationFirearm",
    "FirearmCalculationAmmo",
    "FirearmCalculationCalculated",
    "FirearmCalculationSourceReported",
    "FirearmCalculationDelta",
    "FirearmLoadProfile",
    "FirearmLoadProfileAmmo",
    "FirearmLoadProfileCalculated",
    "FirearmLoadProfileSourceReported",
    # Models - Categories
    "Category",
    "FeatureIcon",
    # Models - Images & Users
    "FirearmImage",
    "FirearmUser",
    # Models - Game Stats
    "GameStats",
    "GameProfile",
    "GameMetaItem",
    # Models - Game Endpoints
    "BalanceDeviation",
    "BalanceEntry",
    "TierItem",
    "TierList",
    "TierListTiers",
    "MatchupFirearm",
    "MatchupResult",
    "RoleRosterItem",
    "StatDistribution",
    "StatDistributionPercentiles",
    "StatDistributionHistogramBucket",
    # Models - Game Stats Snapshots
    "GameStatsVersion",
    "GameStatsSnapshotEntry",
    # Models - Comparisons
    "FirearmComparison",
    "CaliberComparison",
    "HeadToHead",
    "HeadToHeadVerdict",
    # Models - Family Tree
    "FamilyTree",
    # Models - Similar
    "SimilarFirearm",
    # Models - Adoption
    "AdoptionMap",
    "AdoptionMapCountry",
    "AdoptionMapUser",
    # Models - Top / Power / Timeline
    "TopFirearmItem",
    "PowerRating",
    "PowerRatingBreakdown",
    "TimelineItem",
    # Models - Dimensions
    "Dimensions",
    "DimensionsMetric",
    "DimensionsImperial",
    # Models - Filter Options
    "FilterOptions",
    "FilterOptionCategory",
    "FilterOptionItem",
    # Models - Statistics
    "StatsSummary",
    "ProductionStatusItem",
    "FieldCoverage",
    "PopularCaliber",
    "ProlificManufacturer",
    "CategoryStats",
    "EraStats",
    "MaterialStats",
    "MaterialStatsEntry",
    "AdoptionByCountryItem",
    "AdoptionByTypeItem",
    "ActionTypeStats",
    "FeatureFrequency",
    "CaliberPopularityByEra",
    "CaliberPopularityByEraCaliberEntry",
    # Models - Countries & Conflicts
    "Country",
    "CountryArsenal",
    "CountryArsenalGroup",
    "Conflict",
    "ConflictFirearm",
    # Models - Data Quality
    "DataCoverage",
    "ConfidenceEntry",
    # Models - Ballistics & Silhouette
    "BallisticsResult",
    "Silhouette",
    # Models - Balance & Roster
    "BalanceReport",
    "RoleRoster",
    # Models - User Resources
    "Favorite",
    "FavoriteToggle",
    "DataReport",
    "SupportTicket",
    "SupportTicketDetail",
    "SupportTicketReply",
    "WebhookEndpoint",
    "WebhookTestResult",
    "UsageStats",
    "UsageStatsCurrentMonth",
    "UsageStatsDaily",
    "UsageStatsDailyEntry",
    "UsageStatsDailyKey",
    "UsageStatsMcp",
    "UsageStatsMcpKey",
    "UsageStatsEndpointCredit",
    "UsageStatsEndpointCredits",
    "UsageStatsProgress",
    "UsageStatsPerKeyEntry",
    "UsageStatsTier",
    # Models - Response Wrappers
    "PaginatedResponseModel",
    "PaginationMeta",
    "SuccessResponseModel",
    # Params
    "PaginationParams",
    "ListFirearmsParams",
    "SearchFirearmsParams",
    "CompareFirearmsParams",
    "GameMetaParams",
    "RandomFirearmParams",
    "TopFirearmsParams",
    "HeadToHeadParams",
    "ByFeatureParams",
    "ByActionParams",
    "ByMaterialParams",
    "ByDesignerParams",
    "PowerRatingParams",
    "TimelineParams",
    "ByConflictParams",
    "CalculateBallisticsParams",
    "LoadCarriageParams",
    "RecoilParams",
    "PointBlankParams",
    "AmmoLoadParams",
    "LoadFirearmParams",
    "ListManufacturersParams",
    "ListCalibersParams",
    "CompareCalibersParams",
    "CaliberBallisticsParams",
    "ListAmmunitionParams",
    "AmmunitionBallisticsParams",
    "PopularCalibersParams",
    "ProlificManufacturersParams",
    "ByEraParams",
    "AdoptionByCountryParams",
    "AdoptionByTypeParams",
    "ActionTypesParams",
    "FeatureFrequencyParams",
    "CaliberPopularityByEraParams",
    "BalanceReportParams",
    "TierListParams",
    "MatchupsParams",
    "RoleRosterParams",
    "StatDistributionParams",
    "ListSnapshotFirearmsParams",
    "CountryCodeParam",
    "ConflictNameQuery",
    "ConfidenceParams",
    "SilhouetteParams",
    "ListFavoritesParams",
    "CreateReportParams",
    "ListReportsParams",
    "CreateTicketParams",
    "ListTicketsParams",
    "CreateReplyParams",
    "CreateWebhookEndpointParams",
    "UpdateWebhookEndpointParams",
    "ListWebhookEndpointsParams",
    "UsageParams",
    # Provenance, caliber geometry, schematics, webhook creation
    "Provenance",
    "CaseShape",
    "CaseMaterial",
    "ProjectileKind",
    "BulletProfile",
    "Closure",
    "MarkingColor",
    "SpecStandard",
    "FirearmSchematic",
    "WebhookEndpointCreated",
    # Compatibility, sellers, media
    "AttachmentDetail",
    "AttachmentFirearmFit",
    "CaliberRating",
    "FirearmAttachments",
    "FirearmAttachmentsGroup",
    "FitSource",
    "SourceKind",
    "SOURCE_KINDS",
    "ProvenanceCheck",
    "ProvenanceChecks",
    "ProvenanceFinding",
    "ProvenanceReview",
    "SourceCitation",
    "InterfaceFirearm",
    "OfferVendor",
    "PlatformInterface",
    "StandardRef",
    "UnmatchedOffer",
    "InlineMediaItem",
    "ResolveManyResult",
    # Vocabularies (generated)
    "FIREARM_STATUSES",
    "FIREARM_ACTION_TYPES",
    "FIREARM_FIRING_MECHANISMS",
    "FIREARM_TRIGGER_TYPES",
    "FIREARM_MAGAZINE_TYPES",
    "ATTACHMENT_STATUSES",
    "MEDIA_KINDS",
    "IMAGE_TYPES",
    "SCHEMATIC_TYPES",
    "TICKET_STATUSES",
    "TICKET_PRIORITIES",
    "TICKET_CATEGORIES",
    "REPORT_ISSUE_TYPES",
    "REPORT_STATUSES",
    "INTERFACE_SOURCES",
    "FIT_TYPES",
    "FIT_SOURCES",
    "GAME_ARCHETYPES",
    "CHANGELOG_CATEGORIES",
    "NOTICE_VARIANTS",
    "OFFER_STATUSES",
    "OFFER_TARGET_KINDS",
    "ADOPTION_TYPES",
    "FirearmStatus",
    "FirearmActionType",
    "FirearmFiringMechanism",
    "FirearmTriggerType",
    "FirearmMagazineType",
    "ImageType",
    "SchematicType",
    "TicketStatus",
    "TicketPriority",
    "TicketCategory",
    "ReportIssueType",
    "ReportStatus",
    "GameArchetype",
    "ChangelogCategory",
    "NoticeVariant",
    "OfferStatus",
    "OfferTargetKind",
    "AdoptionType",
]
