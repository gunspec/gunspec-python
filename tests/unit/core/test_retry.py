"""Tests for gunspec._core._retry - retry config, retryability, backoff, and retry loops."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from gunspec._core._errors import (
    APIError,
    BadRequestError,
    ConnectError,
    RateLimitError,
    RequestTimeoutError,
)
from gunspec._core._retry import (
    RetryConfig,
    async_with_retry,
    compute_delay,
    is_retryable,
    with_retry,
)

# ---------------------------------------------------------------------------
# RetryConfig defaults
# ---------------------------------------------------------------------------


class TestRetryConfig:
    def test_defaults(self) -> None:
        cfg = RetryConfig()
        assert cfg.max_retries == 2
        assert cfg.initial_delay_s == 0.5
        assert cfg.max_delay_s == 8.0
        assert cfg.multiplier == 2.0

    def test_custom_values(self) -> None:
        cfg = RetryConfig(max_retries=5, initial_delay_s=1.0, max_delay_s=60.0, multiplier=3.0)
        assert cfg.max_retries == 5
        assert cfg.initial_delay_s == 1.0
        assert cfg.max_delay_s == 60.0
        assert cfg.multiplier == 3.0


# ---------------------------------------------------------------------------
# is_retryable
# ---------------------------------------------------------------------------


class TestIsRetryable:
    def test_500_get_is_retryable(self) -> None:
        err = APIError(500, "ERR", "boom", "req-1", {})
        assert is_retryable(err, "GET") is True

    def test_500_post_not_retryable(self) -> None:
        err = APIError(500, "ERR", "boom", "req-1", {})
        assert is_retryable(err, "POST") is False

    def test_400_get_not_retryable(self) -> None:
        err = BadRequestError("BAD", "invalid", "req-1", {})
        assert is_retryable(err, "GET") is False

    def test_connect_error_get_retryable(self) -> None:
        err = ConnectError("fail")
        assert is_retryable(err, "GET") is True

    def test_connect_error_post_not_retryable(self) -> None:
        err = ConnectError("fail")
        assert is_retryable(err, "POST") is False

    def test_timeout_error_get_retryable(self) -> None:
        err = RequestTimeoutError(30)
        assert is_retryable(err, "GET") is True

    def test_timeout_error_post_not_retryable(self) -> None:
        err = RequestTimeoutError(30)
        assert is_retryable(err, "POST") is False

    def test_429_get_is_retryable(self) -> None:
        err = RateLimitError("RATE", "slow", "req-1", {}, retry_after=1.0)
        assert is_retryable(err, "GET") is True

    def test_put_is_idempotent(self) -> None:
        err = APIError(500, "ERR", "boom", "req-1", {})
        assert is_retryable(err, "PUT") is True

    def test_delete_is_idempotent(self) -> None:
        err = APIError(500, "ERR", "boom", "req-1", {})
        assert is_retryable(err, "DELETE") is True


# ---------------------------------------------------------------------------
# compute_delay
# ---------------------------------------------------------------------------


class TestComputeDelay:
    def test_first_attempt_around_initial_delay(self) -> None:
        """Attempt 0 should produce ~0.5s with jitter in +-20% range."""
        cfg = RetryConfig()
        err = APIError(500, "ERR", "boom", "req-1", {})
        delays = [compute_delay(0, cfg, err) for _ in range(50)]
        for d in delays:
            assert 0.39 <= d <= 0.61, f"delay {d} outside expected jitter range"

    def test_respects_max_delay(self) -> None:
        cfg = RetryConfig(max_delay_s=1.0, initial_delay_s=2.0)
        err = APIError(500, "ERR", "boom", "req-1", {})
        delay = compute_delay(0, cfg, err)
        assert delay <= 1.0

    def test_exponential_growth(self) -> None:
        """Attempt 1 should have roughly double the base of attempt 0."""
        cfg = RetryConfig(max_delay_s=100.0)
        err = APIError(500, "ERR", "boom", "req-1", {})
        # Use fixed random to test base growth
        with patch("gunspec._core._retry.random.random", return_value=0.5):
            d0 = compute_delay(0, cfg, err)
            d1 = compute_delay(1, cfg, err)
        assert d1 == pytest.approx(d0 * cfg.multiplier, rel=0.01)

    def test_rate_limit_retry_after_respected(self) -> None:
        """When retry_after > computed backoff, use retry_after."""
        cfg = RetryConfig()
        err = RateLimitError("RATE", "slow", "req-1", {}, retry_after=10.0)
        delay = compute_delay(0, cfg, err)
        assert delay >= 10.0

    def test_rate_limit_retry_after_not_used_when_smaller(self) -> None:
        """When retry_after < computed backoff, the computed backoff wins."""
        cfg = RetryConfig(initial_delay_s=5.0, max_delay_s=100.0)
        err = RateLimitError("RATE", "slow", "req-1", {}, retry_after=0.1)
        delay = compute_delay(0, cfg, err)
        assert delay >= 0.1  # at least retry_after
        assert delay >= 3.5  # close to initial_delay (5 * 0.8 jitter low)


# ---------------------------------------------------------------------------
# with_retry (synchronous)
# ---------------------------------------------------------------------------


class TestWithRetry:
    def test_returns_result_on_first_success(self) -> None:
        fn = MagicMock(return_value="ok")
        result = with_retry(fn, "GET", RetryConfig())
        assert result == "ok"
        assert fn.call_count == 1

    @patch("gunspec._core._retry.time.sleep")
    def test_retries_on_retryable_error_then_succeeds(self, mock_sleep: MagicMock) -> None:
        fn = MagicMock(side_effect=[APIError(500, "ERR", "boom", "req-1", {}), "ok"])
        result = with_retry(fn, "GET", RetryConfig(max_retries=2))
        assert result == "ok"
        assert fn.call_count == 2
        assert mock_sleep.call_count == 1

    @patch("gunspec._core._retry.time.sleep")
    def test_raises_after_max_retries_exhausted(self, mock_sleep: MagicMock) -> None:
        err = APIError(500, "ERR", "boom", "req-1", {})
        fn = MagicMock(side_effect=err)
        with pytest.raises(APIError, match="boom"):
            with_retry(fn, "GET", RetryConfig(max_retries=2))
        assert fn.call_count == 3  # initial + 2 retries

    def test_does_not_retry_non_retryable_errors(self) -> None:
        err = BadRequestError("BAD", "invalid", "req-1", {})
        fn = MagicMock(side_effect=err)
        with pytest.raises(BadRequestError, match="invalid"):
            with_retry(fn, "GET", RetryConfig(max_retries=2))
        assert fn.call_count == 1

    def test_does_not_retry_non_idempotent_methods(self) -> None:
        err = APIError(500, "ERR", "boom", "req-1", {})
        fn = MagicMock(side_effect=err)
        with pytest.raises(APIError, match="boom"):
            with_retry(fn, "POST", RetryConfig(max_retries=2))
        assert fn.call_count == 1


# ---------------------------------------------------------------------------
# async_with_retry
# ---------------------------------------------------------------------------


class TestAsyncWithRetry:
    async def test_returns_result_on_first_success(self) -> None:
        call_count = 0

        async def fn() -> str:
            nonlocal call_count
            call_count += 1
            return "ok"

        result = await async_with_retry(fn, "GET", RetryConfig())
        assert result == "ok"
        assert call_count == 1

    @patch("gunspec._core._retry.asyncio.sleep")
    async def test_retries_on_retryable_error_then_succeeds(self, mock_sleep: MagicMock) -> None:
        # Make mock_sleep a proper coroutine
        async def noop_sleep(delay: float) -> None:
            pass

        mock_sleep.side_effect = noop_sleep

        call_count = 0

        async def fn() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise APIError(500, "ERR", "boom", "req-1", {})
            return "ok"

        result = await async_with_retry(fn, "GET", RetryConfig(max_retries=2))
        assert result == "ok"
        assert call_count == 2
        assert mock_sleep.call_count == 1

    @patch("gunspec._core._retry.asyncio.sleep")
    async def test_raises_after_max_retries_exhausted(self, mock_sleep: MagicMock) -> None:
        async def noop_sleep(delay: float) -> None:
            pass

        mock_sleep.side_effect = noop_sleep

        async def fn() -> str:
            raise APIError(500, "ERR", "boom", "req-1", {})

        with pytest.raises(APIError, match="boom"):
            await async_with_retry(fn, "GET", RetryConfig(max_retries=2))
