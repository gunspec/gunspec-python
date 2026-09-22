from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import CreateReportParams, ListReportsParams

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, PaginatedResponse, SyncHttpClient


class Reports:
    """Sync reports resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def create(self, params: CreateReportParams) -> APIResponse[Dict[str, Any]]:
        return self._client.post("/v1/me/reports", body=params)

    def list(self, params: Optional[ListReportsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return self._client.get_paginated("/v1/me/reports", query=params)


class AsyncReports:
    """Async reports resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: CreateReportParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.post("/v1/me/reports", body=params)

    async def list(self, params: Optional[ListReportsParams] = None) -> PaginatedResponse[Dict[str, Any]]:
        return await self._client.get_paginated("/v1/me/reports", query=params)
