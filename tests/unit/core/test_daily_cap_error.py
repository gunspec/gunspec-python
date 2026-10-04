"""What a script is told when the day's allowance is spent.

A daily refusal carries the real time left until the reset (never a fixed
hour), the limit that was reached and the reset instant, in the body and the
headers, and the plan's month says the same. These hold that the error hands
them over as plain values, that the SDK retries one of these refusals only when
the reset is within ``max_retry_after_s`` (a call refused a second before
midnight waits the second and succeeds) and never sleeps through a longer wait,
and that a per-minute refusal and a paused key are unchanged.
"""

from __future__ import annotations

from datetime import timedelta, timezone
from typing import Any, Dict
from unittest.mock import patch

import httpx
import pytest
import respx

from gunspec._core._error_factory import create_api_error
from gunspec._core._errors import PermissionDeniedError, RateLimitError
from gunspec._core._http_client import AsyncHttpClient, HttpClientConfig, SyncHttpClient
from gunspec._core._retry import RetryConfig
from gunspec.types.error_reasons import ERROR_REASONS

BASE = "https://api.gunspec.io"
RESET = "2026-10-03T00:00:00.000Z"

DAILY_BODY: Dict[str, Any] = {
    "success": False,
    "error": {
        "code": "DAILY_CAP_EXCEEDED",
        "reason": "DAILY_CAP_EXCEEDED",
        "message": f"Daily request limit (50) exceeded for tier explorer. Resets at {RESET} (midnight UTC).",
        "limit": 50,
        "resetsAt": RESET,
        "retryAfter": 14400,
    },
}


def _bare(code: str) -> Dict[str, Any]:
    return {"success": False, "error": {"code": code, "reason": code, "message": "x"}}


def _rate_limit(status_body: Dict[str, Any], headers: Dict[str, str]) -> RateLimitError:
    err = create_api_error(429, status_body, "req-1", headers)
    assert isinstance(err, RateLimitError)
    return err


class TestDailyRefusal:
    def test_says_the_limit_and_the_reset_as_plain_values_from_the_body(self) -> None:
        err = _rate_limit(DAILY_BODY, {"Retry-After": "14400"})
        assert err.is_daily_cap
        assert err.daily_limit == 50
        assert err.daily_reset is not None
        assert err.daily_reset.astimezone(timezone.utc).isoformat() == "2026-10-03T00:00:00+00:00"
        assert err.retry_after == 14400

    def test_the_reset_is_timezone_aware_so_it_can_be_compared_with_now(self) -> None:
        err = _rate_limit(DAILY_BODY, {})
        assert err.daily_reset is not None
        assert err.daily_reset.utcoffset() == timedelta(0)

    def test_falls_back_to_the_headers_whatever_case_the_transport_gives_them(self) -> None:
        # httpx lowercases header names when they are turned into a dict.
        err = _rate_limit(
            _bare("DAILY_CAP_EXCEEDED"),
            {"retry-after": "600", "x-daily-limit": "50", "x-daily-reset": RESET},
        )
        assert err.daily_limit == 50
        assert err.daily_reset is not None
        assert err.daily_reset.astimezone(timezone.utc).isoformat() == "2026-10-03T00:00:00+00:00"

    def test_is_none_never_a_bad_value_when_neither_says(self) -> None:
        bare = _rate_limit(_bare("DAILY_CAP_EXCEEDED"), {"Retry-After": "3600"})
        assert bare.daily_limit is None
        assert bare.daily_reset is None

        junk_body: Dict[str, Any] = {
            "success": False,
            "error": {**_bare("DAILY_CAP_EXCEEDED")["error"], "limit": "lots", "resetsAt": "tomorrow"},
        }
        junk = _rate_limit(junk_body, {"X-Daily-Limit": "many", "X-Daily-Reset": "soon"})
        assert junk.daily_limit is None
        assert junk.daily_reset is None

    def test_a_boolean_is_not_a_limit(self) -> None:
        body: Dict[str, Any] = {
            "success": False,
            "error": {**_bare("DAILY_CAP_EXCEEDED")["error"], "limit": True},
        }
        assert _rate_limit(body, {}).daily_limit is None

    def test_uses_the_header_when_the_body_does_not_parse(self) -> None:
        body: Dict[str, Any] = {"success": False, "error": {**DAILY_BODY["error"], "resetsAt": "not a date"}}
        err = _rate_limit(body, {"X-Daily-Reset": RESET})
        assert err.daily_reset is not None
        assert err.daily_reset.astimezone(timezone.utc).isoformat() == "2026-10-03T00:00:00+00:00"

    def test_keeps_the_same_facts_in_details_and_nothing_sensitive_in_the_log_line(self) -> None:
        err = _rate_limit(DAILY_BODY, {"Retry-After": "14400"})
        assert err.details is not None
        assert err.details["limit"] == 50
        assert err.details["resetsAt"] == RESET
        assert "gsk_" not in str(err.to_dict())


class TestMcpShareOfTheDay:
    MCP_BODY: Dict[str, Any] = {
        "success": False,
        "error": {
            **_bare("MCP_DAILY_CAP_EXCEEDED")["error"],
            "limit": 20,
            "resetsAt": RESET,
            "retryAfter": 600,
        },
    }

    def test_is_a_daily_cap_too_so_no_short_wait_helps_unless_the_reset_is_close(self) -> None:
        err = _rate_limit(self.MCP_BODY, {"Retry-After": "600"})
        assert err.is_daily_cap
        assert err.daily_limit == 20
        assert err.daily_reset is not None

    def test_reads_the_mcp_headers_not_the_plan_ones_when_the_body_is_silent(self) -> None:
        err = _rate_limit(
            _bare("MCP_DAILY_CAP_EXCEEDED"),
            {
                "x-daily-limit": "50",
                "x-daily-mcp-limit": "20",
                "x-daily-reset": RESET,
                "x-daily-mcp-reset": RESET,
            },
        )
        assert err.daily_limit == 20


class TestPerMinuteRefusal:
    def test_is_not_a_daily_cap_and_reports_no_daily_facts_even_if_daily_headers_ride_along(self) -> None:
        err = _rate_limit(
            _bare("RATE_LIMITED"),
            {"Retry-After": "60", "X-Daily-Limit": "50", "X-Daily-Reset": RESET},
        )
        assert not err.is_daily_cap
        assert err.daily_limit is None
        assert err.daily_reset is None
        assert err.retry_after == 60

    def test_keeps_the_positional_constructor_for_existing_callers(self) -> None:
        err = RateLimitError("RATE_LIMITED", "slow", "r", {}, 7)
        assert err.daily_limit is None
        assert err.daily_reset is None


def _client(retry: RetryConfig) -> SyncHttpClient:
    return SyncHttpClient(HttpClientConfig(base_url=BASE, api_key="gsk_test", retry=retry))


def _async_client(retry: RetryConfig) -> AsyncHttpClient:
    return AsyncHttpClient(HttpClientConfig(base_url=BASE, api_key="gsk_test", retry=retry))


class TestWhatTheClientDoesWithA429:
    @respx.mock
    def test_surfaces_a_daily_refusal_at_once_however_long_the_wait_with_the_reset_in_hand(self) -> None:
        # Fourteen hours to the reset: far past the default max_retry_after_s of 30.
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(
                429, json=DAILY_BODY, headers={"Retry-After": "50400", "X-Daily-Reset": RESET}
            )
        )
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep, pytest.raises(RateLimitError) as exc:
                client.get("/v1/x")
            assert sleep.call_count == 0
            assert route.call_count == 1
            assert exc.value.is_daily_cap
            assert exc.value.retry_after == 50400
            assert exc.value.daily_limit == 50
            assert exc.value.daily_reset is not None
        finally:
            client.close()

    @respx.mock
    def test_retries_a_daily_refusal_whose_reset_is_a_couple_of_seconds_away(self) -> None:
        # A call refused a second before midnight waits the second and succeeds.
        route = respx.get(f"{BASE}/v1/x").mock(
            side_effect=[
                httpx.Response(429, json=DAILY_BODY, headers={"Retry-After": "2"}),
                httpx.Response(200, json={"success": True, "data": "ok"}, headers={"X-Request-Id": "r1"}),
            ]
        )
        client = _client(RetryConfig(max_retries=2, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep:
                assert client.get("/v1/x").data == "ok"
            assert route.call_count == 2
            assert sleep.call_count == 1
            assert sleep.call_args.args[0] == 2.0
        finally:
            client.close()

    @respx.mock
    def test_retries_the_mcp_share_of_the_day_on_the_same_rule(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            side_effect=[
                httpx.Response(429, json=_bare("MCP_DAILY_CAP_EXCEEDED"), headers={"Retry-After": "2"}),
                httpx.Response(200, json={"success": True, "data": "ok"}, headers={"X-Request-Id": "r1"}),
            ]
        )
        client = _client(RetryConfig(max_retries=2, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep:
                assert client.get("/v1/x").data == "ok"
            assert route.call_count == 2
            assert sleep.call_count == 1
        finally:
            client.close()

    @respx.mock
    def test_does_not_retry_a_daily_refusal_that_asks_for_more_than_the_caller_allows(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(429, json=DAILY_BODY, headers={"Retry-After": "6"})
        )
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001, max_retry_after_s=5.0))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep, pytest.raises(RateLimitError) as exc:
                client.get("/v1/x")
            assert exc.value.is_daily_cap
            assert sleep.call_count == 0
            assert route.call_count == 1
        finally:
            client.close()

    @respx.mock
    def test_does_not_retry_a_daily_refusal_that_sends_no_retry_after(self) -> None:
        # Nothing says the reset is close, and a refused call is still counted.
        route = respx.get(f"{BASE}/v1/x").mock(return_value=httpx.Response(429, json=DAILY_BODY))
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep, pytest.raises(RateLimitError):
                client.get("/v1/x")
            assert sleep.call_count == 0
            assert route.call_count == 1
        finally:
            client.close()

    @respx.mock
    def test_gives_up_after_max_retries_when_the_refusal_repeats_and_never_waits_longer_than_allowed(
        self,
    ) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(429, json=DAILY_BODY, headers={"Retry-After": "2"})
        )
        client = _client(RetryConfig(max_retries=2, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep, pytest.raises(RateLimitError) as exc:
                client.get("/v1/x")
            assert exc.value.is_daily_cap
            # The first call and two retries, each after the two seconds the server asked for.
            assert route.call_count == 3
            assert sleep.call_count == 2
            assert all(call.args[0] <= 30.0 for call in sleep.call_args_list)
        finally:
            client.close()

    @respx.mock
    def test_still_waits_out_a_per_minute_refusal_when_the_wait_is_one_the_caller_allows(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            side_effect=[
                httpx.Response(429, json=_bare("RATE_LIMITED"), headers={"Retry-After": "60"}),
                httpx.Response(200, json={"success": True, "data": "ok"}, headers={"X-Request-Id": "r1"}),
            ]
        )
        client = _client(RetryConfig(max_retries=1, initial_delay_s=0.001, max_retry_after_s=120.0))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep:
                assert client.get("/v1/x").data == "ok"
            assert route.call_count == 2
            assert sleep.call_count == 1
            assert sleep.call_args.args[0] == 60.0
        finally:
            client.close()

    @respx.mock
    def test_surfaces_a_per_minute_refusal_whose_wait_exceeds_what_the_caller_allows_as_before(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(429, json=_bare("RATE_LIMITED"), headers={"Retry-After": "60"})
        )
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with pytest.raises(RateLimitError) as exc:
                client.get("/v1/x")
            assert exc.value.retry_after == 60
            assert not exc.value.is_daily_cap
            assert route.call_count == 1
        finally:
            client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_the_async_client_retries_a_close_reset_and_surfaces_a_far_one(self) -> None:
        close = respx.get(f"{BASE}/v1/near").mock(
            side_effect=[
                httpx.Response(429, json=DAILY_BODY, headers={"Retry-After": "2"}),
                httpx.Response(200, json={"success": True, "data": "ok"}, headers={"X-Request-Id": "r1"}),
            ]
        )
        far = respx.get(f"{BASE}/v1/far").mock(
            return_value=httpx.Response(429, json=DAILY_BODY, headers={"Retry-After": "50400"})
        )
        client = _async_client(RetryConfig(max_retries=2, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.asyncio.sleep") as sleep:
                assert (await client.get("/v1/near")).data == "ok"
                assert sleep.call_count == 1
                with pytest.raises(RateLimitError):
                    await client.get("/v1/far")
                assert sleep.call_count == 1
            assert close.call_count == 2
            assert far.call_count == 1
        finally:
            await client.aclose()

    @respx.mock
    @pytest.mark.asyncio
    async def test_the_async_client_surfaces_a_daily_refusal_at_once_too(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(429, json=DAILY_BODY, headers={"Retry-After": "50400"})
        )
        client = _async_client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.asyncio.sleep") as sleep, pytest.raises(RateLimitError) as exc:
                await client.get("/v1/x")
            assert sleep.call_count == 0
            assert route.call_count == 1
            assert exc.value.daily_reset is not None
        finally:
            await client.aclose()


class TestMonthlyRefusal:
    RESET_MONTH = "2026-11-01T00:00:00.000Z"
    BODY: Dict[str, Any] = {
        "success": False,
        "error": {
            **_bare("MONTHLY_CAP_EXCEEDED")["error"],
            "message": "Monthly request limit (200) reached for your plan (explorer).",
            "limit": 200,
            "resetsAt": "2026-11-01T00:00:00.000Z",
            "retryAfter": 2592000,
        },
    }

    def test_says_the_limit_and_the_reset_as_plain_values_and_is_not_a_daily_cap(self) -> None:
        err = _rate_limit(self.BODY, {"Retry-After": "2592000"})
        assert err.is_monthly_cap
        assert not err.is_daily_cap
        assert err.monthly_limit == 200
        assert err.monthly_reset is not None
        assert err.monthly_reset.isoformat() == "2026-11-01T00:00:00+00:00"
        assert err.retry_after == 2592000
        assert err.daily_limit is None
        assert err.daily_reset is None

    def test_falls_back_to_the_monthly_headers_never_the_daily_ones_whatever_the_case(self) -> None:
        err = _rate_limit(
            _bare("MONTHLY_CAP_EXCEEDED"),
            {
                "x-daily-limit": "50",
                "x-daily-reset": RESET,
                "x-monthly-limit": "200",
                "x-monthly-remaining": "0",
                "x-monthly-reset": self.RESET_MONTH,
            },
        )
        assert err.monthly_limit == 200
        assert err.monthly_reset is not None
        assert err.monthly_reset.isoformat() == "2026-11-01T00:00:00+00:00"

    def test_is_none_never_a_bad_value_when_neither_says(self) -> None:
        bare = _rate_limit(_bare("MONTHLY_CAP_EXCEEDED"), {"Retry-After": "3600"})
        assert bare.monthly_limit is None
        assert bare.monthly_reset is None
        junk_body: Dict[str, Any] = {
            "success": False,
            "error": {**_bare("MONTHLY_CAP_EXCEEDED")["error"], "limit": "lots", "resetsAt": "next month"},
        }
        junk = _rate_limit(junk_body, {"X-Monthly-Limit": "many", "X-Monthly-Reset": "soon"})
        assert junk.monthly_limit is None
        assert junk.monthly_reset is None

    def test_reports_no_monthly_facts_on_any_other_429(self) -> None:
        err = _rate_limit(
            _bare("RATE_LIMITED"),
            {"Retry-After": "60", "X-Monthly-Limit": "200", "X-Monthly-Reset": self.RESET_MONTH},
        )
        assert not err.is_monthly_cap
        assert err.monthly_limit is None
        assert err.monthly_reset is None

    @respx.mock
    def test_surfaces_it_at_once_when_the_reset_is_weeks_away_with_no_sleeping(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(429, json=self.BODY, headers={"Retry-After": "2000000"})
        )
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep, pytest.raises(RateLimitError) as exc:
                client.get("/v1/x")
            assert sleep.call_count == 0
            assert route.call_count == 1
            assert exc.value.is_monthly_cap
            assert exc.value.retry_after == 2000000
            assert exc.value.monthly_reset is not None
        finally:
            client.close()

    @respx.mock
    def test_retries_it_when_the_month_ends_in_a_few_seconds(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            side_effect=[
                httpx.Response(429, json=self.BODY, headers={"Retry-After": "3"}),
                httpx.Response(200, json={"success": True, "data": "ok"}, headers={"X-Request-Id": "r1"}),
            ]
        )
        client = _client(RetryConfig(max_retries=2, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep:
                assert client.get("/v1/x").data == "ok"
            assert route.call_count == 2
            assert sleep.call_args.args[0] == 3.0
        finally:
            client.close()

    @respx.mock
    def test_does_not_retry_one_that_sends_no_retry_after(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(return_value=httpx.Response(429, json=self.BODY))
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with patch("gunspec._core._retry.time.sleep") as sleep, pytest.raises(RateLimitError):
                client.get("/v1/x")
            assert sleep.call_count == 0
            assert route.call_count == 1
        finally:
            client.close()


class TestPausedKey:
    BODY: Dict[str, Any] = {
        "success": False,
        "error": {
            "code": "FORBIDDEN",
            "reason": "KEY_ON_HOLD",
            "message": "This key is paused until 2026-10-03T00:00:00.000Z",
        },
    }

    def test_is_a_permission_error_with_the_seconds_until_the_pause_ends(self) -> None:
        err = create_api_error(403, self.BODY, "req-1", {"Retry-After": "5400"})
        assert isinstance(err, PermissionDeniedError)
        assert err.reason == "KEY_ON_HOLD"
        assert err.retry_after == 5400
        assert err.action == ERROR_REASONS["KEY_ON_HOLD"]["action"]
        assert "Retry-After" in err.action

    @respx.mock
    def test_is_not_retried_by_the_client_because_a_pause_is_not_transient(self) -> None:
        route = respx.get(f"{BASE}/v1/x").mock(
            return_value=httpx.Response(403, json=self.BODY, headers={"Retry-After": "1"})
        )
        client = _client(RetryConfig(max_retries=3, initial_delay_s=0.001))
        try:
            with pytest.raises(PermissionDeniedError):
                client.get("/v1/x")
            assert route.call_count == 1
        finally:
            client.close()
