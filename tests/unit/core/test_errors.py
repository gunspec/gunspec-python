"""Tests for gunspec._core._errors - error hierarchy and create_api_error factory."""

from __future__ import annotations

import pytest

from gunspec._core._errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConnectError,
    GunSpecError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    RequestTimeoutError,
    ServiceUnavailableError,
    create_api_error,
)

# ---------------------------------------------------------------------------
# Base error
# ---------------------------------------------------------------------------


class TestGunSpecError:
    def test_is_exception_subclass(self) -> None:
        assert issubclass(GunSpecError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(GunSpecError, match="boom"):
            raise GunSpecError("boom")


# ---------------------------------------------------------------------------
# APIError
# ---------------------------------------------------------------------------


class TestAPIError:
    def test_stores_all_fields(self) -> None:
        err = APIError(
            status=418,
            code="TEAPOT",
            message="I'm a teapot",
            request_id="req-1",
            headers={"X-Request-Id": "req-1"},
        )
        assert err.status == 418
        assert err.code == "TEAPOT"
        assert err.message == "I'm a teapot"
        assert err.request_id == "req-1"
        assert err.headers == {"X-Request-Id": "req-1"}

    def test_is_gunspec_error(self) -> None:
        err = APIError(500, "ERR", "msg", "req-1", {})
        assert isinstance(err, GunSpecError)

    def test_str_carries_status_reason_message_and_request_id(self) -> None:
        err = APIError(500, "ERR", "something broke", "req-1", {})
        assert str(err) == "APIError(500 INTERNAL_ERROR): something broke [request_id=req-1]"
        assert err.message == "something broke"


# ---------------------------------------------------------------------------
# Concrete HTTP error subclasses
# ---------------------------------------------------------------------------


class TestAuthenticationError:
    def test_status_is_401(self) -> None:
        err = AuthenticationError("UNAUTHORIZED", "bad key", "req-1", {})
        assert err.status == 401

    def test_is_api_error_and_gunspec_error(self) -> None:
        err = AuthenticationError("UNAUTHORIZED", "bad key", "req-1", {})
        assert isinstance(err, APIError)
        assert isinstance(err, GunSpecError)


class TestPermissionDeniedError:
    def test_status_is_403(self) -> None:
        err = PermissionDeniedError("FORBIDDEN", "nope", "req-1", {})
        assert err.status == 403

    def test_is_api_error(self) -> None:
        assert isinstance(PermissionDeniedError("FORBIDDEN", "nope", "req-1", {}), APIError)


class TestNotFoundError:
    def test_status_is_404(self) -> None:
        err = NotFoundError("NOT_FOUND", "gone", "req-1", {})
        assert err.status == 404

    def test_is_api_error(self) -> None:
        assert isinstance(NotFoundError("NOT_FOUND", "gone", "req-1", {}), APIError)


class TestBadRequestError:
    def test_status_is_400(self) -> None:
        err = BadRequestError("BAD_REQUEST", "invalid", "req-1", {})
        assert err.status == 400

    def test_is_api_error(self) -> None:
        assert isinstance(BadRequestError("BAD_REQUEST", "invalid", "req-1", {}), APIError)


class TestRateLimitError:
    def test_status_is_429(self) -> None:
        err = RateLimitError("RATE_LIMITED", "slow down", "req-1", {}, retry_after=5.0)
        assert err.status == 429

    def test_stores_retry_after(self) -> None:
        err = RateLimitError("RATE_LIMITED", "slow down", "req-1", {}, retry_after=5.0)
        assert err.retry_after == 5.0

    def test_retry_after_can_be_none(self) -> None:
        err = RateLimitError("RATE_LIMITED", "slow down", "req-1", {}, retry_after=None)
        assert err.retry_after is None

    def test_is_api_error(self) -> None:
        assert isinstance(
            RateLimitError("RATE_LIMITED", "slow down", "req-1", {}, retry_after=None),
            APIError,
        )


class TestInternalServerError:
    def test_status_is_500(self) -> None:
        err = InternalServerError("INTERNAL", "oops", "req-1", {})
        assert err.status == 500

    def test_is_api_error(self) -> None:
        assert isinstance(InternalServerError("INTERNAL", "oops", "req-1", {}), APIError)


# ---------------------------------------------------------------------------
# Non-HTTP errors
# ---------------------------------------------------------------------------


class TestConnectError:
    def test_stores_cause(self) -> None:
        cause = OSError("connection reset")
        err = ConnectError("connect failed", cause)
        assert err.cause is cause

    def test_cause_defaults_to_none(self) -> None:
        err = ConnectError("fail")
        assert err.cause is None

    def test_is_gunspec_error_but_not_api_error(self) -> None:
        err = ConnectError("fail")
        assert isinstance(err, GunSpecError)
        assert not isinstance(err, APIError)


class TestRequestTimeoutError:
    def test_stores_timeout_s(self) -> None:
        err = RequestTimeoutError(30.0)
        assert err.timeout_s == 30.0

    def test_message_includes_timeout(self) -> None:
        err = RequestTimeoutError(30.0)
        assert "30.0" in str(err)
        assert "timed out" in str(err).lower()

    def test_is_gunspec_error_but_not_api_error(self) -> None:
        err = RequestTimeoutError(10)
        assert isinstance(err, GunSpecError)
        assert not isinstance(err, APIError)


# ---------------------------------------------------------------------------
# create_api_error factory
# ---------------------------------------------------------------------------


class TestCreateApiError:
    """Tests for the create_api_error() factory function."""

    _body = {"error": {"code": "TEST_CODE", "message": "test message"}}
    _headers = {"X-Request-Id": "req-factory"}

    def test_400_returns_bad_request_error(self) -> None:
        err = create_api_error(400, self._body, "req-1", self._headers)
        assert isinstance(err, BadRequestError)
        assert err.status == 400
        assert err.code == "TEST_CODE"
        assert err.message == "test message"

    def test_401_returns_authentication_error(self) -> None:
        err = create_api_error(401, self._body, "req-1", self._headers)
        assert isinstance(err, AuthenticationError)
        assert err.status == 401

    def test_403_returns_permission_denied_error(self) -> None:
        err = create_api_error(403, self._body, "req-1", self._headers)
        assert isinstance(err, PermissionDeniedError)
        assert err.status == 403

    def test_404_returns_not_found_error(self) -> None:
        err = create_api_error(404, self._body, "req-1", self._headers)
        assert isinstance(err, NotFoundError)
        assert err.status == 404

    def test_429_returns_rate_limit_error(self) -> None:
        err = create_api_error(429, self._body, "req-1", self._headers)
        assert isinstance(err, RateLimitError)
        assert err.status == 429

    def test_500_returns_internal_server_error(self) -> None:
        err = create_api_error(500, self._body, "req-1", self._headers)
        assert isinstance(err, InternalServerError)
        assert err.status == 500

    def test_503_returns_service_unavailable_error(self) -> None:
        err = create_api_error(503, self._body, "req-1", self._headers)
        assert type(err) is ServiceUnavailableError
        assert err.status == 503

    def test_none_body_returns_defaults(self) -> None:
        err = create_api_error(400, None, "req-1", self._headers)
        assert isinstance(err, BadRequestError)
        assert err.code == "HTTP_400"
        assert "400" in err.message

    def test_empty_body_returns_defaults(self) -> None:
        err = create_api_error(401, {}, "req-1", self._headers)
        assert isinstance(err, AuthenticationError)
        assert err.code == "HTTP_401"

    def test_hierarchy_all_api_errors_are_gunspec_errors(self) -> None:
        for status in (400, 401, 403, 404, 429, 500, 503):
            err = create_api_error(status, self._body, "req-1", self._headers)
            assert isinstance(err, APIError), f"status {status} not APIError"
            assert isinstance(err, GunSpecError), f"status {status} not GunSpecError"
