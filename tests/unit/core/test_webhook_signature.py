"""Tests for gunspec._core._webhook_signature."""

from __future__ import annotations

import hashlib
import hmac
import json

import pytest

from gunspec._core._webhook_signature import (
    WEBHOOK_HEADERS,
    WebhookSignatureError,
    construct_webhook_event,
    parse_signature_header,
    sign_webhook_payload,
    verify_webhook_signature,
)

# A throwaway HMAC key for the test vectors below; it authenticates nothing.
TEST_HMAC_KEY = "unit-test-hmac-key"
NOW = 1_800_000_000


def _now() -> float:
    return float(NOW)


def _signed(body: str, key: str = TEST_HMAC_KEY, at: int = NOW) -> str:
    return f"t={at},v1={sign_webhook_payload(key, at, body)}"


BODY = json.dumps(
    {"id": "evt_1", "type": "firearm.updated", "created_at": "2026-01-01T00:00:00Z", "data": {"id": "ak-47"}},
    separators=(",", ":"),
)


class TestSignWebhookPayload:
    def test_matches_the_api(self) -> None:
        expected = hmac.new(TEST_HMAC_KEY.encode(), b'1700000000.{"a":1}', hashlib.sha256).hexdigest()
        assert sign_webhook_payload(TEST_HMAC_KEY, 1700000000, '{"a":1}') == expected


class TestParseSignatureHeader:
    def test_reads_t_and_v1(self) -> None:
        assert parse_signature_header("t=12,v1=abcd") == (12, ["abcd"])

    def test_accepts_several_v1_and_ignores_unknown(self) -> None:
        assert parse_signature_header("t=12,v1=aa,v0=zz,v1=BB")[1] == ["aa", "bb"]

    def test_rejects_missing_parts(self) -> None:
        with pytest.raises(WebhookSignatureError):
            parse_signature_header(None)
        with pytest.raises(WebhookSignatureError, match="timestamp"):
            parse_signature_header("v1=abcd")
        with pytest.raises(WebhookSignatureError, match="v1"):
            parse_signature_header("t=12")
        with pytest.raises(WebhookSignatureError, match="v1"):
            parse_signature_header("t=12,v1=not-hex")


class TestVerifyWebhookSignature:
    def test_accepts_genuine_delivery(self) -> None:
        verify_webhook_signature(BODY, _signed(BODY), TEST_HMAC_KEY, now=_now)

    def test_accepts_bytes_body(self) -> None:
        verify_webhook_signature(BODY.encode(), _signed(BODY), TEST_HMAC_KEY, now=_now)

    def test_rejects_tampered_body(self) -> None:
        with pytest.raises(WebhookSignatureError, match="does not match"):
            verify_webhook_signature(BODY.replace("ak-47", "ak-74"), _signed(BODY), TEST_HMAC_KEY, now=_now)

    def test_rejects_wrong_key(self) -> None:
        with pytest.raises(WebhookSignatureError, match="does not match"):
            verify_webhook_signature(BODY, _signed(BODY, "other-key"), TEST_HMAC_KEY, now=_now)

    def test_rejects_replay_outside_tolerance(self) -> None:
        old = NOW - 600
        with pytest.raises(WebhookSignatureError, match="tolerance"):
            verify_webhook_signature(BODY, _signed(BODY, at=old), TEST_HMAC_KEY, now=_now)
        verify_webhook_signature(BODY, _signed(BODY, at=old), TEST_HMAC_KEY, tolerance_seconds=900, now=_now)

    def test_rejects_empty_key(self) -> None:
        with pytest.raises(WebhookSignatureError, match="empty"):
            verify_webhook_signature(BODY, _signed(BODY), "", now=_now)


class TestConstructWebhookEvent:
    def test_verifies_then_parses(self) -> None:
        body = json.dumps(
            {"id": "evt_2", "type": "catalog.resynced", "created_at": "x", "data": {"reason": "HASH"}}
        )
        event = construct_webhook_event(body, _signed(body), TEST_HMAC_KEY, now=_now)
        assert event["type"] == "catalog.resynced"
        assert event["data"]["reason"] == "HASH"

    def test_lets_unknown_event_type_through(self) -> None:
        body = json.dumps({"id": "evt_3", "type": "firearm.renamed", "created_at": "x", "data": {}})
        assert (
            construct_webhook_event(body, _signed(body), TEST_HMAC_KEY, now=_now)["type"] == "firearm.renamed"
        )

    def test_rejects_non_event_body(self) -> None:
        body = "[1,2,3]"
        with pytest.raises(WebhookSignatureError, match="not an object"):
            construct_webhook_event(body, _signed(body), TEST_HMAC_KEY, now=_now)

    def test_never_parses_before_verifying(self) -> None:
        with pytest.raises(WebhookSignatureError, match="tolerance|match"):
            construct_webhook_event("{not json", "t=1,v1=00", TEST_HMAC_KEY, now=_now)


def test_webhook_headers() -> None:
    assert list(WEBHOOK_HEADERS.values()) == [
        "X-Webhook-Signature",
        "X-Webhook-Id",
        "X-Webhook-Event",
        "X-Webhook-Delivery",
    ]
