"""Tests for gunspec._core._http_client - query serialization, sync/async HTTP clients."""

from __future__ import annotations

import httpx
import pytest
import respx

from gunspec._core._errors import BadRequestError
from gunspec._core._http_client import (
    APIResponse,
    AsyncHttpClient,
    HttpClientConfig,
    PaginatedResponse,
    SyncHttpClient,
    serialize_query,
)
from gunspec._core._retry import RetryConfig

# ---------------------------------------------------------------------------
# serialize_query
# ---------------------------------------------------------------------------


class TestSerializeQuery:
    def test_none_returns_empty_dict(self) -> None:
        assert serialize_query(None) == {}

    def test_none_values_skipped(self) -> None:
        assert serialize_query({"a": None}) == {}

    def test_bool_true_becomes_string(self) -> None:
        assert serialize_query({"flag": True}) == {"flag": "true"}

    def test_bool_false_becomes_string(self) -> None:
        assert serialize_query({"flag": False}) == {"flag": "false"}

    def test_list_preserved(self) -> None:
        assert serialize_query({"ids": [1, 2]}) == {"ids": [1, 2]}

    def test_mixed_params_skip_none(self) -> None:
        result = serialize_query({"name": "test", "x": None})
        assert result == {"name": "test"}

    def test_string_passed_through(self) -> None:
        assert serialize_query({"q": "hello"}) == {"q": "hello"}

    def test_int_passed_through(self) -> None:
        assert serialize_query({"page": 2}) == {"page": 2}

    def test_empty_dict_returns_empty_dict(self) -> None:
        assert serialize_query({}) == {}


# ---------------------------------------------------------------------------
# Helper: standard JSON response bodies
# ---------------------------------------------------------------------------

BASE_URL = "https://api.gunspec.io"

RESPONSE_HEADERS = {
    "X-Request-Id": "req-test-1",
    "X-RateLimit-Limit": "100",
    "X-RateLimit-Remaining": "99",
    "X-RateLimit-Reset": "1700000000",
}

SINGLE_BODY = {"success": True, "data": {"id": 1, "name": "AK-47"}}

PAGINATED_BODY = {
    "success": True,
    "data": [{"id": 1}, {"id": 2}],
    "pagination": {"page": 1, "limit": 25, "total": 50, "totalPages": 2},
}

ERROR_BODY = {
    "success": False,
    "error": {"code": "BAD_REQUEST", "message": "invalid input"},
}

# Use a RetryConfig with 0 retries so tests don't loop.
NO_RETRY = RetryConfig(max_retries=0)


# ---------------------------------------------------------------------------
# SyncHttpClient
# ---------------------------------------------------------------------------


class TestSyncHttpClientGet:
    @respx.mock
    def test_get_returns_api_response_with_unwrapped_data(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = SyncHttpClient(config)
        try:
            result = client.get("/v1/firearms/1")
            assert isinstance(result, APIResponse)
            assert result.data == {"id": 1, "name": "AK-47"}
            assert result.status == 200
            assert result.request_id == "req-test-1"
        finally:
            client.close()

    @respx.mock
    def test_get_paginated_returns_paginated_response(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms").mock(
            return_value=httpx.Response(200, json=PAGINATED_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = SyncHttpClient(config)
        try:
            result = client.get_paginated("/v1/firearms")
            assert isinstance(result, PaginatedResponse)
            assert len(result.data) == 2
            assert result.pagination.page == 1
            assert result.pagination.total == 50
            assert result.pagination.total_pages == 2
        finally:
            client.close()

    @respx.mock
    def test_parses_rate_limit_headers(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = SyncHttpClient(config)
        try:
            result = client.get("/v1/firearms/1")
            assert result.rate_limit.limit == 100
            assert result.rate_limit.remaining == 99
            assert result.rate_limit.reset == 1700000000
        finally:
            client.close()

    @respx.mock
    def test_raises_error_on_non_success_status(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms/bad").mock(
            return_value=httpx.Response(400, json=ERROR_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = SyncHttpClient(config)
        try:
            with pytest.raises(BadRequestError) as exc_info:
                client.get("/v1/firearms/bad")
            assert exc_info.value.status == 400
            assert exc_info.value.code == "BAD_REQUEST"
        finally:
            client.close()

    @respx.mock
    def test_sends_api_key_header(self) -> None:
        route = respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, api_key="gs_my_key", retry=NO_RETRY)
        client = SyncHttpClient(config)
        try:
            client.get("/v1/firearms/1")
            assert route.called
            request = route.calls.last.request
            assert request.headers["x-api-key"] == "gs_my_key"
        finally:
            client.close()

    @respx.mock
    def test_sends_user_agent_header(self) -> None:
        route = respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = SyncHttpClient(config)
        try:
            client.get("/v1/firearms/1")
            request = route.calls.last.request
            assert "gunspec-sdk/python" in request.headers["user-agent"]
        finally:
            client.close()


# ---------------------------------------------------------------------------
# AsyncHttpClient
# ---------------------------------------------------------------------------


class TestAsyncHttpClientGet:
    @respx.mock
    async def test_get_returns_api_response(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = AsyncHttpClient(config)
        try:
            result = await client.get("/v1/firearms/1")
            assert isinstance(result, APIResponse)
            assert result.data == {"id": 1, "name": "AK-47"}
            assert result.status == 200
            assert result.request_id == "req-test-1"
        finally:
            await client.aclose()

    @respx.mock
    async def test_get_paginated_returns_paginated_response(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms").mock(
            return_value=httpx.Response(200, json=PAGINATED_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = AsyncHttpClient(config)
        try:
            result = await client.get_paginated("/v1/firearms")
            assert isinstance(result, PaginatedResponse)
            assert len(result.data) == 2
            assert result.pagination.page == 1
            assert result.pagination.total == 50
        finally:
            await client.aclose()

    @respx.mock
    async def test_sends_api_key_header(self) -> None:
        route = respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, api_key="gs_async_key", retry=NO_RETRY)
        client = AsyncHttpClient(config)
        try:
            await client.get("/v1/firearms/1")
            request = route.calls.last.request
            assert request.headers["x-api-key"] == "gs_async_key"
        finally:
            await client.aclose()

    @respx.mock
    async def test_sends_user_agent_header(self) -> None:
        route = respx.get(f"{BASE_URL}/v1/firearms/1").mock(
            return_value=httpx.Response(200, json=SINGLE_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = AsyncHttpClient(config)
        try:
            await client.get("/v1/firearms/1")
            request = route.calls.last.request
            assert "gunspec-sdk/python" in request.headers["user-agent"]
        finally:
            await client.aclose()

    @respx.mock
    async def test_raises_error_on_non_success_status(self) -> None:
        respx.get(f"{BASE_URL}/v1/firearms/bad").mock(
            return_value=httpx.Response(400, json=ERROR_BODY, headers=RESPONSE_HEADERS)
        )
        config = HttpClientConfig(base_url=BASE_URL, retry=NO_RETRY)
        client = AsyncHttpClient(config)
        try:
            with pytest.raises(BadRequestError) as exc_info:
                await client.get("/v1/firearms/bad")
            assert exc_info.value.status == 400
        finally:
            await client.aclose()
