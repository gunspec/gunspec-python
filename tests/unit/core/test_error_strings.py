"""The string forms of every error: what a log line and a traceback show."""

from __future__ import annotations

import json

from gunspec import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    ConnectError,
    GunSpecError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    RequestTimeoutError,
    WebhookSignatureError,
)
from gunspec._core._error_factory import create_api_error

SECRET_HEADER = {"X-API-Key": "gsk_should_never_print", "Retry-After": "3600"}


def _err(status: int, code: str, reason: str, message: str, **details: object) -> APIError:
    body = {"success": False, "error": {"code": code, "reason": reason, "message": message, **details}}
    return create_api_error(status, body, "req-42", SECRET_HEADER)


class TestStr:
    def test_not_found(self) -> None:
        err = _err(404, "NOT_FOUND", "RESOURCE_NOT_FOUND", "Firearm 'x' not found")
        assert str(err) == "NotFoundError(404 RESOURCE_NOT_FOUND): Firearm 'x' not found [request_id=req-42]"

    def test_daily_cap(self) -> None:
        err = _err(429, "DAILY_CAP_EXCEEDED", "DAILY_CAP_EXCEEDED", "Daily cap exceeded")
        assert isinstance(err, RateLimitError) and err.is_daily_cap
        assert str(err).startswith("RateLimitError(429 DAILY_CAP_EXCEEDED): Daily cap exceeded")

    def test_plan_required(self) -> None:
        err = _err(
            403, "SUBSCRIPTION_REQUIRED", "PLAN_REQUIRED", "Studio plan required", requiredTier="studio"
        )
        assert isinstance(err, PermissionDeniedError)
        assert (
            str(err) == "PermissionDeniedError(403 PLAN_REQUIRED): Studio plan required [request_id=req-42]"
        )
        assert err.required_tier == "studio"

    def test_key_invalid(self) -> None:
        err = _err(401, "UNAUTHORIZED", "KEY_INVALID", "Invalid API key")
        assert isinstance(err, AuthenticationError)
        assert str(err) == "AuthenticationError(401 KEY_INVALID): Invalid API key [request_id=req-42]"

    def test_without_request_id(self) -> None:
        err = NotFoundError("NOT_FOUND", "gone", "", {})
        assert str(err) == "NotFoundError(404 RESOURCE_NOT_FOUND): gone"


class TestReprNeverLeaks:
    def test_repr_has_no_headers_or_key(self) -> None:
        err = _err(401, "UNAUTHORIZED", "KEY_INVALID", "Invalid API key")
        text = repr(err)
        assert "gsk_should_never_print" not in text
        assert "headers" not in text
        assert text.startswith("AuthenticationError(status=401, code='UNAUTHORIZED', reason='KEY_INVALID'")

    def test_to_dict_is_json_and_stable(self) -> None:
        err = _err(429, "RATE_LIMITED", "RATE_LIMITED", "slow down")
        payload = json.loads(json.dumps(err.to_dict()))
        assert payload == {
            "name": "RateLimitError",
            "status": 429,
            "code": "RATE_LIMITED",
            "reason": "RATE_LIMITED",
            "message": "slow down",
            "request_id": "req-42",
            "retry_after": 3600.0,
        }
        assert err.action


class TestHierarchy:
    def test_every_error_shares_the_root(self) -> None:
        for cls in (ConfigurationError, WebhookSignatureError, ConnectError, RequestTimeoutError, APIError):
            assert issubclass(cls, GunSpecError), cls.__name__

    def test_transport_reprs(self) -> None:
        assert repr(RequestTimeoutError(2.5)) == "RequestTimeoutError(timeout_s=2.5)"
        assert repr(ConnectError("dns failed")) == "ConnectError('dns failed')"
        assert str(ConfigurationError("bad base_url")) == "bad base_url"
