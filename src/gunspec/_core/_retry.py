from __future__ import annotations

import asyncio
import math
import random
import time
from dataclasses import dataclass
from typing import Awaitable, Callable, Set, TypeVar

from ._errors import (
    APIError,
    ConnectError,
    RateLimitError,
    RequestTimeoutError,
)

T = TypeVar("T")

IDEMPOTENT_METHODS: Set[str] = {"GET", "PUT", "DELETE"}
RETRYABLE_STATUS_CODES: Set[int] = {408, 429, 500, 502, 503, 504}


@dataclass
class RetryConfig:
    """Configuration for retry behaviour with exponential backoff."""

    max_retries: int = 2
    initial_delay_s: float = 0.5
    max_delay_s: float = 8.0
    multiplier: float = 2.0
    max_retry_after_s: float = 30.0
    """Longest ``Retry-After`` the SDK will honour. A server asking for a
    longer wait (a daily cap resetting at midnight, a monthly cap resetting on
    the 1st, a maintenance window) gets the error raised instead of a sleeping
    process. A reset inside this window is waited out, so a call refused a
    second before midnight succeeds after it."""


def is_retryable(error: BaseException, method: str) -> bool:
    """Determine whether the error is eligible for automatic retry."""
    if method.upper() not in IDEMPOTENT_METHODS:
        return False

    if isinstance(error, (ConnectError, RequestTimeoutError)):
        return True

    if isinstance(error, APIError):
        # A spent daily or monthly allowance is a 429 that backoff will not
        # outlast, so it is retried only when the server says the reset is
        # close: the loop's ``_refuse_long_wait`` raises any wait longer than
        # ``max_retry_after_s`` instead of sleeping through it, which leaves a
        # call refused a second before midnight to wait the second and succeed.
        # Without a ``Retry-After`` there is nothing to say the reset is near,
        # and a refused call is still counted.
        if isinstance(error, RateLimitError) and (error.is_daily_cap or error.is_monthly_cap):
            return error.retry_after is not None
        return error.status in RETRYABLE_STATUS_CODES

    return False


def compute_delay(attempt: int, config: RetryConfig, error: BaseException) -> float:
    """Compute the delay in seconds before the next retry attempt.

    Uses exponential backoff with +-20% jitter, capped at ``config.max_delay_s``.
    For responses carrying a ``Retry-After`` header (429, 503) the returned
    delay is the greater of the computed backoff and the server-requested wait.
    """
    base = config.initial_delay_s * math.pow(config.multiplier, attempt)
    jitter = 1.0 + (random.random() * 0.4 - 0.2)
    delay = min(base * jitter, config.max_delay_s)

    if isinstance(error, APIError) and error.retry_after is not None:
        delay = max(delay, error.retry_after)

    return round(delay, 3)


def _refuse_long_wait(error: BaseException, config: RetryConfig) -> None:
    """A wait the server asked for that is longer than the caller will
    tolerate is their decision to make, not ours to sleep through."""
    if (
        isinstance(error, APIError)
        and error.retry_after is not None
        and error.retry_after > config.max_retry_after_s
    ):
        raise error


def with_retry(
    fn: Callable[[], T],
    method: str,
    config: RetryConfig,
) -> T:
    """Execute a synchronous function with automatic retries on transient failures."""
    last_error: BaseException | None = None

    for attempt in range(config.max_retries + 1):
        try:
            return fn()
        except BaseException as error:
            last_error = error
            is_last = attempt == config.max_retries
            if is_last or not is_retryable(error, method):
                raise
            _refuse_long_wait(error, config)
            delay = compute_delay(attempt, config, error)
            time.sleep(delay)

    # Unreachable but satisfies the type checker.
    assert last_error is not None
    raise last_error


async def async_with_retry(
    fn: Callable[[], Awaitable[T]],
    method: str,
    config: RetryConfig,
) -> T:
    """Execute an async function with automatic retries on transient failures."""
    last_error: BaseException | None = None

    for attempt in range(config.max_retries + 1):
        try:
            return await fn()
        except BaseException as error:
            last_error = error
            is_last = attempt == config.max_retries
            if is_last or not is_retryable(error, method):
                raise
            _refuse_long_wait(error, config)
            delay = compute_delay(attempt, config, error)
            await asyncio.sleep(delay)

    assert last_error is not None
    raise last_error
