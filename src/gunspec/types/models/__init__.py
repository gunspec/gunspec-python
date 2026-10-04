"""Pydantic response models barrel. Import from here or from the domain module."""

from __future__ import annotations

from .account import (
    DataReport as DataReport,
)
from .account import (
    Favorite as Favorite,
)
from .account import (
    FavoriteIds as FavoriteIds,
)
from .account import (
    FavoriteToggle as FavoriteToggle,
)
from .account import (
    SupportTicket as SupportTicket,
)
from .account import (
    SupportTicketDetail as SupportTicketDetail,
)
from .account import (
    SupportTicketReply as SupportTicketReply,
)
from .account import (
    UsageStats as UsageStats,
)
from .account import (
    UsageStatsCurrentMonth as UsageStatsCurrentMonth,
)
from .account import (
    UsageStatsDaily as UsageStatsDaily,
)
from .account import (
    UsageStatsDailyEntry as UsageStatsDailyEntry,
)
from .account import (
    UsageStatsDailyKey as UsageStatsDailyKey,
)
from .account import (
    UsageStatsEndpointCredit as UsageStatsEndpointCredit,
)
from .account import (
    UsageStatsEndpointCredits as UsageStatsEndpointCredits,
)
from .account import (
    UsageStatsMcp as UsageStatsMcp,
)
from .account import (
    UsageStatsMcpKey as UsageStatsMcpKey,
)
from .account import (
    UsageStatsPerKeyEntry as UsageStatsPerKeyEntry,
)
from .account import (
    UsageStatsProgress as UsageStatsProgress,
)
from .account import (
    UsageStatsTier as UsageStatsTier,
)
from .account import (
    WebhookEndpoint as WebhookEndpoint,
)
from .account import (
    WebhookEndpointCreated as WebhookEndpointCreated,
)
from .account import (
    WebhookTestResult as WebhookTestResult,
)
from .ammunition import (
    Ammunition as Ammunition,
)
from .ammunition import (
    BallisticProfile as BallisticProfile,
)
from .ammunition import (
    BallisticProfileAmmo as BallisticProfileAmmo,
)
from .ammunition import (
    BallisticsResult as BallisticsResult,
)
from .ammunition import (
    FirearmCalculation as FirearmCalculation,
)
from .ammunition import (
    FirearmCalculationAmmo as FirearmCalculationAmmo,
)
from .ammunition import (
    FirearmCalculationCalculated as FirearmCalculationCalculated,
)
from .ammunition import (
    FirearmCalculationDelta as FirearmCalculationDelta,
)
from .ammunition import (
    FirearmCalculationFirearm as FirearmCalculationFirearm,
)
from .ammunition import (
    FirearmCalculationSourceReported as FirearmCalculationSourceReported,
)
from .ammunition import (
    FirearmLoadProfile as FirearmLoadProfile,
)
from .ammunition import (
    FirearmLoadProfileAmmo as FirearmLoadProfileAmmo,
)
from .ammunition import (
    FirearmLoadProfileCalculated as FirearmLoadProfileCalculated,
)
from .ammunition import (
    FirearmLoadProfileSourceReported as FirearmLoadProfileSourceReported,
)
from .ammunition import (
    TerminalBallistics as TerminalBallistics,
)
from .ammunition import (
    TrajectoryPoint as TrajectoryPoint,
)
from .caliber_geometry import (
    BulletProfile as BulletProfile,
)
from .caliber_geometry import (
    CaseMaterial as CaseMaterial,
)
from .caliber_geometry import (
    CaseShape as CaseShape,
)
from .caliber_geometry import (
    Closure as Closure,
)
from .caliber_geometry import (
    MarkingColor as MarkingColor,
)
from .caliber_geometry import (
    ProjectileKind as ProjectileKind,
)
from .caliber_geometry import (
    SpecStandard as SpecStandard,
)
from .catalog import (
    Caliber as Caliber,
)
from .catalog import (
    CaliberBallistics as CaliberBallistics,
)
from .catalog import (
    CaliberBallisticsCaliber as CaliberBallisticsCaliber,
)
from .catalog import (
    CaliberFamily as CaliberFamily,
)
from .catalog import (
    Category as Category,
)
from .catalog import (
    Conflict as Conflict,
)
from .catalog import (
    ConflictFirearm as ConflictFirearm,
)
from .catalog import (
    Country as Country,
)
from .catalog import (
    CountryArsenal as CountryArsenal,
)
from .catalog import (
    CountryArsenalGroup as CountryArsenalGroup,
)
from .catalog import (
    FeatureIcon as FeatureIcon,
)
from .catalog import (
    Manufacturer as Manufacturer,
)
from .catalog import (
    ManufacturerStats as ManufacturerStats,
)
from .catalog import (
    ManufacturerStatsAggregates as ManufacturerStatsAggregates,
)
from .catalog import (
    ManufacturerStatsCategory as ManufacturerStatsCategory,
)
from .catalog import (
    ManufacturerStatsManufacturer as ManufacturerStatsManufacturer,
)
from .catalog import (
    ManufacturerTimeline as ManufacturerTimeline,
)
from .catalog import (
    ManufacturerTimelineFirearm as ManufacturerTimelineFirearm,
)
from .catalog import (
    ManufacturerTimelineYear as ManufacturerTimelineYear,
)
from .firearm import (
    Firearm as Firearm,
)
from .firearm import (
    FirearmCaliberEntry as FirearmCaliberEntry,
)
from .firearm import (
    FirearmDetail as FirearmDetail,
)
from .firearm import (
    FirearmImage as FirearmImage,
)
from .firearm import (
    FirearmListItem as FirearmListItem,
)
from .firearm import (
    FirearmSchematic as FirearmSchematic,
)
from .firearm import (
    FirearmUser as FirearmUser,
)
from .firearm import (
    FirearmVariant as FirearmVariant,
)
from .firearm_analysis import (
    AdoptionMap as AdoptionMap,
)
from .firearm_analysis import (
    AdoptionMapCountry as AdoptionMapCountry,
)
from .firearm_analysis import (
    AdoptionMapUser as AdoptionMapUser,
)
from .firearm_analysis import (
    CaliberComparison as CaliberComparison,
)
from .firearm_analysis import (
    Dimensions as Dimensions,
)
from .firearm_analysis import (
    DimensionsImperial as DimensionsImperial,
)
from .firearm_analysis import (
    DimensionsMetric as DimensionsMetric,
)
from .firearm_analysis import (
    FamilyTree as FamilyTree,
)
from .firearm_analysis import (
    FilterOptionCategory as FilterOptionCategory,
)
from .firearm_analysis import (
    FilterOptionItem as FilterOptionItem,
)
from .firearm_analysis import (
    FilterOptions as FilterOptions,
)
from .firearm_analysis import (
    FirearmComparison as FirearmComparison,
)
from .firearm_analysis import (
    HeadToHead as HeadToHead,
)
from .firearm_analysis import (
    HeadToHeadVerdict as HeadToHeadVerdict,
)
from .firearm_analysis import (
    PowerRating as PowerRating,
)
from .firearm_analysis import (
    PowerRatingBreakdown as PowerRatingBreakdown,
)
from .firearm_analysis import (
    Silhouette as Silhouette,
)
from .firearm_analysis import (
    SimilarFirearm as SimilarFirearm,
)
from .firearm_analysis import (
    TimelineItem as TimelineItem,
)
from .firearm_analysis import (
    TopFirearmItem as TopFirearmItem,
)
from .game import (
    BalanceDeviation as BalanceDeviation,
)
from .game import (
    BalanceEntry as BalanceEntry,
)
from .game import (
    BalanceReport as BalanceReport,
)
from .game import (
    GameMetaItem as GameMetaItem,
)
from .game import (
    GameProfile as GameProfile,
)
from .game import (
    GameStats as GameStats,
)
from .game import (
    GameStatsSnapshotEntry as GameStatsSnapshotEntry,
)
from .game import (
    GameStatsVersion as GameStatsVersion,
)
from .game import (
    MatchupFirearm as MatchupFirearm,
)
from .game import (
    MatchupResult as MatchupResult,
)
from .game import (
    RoleRoster as RoleRoster,
)
from .game import (
    RoleRosterItem as RoleRosterItem,
)
from .game import (
    StatDistribution as StatDistribution,
)
from .game import (
    StatDistributionHistogramBucket as StatDistributionHistogramBucket,
)
from .game import (
    StatDistributionPercentiles as StatDistributionPercentiles,
)
from .game import (
    TierItem as TierItem,
)
from .game import (
    TierList as TierList,
)
from .game import (
    TierListTiers as TierListTiers,
)

# ``catalog`` refers to ``Firearm`` under TYPE_CHECKING to break an import
# cycle; the forward reference is resolved once every module is loaded.
from .provenance import (
    Provenance as Provenance,
)
from .provenance import (
    ProvenanceCheck as ProvenanceCheck,
)
from .provenance import (
    ProvenanceChecks as ProvenanceChecks,
)
from .provenance import (
    ProvenanceFinding as ProvenanceFinding,
)
from .provenance import (
    ProvenanceReview as ProvenanceReview,
)
from .provenance import (
    SourceCitation as SourceCitation,
)
from .shared import (
    PaginatedResponseModel as PaginatedResponseModel,
)
from .shared import (
    PaginationMeta as PaginationMeta,
)
from .shared import (
    SuccessResponseModel as SuccessResponseModel,
)
from .stats import (
    ActionTypeStats as ActionTypeStats,
)
from .stats import (
    AdoptionByCountryItem as AdoptionByCountryItem,
)
from .stats import (
    AdoptionByTypeItem as AdoptionByTypeItem,
)
from .stats import (
    CaliberPopularityByEra as CaliberPopularityByEra,
)
from .stats import (
    CaliberPopularityByEraCaliberEntry as CaliberPopularityByEraCaliberEntry,
)
from .stats import (
    CategoryStats as CategoryStats,
)
from .stats import (
    ConfidenceEntry as ConfidenceEntry,
)
from .stats import (
    DataCoverage as DataCoverage,
)
from .stats import (
    EraStats as EraStats,
)
from .stats import (
    FeatureFrequency as FeatureFrequency,
)
from .stats import (
    FieldCoverage as FieldCoverage,
)
from .stats import (
    MaterialStats as MaterialStats,
)
from .stats import (
    MaterialStatsEntry as MaterialStatsEntry,
)
from .stats import (
    PopularCaliber as PopularCaliber,
)
from .stats import (
    ProductionStatusItem as ProductionStatusItem,
)
from .stats import (
    ProlificManufacturer as ProlificManufacturer,
)
from .stats import (
    StatsSummary as StatsSummary,
)

CountryArsenalGroup.model_rebuild()

__all__ = [
    "PaginatedResponseModel",
    "PaginationMeta",
    "SuccessResponseModel",
    "Firearm",
    "FirearmCaliberEntry",
    "FirearmDetail",
    "FirearmImage",
    "FirearmListItem",
    "FirearmUser",
    "FirearmVariant",
    "Caliber",
    "CaliberBallistics",
    "CaliberBallisticsCaliber",
    "CaliberFamily",
    "Category",
    "FeatureIcon",
    "Conflict",
    "ConflictFirearm",
    "Country",
    "CountryArsenal",
    "CountryArsenalGroup",
    "Manufacturer",
    "ManufacturerStats",
    "ManufacturerStatsAggregates",
    "ManufacturerStatsCategory",
    "ManufacturerStatsManufacturer",
    "ManufacturerTimeline",
    "ManufacturerTimelineFirearm",
    "ManufacturerTimelineYear",
    "Ammunition",
    "BallisticProfile",
    "BallisticProfileAmmo",
    "BallisticsResult",
    "FirearmCalculation",
    "FirearmCalculationAmmo",
    "FirearmCalculationCalculated",
    "FirearmCalculationDelta",
    "FirearmCalculationFirearm",
    "FirearmCalculationSourceReported",
    "FirearmLoadProfile",
    "FirearmLoadProfileAmmo",
    "FirearmLoadProfileCalculated",
    "FirearmLoadProfileSourceReported",
    "TerminalBallistics",
    "TrajectoryPoint",
    "BalanceDeviation",
    "BalanceEntry",
    "BalanceReport",
    "GameMetaItem",
    "GameProfile",
    "GameStats",
    "GameStatsSnapshotEntry",
    "GameStatsVersion",
    "MatchupFirearm",
    "MatchupResult",
    "RoleRoster",
    "RoleRosterItem",
    "StatDistribution",
    "StatDistributionHistogramBucket",
    "StatDistributionPercentiles",
    "TierItem",
    "TierList",
    "TierListTiers",
    "AdoptionMap",
    "AdoptionMapCountry",
    "AdoptionMapUser",
    "CaliberComparison",
    "Dimensions",
    "DimensionsImperial",
    "DimensionsMetric",
    "FamilyTree",
    "FilterOptionCategory",
    "FilterOptionItem",
    "FilterOptions",
    "FirearmComparison",
    "HeadToHead",
    "HeadToHeadVerdict",
    "PowerRating",
    "PowerRatingBreakdown",
    "Silhouette",
    "SimilarFirearm",
    "TimelineItem",
    "TopFirearmItem",
    "ActionTypeStats",
    "AdoptionByCountryItem",
    "AdoptionByTypeItem",
    "CaliberPopularityByEra",
    "CaliberPopularityByEraCaliberEntry",
    "CategoryStats",
    "ConfidenceEntry",
    "DataCoverage",
    "EraStats",
    "FeatureFrequency",
    "FieldCoverage",
    "MaterialStats",
    "MaterialStatsEntry",
    "PopularCaliber",
    "ProductionStatusItem",
    "ProlificManufacturer",
    "StatsSummary",
    "DataReport",
    "Favorite",
    "FavoriteIds",
    "FavoriteToggle",
    "SupportTicket",
    "SupportTicketDetail",
    "SupportTicketReply",
    "UsageStats",
    "UsageStatsCurrentMonth",
    "UsageStatsDailyEntry",
    "UsageStatsMcp",
    "UsageStatsMcpKey",
    "UsageStatsEndpointCredit",
    "UsageStatsEndpointCredits",
    "UsageStatsProgress",
    "UsageStatsPerKeyEntry",
    "UsageStatsTier",
    "WebhookEndpoint",
    "WebhookTestResult",
]
