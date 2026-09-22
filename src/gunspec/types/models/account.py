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
    """Current billing month usage."""

    model_config = _MODEL_CONFIG

    used: int
    limit: int
    percentage: float
    resets_at: str


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


class UsageStatsTier(BaseModel):
    """Current subscription tier details."""

    model_config = _MODEL_CONFIG

    name: str
    requests_per_month: int
    rate_limit: int
    mcp_calls_per_day: Optional[int] = None
    """MCP calls each key may make per UTC day on this plan."""


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


class UsageStats(BaseModel):
    """API usage statistics for the authenticated user."""

    model_config = _MODEL_CONFIG

    current_month: UsageStatsCurrentMonth
    daily_breakdown: list[UsageStatsDailyEntry] = []
    per_key: list[UsageStatsPerKeyEntry] = []
    key_count: int
    tier: UsageStatsTier
    mcp: Optional[UsageStatsMcp] = None
    """MCP usage; absent from an API that predates it."""
    progress: Optional[UsageStatsProgress] = None
    """Experience, level and streak; absent from an API that predates it."""
