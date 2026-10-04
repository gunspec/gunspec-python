"""Pydantic response models: account."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from ..vocabulary import ReportIssueType, ReportStatus, TicketPriority, TicketStatus
from .shared import _MODEL_CONFIG

# Support tickets are the one resource the API serves in snake_case, so the
# field names are the wire names and no camelCase alias is generated.
_SNAKE_CONFIG = ConfigDict(frozen=True, populate_by_name=True)

# User-Scoped Resources


class Favorite(BaseModel):
    """A user's favorited firearm, with enough of the record to render a card.

    ``GET /v1/me/favorites``. snake_case, like the search results and unlike
    ``/v1/firearms``: the endpoint answers its own SQL under column names.
    ``id`` and ``firearm_id`` carry the same slug.
    """

    model_config = _MODEL_CONFIG

    id: str
    firearm_id: str
    favorited_at: str
    name: str
    manufacturer_id: Optional[str] = None
    manufacturer_name: Optional[str] = None
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    status: Optional[str] = None
    year_introduced: Optional[int] = None
    action_type: Optional[str] = None
    country_of_origin: Optional[str] = None
    weight_empty_g: Optional[float] = None
    barrel_length_mm: Optional[float] = None
    svg_line_art_url: Optional[str] = None
    model_3d_url: Optional[str] = None
    favorite_count: int = 0
    images: list[dict[str, Any]] = []


class FavoriteIds(BaseModel):
    """``GET /v1/me/favorites/ids``: the favorited firearm ids, as an object."""

    model_config = _MODEL_CONFIG

    ids: list[str] = []


class FavoriteToggle(BaseModel):
    """Result of toggling a favorite."""

    model_config = _MODEL_CONFIG

    firearm_id: str
    favorited: bool


class DataReport(BaseModel):
    """A user-submitted data quality report."""

    model_config = _MODEL_CONFIG

    id: str
    firearm_id: str
    section: str
    issue_type: ReportIssueType
    description: str
    references: list[str] = []
    suggested_value: Optional[str] = None
    status: ReportStatus
    created_at: Optional[str] = None
    reviewed_at: Optional[str] = None


class SupportTicket(BaseModel):
    """A support ticket summary. The API serves this resource in snake_case
    (``created_at``, ``reply_count``), which the field names match directly."""

    model_config = _SNAKE_CONFIG

    id: str
    subject: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: TicketPriority
    status: TicketStatus
    reply_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    closed_at: Optional[str] = None


class SupportTicketReply(BaseModel):
    """A single reply in a support ticket thread. Snake_case, like the ticket."""

    model_config = _SNAKE_CONFIG

    id: int
    ticket_id: str
    message: str
    created_at: Optional[str] = None


class SupportTicketDetail(SupportTicket):
    """A support ticket with its reply thread."""

    replies: list[SupportTicketReply] = []


class WebhookEndpoint(BaseModel):
    """A webhook endpoint configuration."""

    model_config = _MODEL_CONFIG

    id: str
    url: str
    description: Optional[str] = None
    events: list[str] = []
    active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class WebhookEndpointCreated(WebhookEndpoint):
    """The endpoint as ``POST /v1/me/webhooks`` returns it: the only response
    that carries the signing secret. Store it; it is not shown again."""

    secret: str


class WebhookTestResult(BaseModel):
    """Result of sending a test event to a webhook endpoint."""

    model_config = _MODEL_CONFIG

    delivered: bool
    http_status: Optional[int] = None
    error: Optional[str] = None


class UsageStatsCurrentMonth(BaseModel):
    """This UTC month's usage against the plan's allowance.

    The allowance is enforced for the whole account (every key draws on one
    pool): once ``used`` reaches ``limit`` every call is refused with
    ``MONTHLY_CAP_EXCEEDED`` until ``resets_at``. The same figures ride every
    keyed response as ``X-Monthly-Limit``, ``X-Monthly-Remaining`` and
    ``X-Monthly-Reset`` (see ``response.rate_limit``).
    """

    model_config = _MODEL_CONFIG

    used: int
    """Requests served this month across every key. Calls a limit refused with a
    429, and 304s, are not counted: they spent nothing."""
    limit: int
    remaining: Optional[int] = None
    """Requests left this month, never below zero."""
    percentage: float
    resets_at: str
    """Midnight UTC on the 1st, for every plan."""


class UsageStatsDailyEntry(BaseModel):
    """A daily request count entry."""

    model_config = _MODEL_CONFIG

    date: str
    count: int
    mcp_count: int = 0
    """Of ``count``, the requests made through the hosted MCP server."""


class UsageStatsPerKeyEntry(BaseModel):
    """Per-API-key usage entry."""

    model_config = _MODEL_CONFIG

    key_id: str
    key_name: str
    count: int
    mcp_count: int = 0
    """Of ``count``, the requests made through the hosted MCP server."""
    mcp_today: int = 0
    """MCP calls this key made today (UTC), held against its daily MCP limit."""
    today: int = 0
    """Requests this key made today (UTC), the figure its daily limit is held
    against. Counts calls the limit refused, so it can pass the limit."""
    remaining_today: Optional[int] = None
    """Requests this key has left today, never below zero; ``None`` with no daily ceiling."""


class UsageStatsTier(BaseModel):
    """Current subscription tier details."""

    model_config = _MODEL_CONFIG

    name: str
    requests_per_month: int
    rate_limit: int
    requests_per_day: Optional[int] = None
    """Requests each key may make per UTC day: the limit that is enforced.
    ``None`` on a plan with no daily ceiling."""
    mcp_calls_per_day: Optional[int] = None
    """MCP calls each key may make per UTC day on this plan."""


class UsageStatsDailyKey(BaseModel):
    """The key nearest its daily limit today."""

    model_config = _MODEL_CONFIG

    key_id: str
    key_name: str
    used: int
    """Requests that key made today. Counts calls the limit refused too, so it
    can pass ``limit_per_key``: far past it means the key kept calling after
    being told to stop."""
    remaining: Optional[int] = None
    """Requests that key has left today, never below zero; ``None`` with no daily ceiling."""
    percentage: int
    """Share of ``limit_per_key`` that key has used, rounded. Can exceed 100."""


class UsageStatsDaily(BaseModel):
    """What is left of today, against the limit that is enforced: the daily
    limit, counted per key.

    The same figures ride every ``/v1`` response as ``X-Daily-Limit``,
    ``X-Daily-Remaining`` and ``X-Daily-Reset`` (see ``response.rate_limit``),
    so pacing needs no call to this endpoint. This is the figure to reconcile
    against, and the one that shows every key at once.
    """

    model_config = _MODEL_CONFIG

    limit_per_key: Optional[int] = None
    """Requests one key may make per UTC day on this plan, held against each key
    on its own. ``None`` on a plan with no daily ceiling."""
    used_today: int
    """Requests made today (UTC) across every key. Not comparable with
    ``limit_per_key`` unless the account has one key."""
    busiest_key_today: Optional[UsageStatsDailyKey] = None
    """The key nearest its daily limit, or ``None`` when no key has made a request today."""
    resets_at: str
    """ISO-8601 instant the daily counters return to zero: the next midnight UTC.
    The same as ``X-Daily-Reset``."""


class UsageStatsMcpKey(BaseModel):
    """The key nearest its daily MCP limit today."""

    model_config = _MODEL_CONFIG

    key_id: str
    key_name: str
    used: int
    percentage: int


class UsageStatsMcp(BaseModel):
    """Usage through the hosted MCP server, a subset of the account's requests."""

    model_config = _MODEL_CONFIG

    used_this_month: int
    used_today: int
    daily_limit_per_key: int
    busiest_key_today: Optional[UsageStatsMcpKey] = None
    resets_at: str


class UsageStatsProgress(BaseModel):
    """Your standing: experience earned per call, weighted by what the call is.

    Earned by an SDK, the MCP server, a script or a request tool; a browser, a
    ``304`` and a failed call earn nothing.
    """

    model_config = _MODEL_CONFIG

    xp: int
    """Experience earned across every key on the account, for its whole life."""
    xp_today: int
    """Experience earned today (UTC)."""
    daily_xp_cap: int
    """The most one key can earn in a UTC day."""
    level: int
    """Level, derived from ``xp`` alone."""
    level_starts_at: int
    """The experience this level began at."""
    next_level_at: int
    """The experience the next level begins at."""
    streak_days: int
    """Consecutive days with a call, counting today."""
    days_active: int
    """Days with any call, over the last two years."""
    operations_used: int
    """Documented operations called at least once, counted nightly."""
    operations_available: int
    """Documented operations there are to call, counted from the spec."""


class UsageStatsEndpointCredit(BaseModel):
    """One grant of calls to endpoints above the account's plan."""

    model_config = _MODEL_CONFIG

    id: str
    """Id of the credit."""
    source: str
    """``welcome`` for the one-time grant every account receives, ``staff`` for a credit the team gave you."""
    operations: Optional[list[str]] = None
    """The operations it covers, or ``None`` when it covers everything up to ``max_tier``."""
    max_tier: Optional[str] = None
    """The highest plan whose endpoints it covers, or ``None`` when it names operations."""
    calls_granted: int
    """Calls the credit was given."""
    calls_used: int
    """Calls spent so far."""
    calls_remaining: int
    """Calls left on it; zero once spent, expired or withdrawn."""
    expires_at: Optional[str] = None
    """When it lapses, ISO 8601 UTC, or ``None`` when it does not."""
    status: str
    """``active``, ``spent``, ``expired`` or ``revoked``."""
    created_at: str
    """When it was given."""


class UsageStatsEndpointCredits(BaseModel):
    """Calls to endpoints above the account's plan, shared by every key on it."""

    model_config = _MODEL_CONFIG

    remaining: int
    """Calls left across every credit that can still be spent."""
    credits: list[UsageStatsEndpointCredit] = []
    """Every credit the account has had, newest first, spent ones included."""


class UsageStats(BaseModel):
    """API usage statistics for the authenticated user."""

    model_config = _MODEL_CONFIG

    current_month: UsageStatsCurrentMonth
    daily_breakdown: list[UsageStatsDailyEntry] = []
    per_key: list[UsageStatsPerKeyEntry] = []
    key_count: int
    tier: UsageStatsTier
    daily: Optional[UsageStatsDaily] = None
    """Requests left today against the enforced daily limit; absent from an API that predates it."""
    mcp: Optional[UsageStatsMcp] = None
    """MCP usage; absent from an API that predates it."""
    progress: Optional[UsageStatsProgress] = None
    """Experience, level and streak; absent from an API that predates it."""
    endpoint_credits: Optional[UsageStatsEndpointCredits] = None
    """Calls to endpoints above your plan; absent from an API that predates it."""
