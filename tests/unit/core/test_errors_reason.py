"""Tests for error.reason, details, retry_after and the new status subclasses."""

from __future__ import annotations

from gunspec._core._errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    PayloadTooLargeError,
    PermissionDeniedError,
    RateLimitError,
    ServiceUnavailableError,
    create_api_error,
)


def _body(code: str, reason: str | None = None, **extra: object) -> dict:
    error: dict = {"code": code, "message": "msg"}
    if reason:
        error["reason"] = reason
    error.update(extra)
    return {"success": False, "error": error}


class TestReason:
    def test_read_from_body(self) -> None:
        err = create_api_error(401, _body("UNAUTHORIZED", "KEY_EXPIRED"), "r1", {})
        assert isinstance(err, AuthenticationError)
        assert err.reason == "KEY_EXPIRED"
        assert "new key" in err.action.lower()

    def test_defaults_by_status_when_absent(self) -> None:
        assert create_api_error(401, _body("UNAUTHORIZED"), "", {}).reason == "AUTH_REQUIRED"
        assert create_api_error(403, None, "", {}).reason == "ACTION_NOT_ALLOWED"
        assert create_api_error(404, None, "", {}).reason == "RESOURCE_NOT_FOUND"
        assert create_api_error(429, None, "", {}).reason == "RATE_LIMITED"
        assert create_api_error(418, None, "", {}).reason == "INTERNAL_ERROR"

    def test_unknown_reason_falls_back(self) -> None:
        err = create_api_error(403, _body("FORBIDDEN", "SOMETHING_NEW"), "", {})
        assert err.reason == "ACTION_NOT_ALLOWED"

    def test_request_id_from_body_when_header_absent(self) -> None:
        err = create_api_error(500, _body("INTERNAL_ERROR", request_id="body-id"), "", {})
        assert err.request_id == "body-id"


class TestDetails:
    def test_merges_details_and_extra_fields(self) -> None:
        err = create_api_error(
            400, _body("VALIDATION_ERROR", "INVALID_PARAMETER", details={"fields": ["q"]}, hint="x"), "", {}
        )
        assert isinstance(err, BadRequestError)
        assert err.details == {"fields": ["q"], "hint": "x"}

    def test_none_when_only_core_fields(self) -> None:
        err = create_api_error(404, _body("NOT_FOUND", request_id="r"), "r", {})
        assert err.details is None

    def test_required_tier(self) -> None:
        err = create_api_error(
            403, _body("SUBSCRIPTION_REQUIRED", "PLAN_REQUIRED", details={"requiredTier": "studio"}), "", {}
        )
        assert isinstance(err, PermissionDeniedError)
        assert err.required_tier == "studio"

    def test_max_bytes(self) -> None:
        err = create_api_error(413, _body("PAYLOAD_TOO_LARGE", maxBytes=1024), "", {})
        assert isinstance(err, PayloadTooLargeError)
        assert err.max_bytes == 1024


class TestNewSubclasses:
    def test_409_conflict(self) -> None:
        assert isinstance(create_api_error(409, None, "", {}), ConflictError)

    def test_503_with_retry_after(self) -> None:
        err = create_api_error(503, _body("SERVICE_UNAVAILABLE", "MAINTENANCE"), "", {"Retry-After": "120"})
        assert isinstance(err, ServiceUnavailableError)
        assert err.reason == "MAINTENANCE"
        assert err.retry_after == 120

    def test_unmapped_stays_base(self) -> None:
        assert type(create_api_error(502, None, "", {})) is APIError


class TestRateLimit:
    def test_daily_cap(self) -> None:
        err = create_api_error(
            429, _body("DAILY_CAP_EXCEEDED", "DAILY_CAP_EXCEEDED"), "", {"Retry-After": "3600"}
        )
        assert isinstance(err, RateLimitError)
        assert err.is_daily_cap
        assert err.retry_after == 3600

    def test_positional_constructor_still_works(self) -> None:
        err = RateLimitError("RATE_LIMITED", "slow", "r", {}, 7)
        assert err.retry_after == 7
        assert not err.is_daily_cap
        assert err.reason == "RATE_LIMITED"


class TestToDict:
    def test_serialises_log_fields_only(self) -> None:
        err = create_api_error(
            403,
            _body("FORBIDDEN", "ACCOUNT_SUSPENDED", details={"since": "2026-01-01"}),
            "req-9",
            {"X-Secret": "no"},
        )
        assert err.to_dict() == {
            "name": "PermissionDeniedError",
            "status": 403,
            "code": "FORBIDDEN",
            "reason": "ACCOUNT_SUSPENDED",
            "message": "msg",
            "request_id": "req-9",
            "details": {"since": "2026-01-01"},
        }
