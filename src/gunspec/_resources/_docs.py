from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping

if TYPE_CHECKING:
    from .._core._http_client import APIResponse, AsyncHttpClient, SyncHttpClient


class Docs:
    """Sync docs resource.

    Wraps the ``/v1/docs`` endpoints: the API reference and the plan limits as
    data. Any key, Explorer included.
    """

    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get_operations(self, params: Mapping[str, Any]) -> APIResponse[Dict[str, Any]]:
        """What the reference documents for an operation: parameters, plan, caching and failures.

        ``params`` takes ``path`` (a template, concrete path or URL) and optionally ``method``.
        """
        return self._client.get("/v1/docs/operations", query=params)

    def get_sample(self, params: Mapping[str, Any]) -> APIResponse[Dict[str, Any]]:
        """The sample the reference prints for an operation in one language, with its last check.

        ``params`` takes ``path``, ``language`` and, where the path answers several, ``method``.
        """
        return self._client.get("/v1/docs/samples", query=params)

    def get_limits(self) -> APIResponse[Dict[str, Any]]:
        """What each plan allows, from the configuration the API enforces."""
        return self._client.get("/v1/docs/limits")


class AsyncDocs:
    """Async docs resource."""

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get_operations(self, params: Mapping[str, Any]) -> APIResponse[Dict[str, Any]]:
        """What the reference documents for an operation: parameters, plan, caching and failures."""
        return await self._client.get("/v1/docs/operations", query=params)

    async def get_sample(self, params: Mapping[str, Any]) -> APIResponse[Dict[str, Any]]:
        """The sample the reference prints for an operation in one language, with its last check."""
        return await self._client.get("/v1/docs/samples", query=params)

    async def get_limits(self) -> APIResponse[Dict[str, Any]]:
        """What each plan allows, from the configuration the API enforces."""
        return await self._client.get("/v1/docs/limits")
