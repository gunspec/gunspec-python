"""What the response says about your allowance.

The per-minute three were parsed and shipped for years against an API that
sends none of them, so every reader got ``None`` and no test noticed: the suite
mocked the headers it wanted. These hold the daily figures, which are real, and
hold the phantoms at ``None`` when the API behaves as it actually does.
"""

from datetime import timezone

import httpx

from gunspec._core._response import parse_rate_limit


def test_reads_the_daily_allowance_the_api_really_sends() -> None:
    info = parse_rate_limit(
        httpx.Headers(
            {
                "X-Daily-Limit": "2000",
                "X-Daily-Remaining": "1847",
                "X-Daily-Reset": "2026-09-20T00:00:00.000Z",
            }
        )
    )
    assert info.daily_limit == 2000
    assert info.daily_remaining == 1847
    assert info.daily_reset is not None
    assert info.daily_reset.astimezone(timezone.utc).isoformat() == "2026-09-20T00:00:00+00:00"


def test_leaves_the_per_minute_fields_none() -> None:
    info = parse_rate_limit(httpx.Headers({"X-Daily-Limit": "50", "X-Daily-Remaining": "49"}))
    assert info.limit is None
    assert info.remaining is None
    assert info.reset is None


def test_nulls_an_allowance_a_plan_without_a_ceiling_does_not_send() -> None:
    info = parse_rate_limit(httpx.Headers({}))
    assert info.daily_limit is None
    assert info.daily_remaining is None
    assert info.daily_reset is None


def test_nulls_an_unparseable_reset() -> None:
    assert parse_rate_limit(httpx.Headers({"X-Daily-Reset": "tomorrow"})).daily_reset is None
