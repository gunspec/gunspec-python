# gunspec

> This repository mirrors the SDK's source on every stable release. The package is built and published to PyPI from the GunSpec monorepo, and each release here is tagged with the version it matches. Issues are welcome here. A pull request is read and applied upstream by hand, then arrives with the next release.

Official Python SDK for the [GunSpec.io](https://gunspec.io) firearms specification database API. Sync and async clients over httpx, typed parameters, pydantic models, retries with backoff, conditional requests, and webhook verification. Python 3.9 or later.

## Installation

```bash
pip install gunspec
```

## Quick Start

```python
from gunspec import GunSpec

# Reads GUNSPEC_API_KEY from the environment
client = GunSpec()

# List firearms; data rows are dicts as the API returns them
result = client.firearms.list({"category": "pistol", "per_page": 5})
for firearm in result.data:
    print(firearm["id"], firearm["name"])

# Get a single firearm (Builder plan)
detail = client.firearms.get("glock-g19").data
print(detail["name"], detail["version"], detail["updatedAt"])
```

## Async Usage

<!-- smoke: skip -->
```python
from gunspec import AsyncGunSpec

async with AsyncGunSpec() as client:
    result = await client.firearms.list({"category": "rifle"})
    for firearm in result.data:
        print(firearm["name"])
```

## Configuration

```python
import os

from gunspec import GunSpec, RetryConfig

client = GunSpec(
    api_key=os.environ["GUNSPEC_API_KEY"],    # omitted reads GUNSPEC_API_KEY; None is anonymous on purpose
    auth_scheme="x-api-key",                   # or "bearer" for Authorization: Bearer
    base_url="https://api.gunspec.io",        # default; a key over plain http is refused unless allow_insecure=True
    timeout=30.0,                              # seconds
    retry=RetryConfig(
        max_retries=2,
        initial_delay_s=0.5,
        max_retry_after_s=30.0,                # a longer server wait is raised, not slept through
    ),
    etag_cache=True,                           # hold ETags; a 304 is served from cache and skips the daily cap
)
print(client.is_authenticated, repr(client))  # the key is masked in repr
```

An explicit `api_key=None` sends no credential and does not read the environment, which is how a test or a public-only caller opts out of a key the shell exports.

## Resources

Every method takes the matching `TypedDict` from `gunspec.types.params` (a plain dict works too) and returns `APIResponse[Dict[str, Any]]` or `PaginatedResponse[Dict[str, Any]]`: `.data`, `.status`, `.headers`, `.request_id`, `.rate_limit`, `.etag`, `.cache_control`, `.from_cache`, and `.pagination` (`page`, `limit`, `per_page`, `total`, `total_pages`) on lists.

| Resource | Methods |
|----------|---------|
| `client.firearms` | `list`, `get`, `search`, `compare`, `resolve`, `resolve_many`, `game_meta`, `action_types`, `filter_options`, `random`, `top`, `head_to_head`, `by_feature`, `by_action`, `by_material`, `by_designer`, `power_rating`, `timeline`, `by_conflict`, `get_variants`, `get_images`, `get_game_stats`, `get_dimensions`, `get_users`, `get_family_tree`, `get_similar`, `get_adoption_map`, `get_game_profile`, `get_silhouette`, `get_schematics`, `popular`, `calculate`, `load`, `media_catalog`, `list_media`, `get_media`, `download_media`, `get_image_asset`, `get_model`, `get_offers`, `get_interfaces`, `get_attachments`, `list_auto_paging` |
| `client.manufacturers` | `list`, `get`, `get_firearms`, `get_timeline`, `get_stats`, `list_auto_paging` |
| `client.calibers` | `list`, `get`, `compare`, `ballistics`, `get_firearms`, `get_parent_chain`, `get_family`, `get_ammunition`, `list_auto_paging` |
| `client.categories` | `list`, `get_firearms` |
| `client.stats` | `summary`, `production_status`, `field_coverage`, `catalog_coverage`, `popular_calibers`, `prolific_manufacturers`, `by_category`, `by_era`, `materials`, `adoption_by_country`, `adoption_by_type`, `action_types`, `feature_frequency`, `caliber_popularity_by_era` |
| `client.game` | `balance_report`, `tier_list`, `matchups`, `role_roster`, `stat_distribution` |
| `client.game_stats` | `list_versions`, `list_firearms`, `get_firearm` |
| `client.ammunition` | `list`, `get`, `get_bullet_svg` (text), `ballistics`, `list_auto_paging` |
| `client.countries` | `list`, `get_arsenal` |
| `client.conflicts` | `list` |
| `client.content` | `list_changelog`, `get_changelog_entry`, `list_blog_posts`, `get_blog_post`, `list_notices` (no key needed) |
| `client.collections` | `get_shared` |
| `client.attachments` | `list`, `get`, `get_firearms`, `get_offers`, `list_auto_paging` (fit computation is Studio) |
| `client.interfaces` | `list`, `get_firearms` |
| `client.platforms` | `list`, `get` (Studio) |
| `client.vendor` | `shops`, `list_offers`, `push_offers`, `update_offer`, `delete_offer`, `click_url`, `resolve_click` (Enterprise seller) |
| `client.data_quality` | `coverage`, `confidence` |
| `client.favorites` | `list`, `list_ids`, `add`, `remove` |
| `client.reports` | `create`, `list` |
| `client.support` | `create`, `list`, `get`, `reply` |
| `client.webhooks` | `list`, `create`, `get`, `update`, `delete`, `test` |
| `client.usage` | `get` |

`client.usage.get()` reports requests made through the hosted MCP server beside the account's totals: `mcp` on the usage stats carries this month's and today's MCP calls, the daily limit per key and the key nearest it, and each key carries `mcp_today`. MCP calls have their own daily ceiling inside the plan's, and a call past it raises with the reason `MCP_DAILY_CAP_EXCEEDED`.

`gunspec.types` also exports the firearm vocabularies `FIREARM_FIRING_MECHANISMS`, `FIREARM_TRIGGER_TYPES` and `FIREARM_MAGAZINE_TYPES`, each with a matching `Literal` (`FirearmFiringMechanism`, `FirearmTriggerType`, `FirearmMagazineType`), generated from the API source like every other vocabulary.

`client.http` is the transport (`get`, `get_paginated`, `get_text`, `get_bytes`, `request_conditional`, `resolve_redirect`, `url_for`) for endpoints the resources do not cover yet.

## Auto-Pagination

```python
from gunspec import GunSpec

client = GunSpec()
count = 0
for firearm in client.firearms.list_auto_paging({"category": "rifle", "per_page": 100}):
    count += 1
    if count >= 150:
        break
```

<!-- smoke: skip -->
```python
async for firearm in client.firearms.list_auto_paging({"category": "rifle"}):
    print(firearm["name"])
```

## Compatibility and sellers

```python
from gunspec import GunSpec

client = GunSpec()
firearm_id = client.firearms.list({"per_page": 1}).data[0]["id"]

# What fits a firearm (Studio), with the evidence for each fit
fits = client.firearms.get_attachments(firearm_id, {"with_offers": True}).data
for group in fits["groups"]:
    for item in group["items"]:
        print(group["category"], item["name"], item["fitType"], item["confidence"])

# Where to buy: link through the tracked click so the seller sees the visit
for offer in client.firearms.get_offers(firearm_id, {"region": "AU"}).data:
    href = client.vendor.click_url(offer["clickId"]) if offer["clickId"] else offer["url"]

# The mount vocabulary the fit engine reasons over
standards = client.interfaces.list({"kind": "thread"}).data
```

<!-- smoke: skip -->
```python
# Seller side (an Enterprise key named by a shop): read before you write
shops = client.vendor.shops().data
client.vendor.push_offers({"offers": [
    {"sku": "A1", "firearm_id": "ak-74m", "price_cents": 129900, "currency": "AUD", "url": "https://shop.example/a1"},
]})
client.vendor.update_offer("A1", {"price_cents": 119900, "status": "published"})
client.vendor.delete_offer("A1")
```

### Provenance

A firearm detail, a caliber and an attachment detail carry `provenance`: the pages consulted (`sources`), the 0 to 1 `dataConfidence` set from what was actually sourced, `verifiedAt` and `verifiedFields` for the last check against a maker's page (null means seed knowledge nobody has checked), and the same `updatedAt` and `version` the record carries at the top level. Check a specific figure against `sources`, not against the score. `gunspec.types.Provenance` parses it.

```python
detail = client.firearms.get(firearm_id).data
if detail["provenance"]["verifiedAt"] is None:
    print("unverified; sources:", detail["provenance"]["sources"])
```

### Evidence on fits

Every fit item (`firearms.get_attachments`, `attachments.get_firearms`) carries `source`, the weakest evidence behind it: `curated` is a person's verdict, `universal` needs no interface at all, and `inferred`, `inherited:parent` or `inherited:platform` name the least trustworthy interface row the fit passed through. Treat `inferred` as unverified; `min_confidence` hides it. `gunspec.types.FIT_SOURCES` lists the values, and every other closed vocabulary the API serves (`FIREARM_STATUSES`, `MEDIA_KINDS`, `TICKET_STATUSES` ...) is exported the same way with a matching `Literal` (`FitSource`, `FirearmStatus` ...), generated from the API source. The pydantic models use those Literals, and `tests/unit/test_types_mirror.py` checks every model's field names against the API's OpenAPI document.

## Error Handling

Every `APIError` carries `code` (the family, never renamed) and `reason` (the specific situation, what to branch on), plus `details`, `retry_after`, `request_id` and `action`, the API's own one-line advice. `str(err)` reads `NotFoundError(404 RESOURCE_NOT_FOUND): Firearm 'x' not found [request_id=...]`; `repr` and `to_dict()` never include headers or the key.

```python
from gunspec import (
    APIError,
    AuthenticationError,
    GunSpec,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

client = GunSpec()

try:
    client.firearms.get("no-such-firearm-xyz")
except NotFoundError as e:
    print(e)                      # NotFoundError(404 RESOURCE_NOT_FOUND): ... [request_id=...]
    print(e.action)               # "Check the id. The list and search endpoints return valid ones."
except RateLimitError as e:
    if e.is_daily_cap:
        print("Daily allowance spent; resets at midnight UTC")
    else:
        print(f"Retry after: {e.retry_after}s")
except PermissionDeniedError as e:
    if e.reason == "PLAN_REQUIRED":
        print(f"Needs the {e.required_tier} plan")
except AuthenticationError as e:
    print(e.reason, e.action)     # e.g. KEY_EXPIRED, "Create a new key in your account."
except APIError as e:
    log_line = e.to_dict()        # JSON-serialisable, no headers, no key
```

`ConflictError` (409), `PayloadTooLargeError` (413, `max_bytes`) and `ServiceUnavailableError` (503, `retry_after`) cover those statuses; `ConfigurationError`, `ConnectError`, `RequestTimeoutError` and `WebhookSignatureError` share the same `GunSpecError` root. A spent daily cap is never retried; a `Retry-After` longer than `max_retry_after_s` is raised rather than slept through.

## Conditional requests

```python
from gunspec import GunSpec

client = GunSpec(etag_cache=True)
firearm_id = client.firearms.list({"per_page": 1}).data[0]["id"]

first = client.firearms.get(firearm_id)      # 200, stored with its ETag
second = client.firearms.get(firearm_id)     # 304 from the API, body from the cache
assert second.from_cache and second.data == first.data

# Holding your own tag
res = client.http.request_conditional(f"/v1/firearms/{firearm_id}", if_none_match=first.etag or "")
if res.not_modified:
    pass
```

Pass a `MemoryETagStore(max_entries)` or your own `ETagStore` to `etag_cache` to size or persist it. Cache keys are namespaced by a fingerprint of the key, so a shared store never hands a paid-tier body to a cheaper key.

## Verifying webhooks

<!-- smoke: skip -->
```python
import os

from gunspec import WebhookSignatureError, construct_webhook_event

@app.post("/hooks/gunspec")
def hook(request):
    try:
        event = construct_webhook_event(
            request.get_data(),                       # the raw body, before parsing
            request.headers.get("X-Webhook-Signature"),
            os.environ["GUNSPEC_WEBHOOK_SECRET"],
        )
    except WebhookSignatureError:
        return "", 400
    if event["type"] == "firearm.updated":
        mirror.upsert(event["data"])
    return "", 204
```

Signatures are HMAC-SHA256 over `f"{t}.{body}"` and compared in constant time; deliveries older than `tolerance_seconds` (300) are refused. Dedupe on `X-Webhook-Id`; `WEBHOOK_EVENT_TYPES` lists every event. See `examples/webhooks.py` for a complete receiver.

## Context Managers

```python
from gunspec import GunSpec

with GunSpec() as client:
    result = client.firearms.list({"per_page": 1})
```

<!-- smoke: skip -->
```python
async with AsyncGunSpec() as client:
    result = await client.firearms.list()
```

## Requirements

- Python >= 3.9 (the unit suite runs on 3.9; model fields use `Optional[...]` so pydantic can build them there)
- httpx >= 0.25
- pydantic >= 2

## Development

```bash
cd packages/sdk-python
uv sync --extra dev

uv run pytest tests/unit                       # unit, no network
uv run mypy --strict src                       # type check
uv run ruff check src tests scripts examples   # lint
uv run ruff format --check                     # formatting
uv run python scripts/sync_api_contracts.py    # regenerate error reasons and webhook events from the API source

# Against the local API (see tests/integration/README.md)
GUNSPEC_INTEGRATION_BASE_URL=http://localhost:8788 GUNSPEC_INTEGRATION_API_KEY=... uv run pytest tests/integration
GUNSPEC_INTEGRATION_BASE_URL=http://localhost:8788 GUNSPEC_INTEGRATION_API_KEY=... uv run python scripts/smoke_readme.py
```

`__version__` comes from the installed package metadata, so `pyproject.toml` is the only place the version lives (`uv version 0.2.0b1` for a prerelease).

## Publishing

```bash
cd packages/sdk-python
uv build                      # sdist and wheel in dist/, LICENSE and CHANGELOG.md included
uv publish                    # PyPI; UV_PUBLISH_TOKEN in the environment
```

## License

MIT
