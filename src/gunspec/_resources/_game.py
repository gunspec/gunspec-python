from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import (
    BalanceReportParams,
    MatchupsParams,
    RoleRosterParams,
    StatDistributionParams,
    TierListParams,
)

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, SyncHttpClient


class Game:
    """Sync game resource."""

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def balance_report(
        self, params: Optional[BalanceReportParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/game/balance-report", query=params)

    def tier_list(self, params: Optional[TierListParams] = None) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/game/tier-list", query=params)

    def matchups(self, params: MatchupsParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/game/matchups", query=params)

    def role_roster(self, params: RoleRosterParams) -> APIResponse[List[Dict[str, Any]]]:
        return self._client.get("/v1/game/role-roster", query=params)

    def stat_distribution(self, params: StatDistributionParams) -> APIResponse[Dict[str, Any]]:
        return self._client.get("/v1/game/stat-distribution", query=params)


class AsyncGame:
    """Async game resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def balance_report(
        self, params: Optional[BalanceReportParams] = None
    ) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/game/balance-report", query=params)

    async def tier_list(self, params: Optional[TierListParams] = None) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/game/tier-list", query=params)

    async def matchups(self, params: MatchupsParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/game/matchups", query=params)

    async def role_roster(self, params: RoleRosterParams) -> APIResponse[List[Dict[str, Any]]]:
        return await self._client.get("/v1/game/role-roster", query=params)

    async def stat_distribution(self, params: StatDistributionParams) -> APIResponse[Dict[str, Any]]:
        return await self._client.get("/v1/game/stat-distribution", query=params)
