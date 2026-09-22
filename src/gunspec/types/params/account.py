"""Request parameter TypedDicts: account."""

from __future__ import annotations

from typing import Optional, TypedDict

# User-Scoped (via /v1/me)


class ListFavoritesParams(TypedDict, total=False):
    """Parameters for ``GET /v1/me/favorites``."""

    page: int
    limit: int


class _CreateReportRequired(TypedDict):
    firearm_id: str
    section: str
    issue_type: str
    description: str


class CreateReportParams(_CreateReportRequired, total=False):
    """Body for ``POST /v1/me/reports``."""

    references: list[str]
    suggested_value: str


class ListReportsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/me/reports``."""

    page: int
    per_page: int


class _CreateTicketRequired(TypedDict):
    subject: str
    description: str


class CreateTicketParams(_CreateTicketRequired, total=False):
    """Body for ``POST /v1/me/support``."""

    category: str
    priority: str


class ListTicketsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/me/support``."""

    page: int
    per_page: int
    status: str
    sort: str
    order: str


class _CreateReplyRequired(TypedDict):
    message: str


class CreateReplyParams(_CreateReplyRequired, total=False):
    """Body for ``POST /v1/me/support/:ticketId/replies``."""


class _CreateWebhookRequired(TypedDict):
    url: str
    events: list[str]


class CreateWebhookEndpointParams(_CreateWebhookRequired, total=False):
    """Body for ``POST /v1/me/webhooks``."""

    description: str


class UpdateWebhookEndpointParams(TypedDict, total=False):
    """Body for ``PUT /v1/me/webhooks/:id``."""

    url: str
    description: Optional[str]
    events: list[str]
    active: bool


class ListWebhookEndpointsParams(TypedDict, total=False):
    """Parameters for ``GET /v1/me/webhooks``."""

    page: int
    per_page: int


class UsageParams(TypedDict, total=False):
    """Parameters for ``GET /v1/me/usage``."""

    month: str
    days: int
