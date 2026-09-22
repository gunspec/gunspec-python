# Changelog

All notable changes to the `gunspec` Python package. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the package follows [Semantic Versioning](https://semver.org/).

## [0.7.0](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/compare/sdk-py-v0.6.0...sdk-py-v0.7.0) (2026-09-22)


### Added

* build apps/site, serve ten fields as arrays, enforce the craft rules ([bcec6f3](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/bcec6f30fbb04ff4d017a3021f776472b0c74e5a))
* give the MCP the docs, report the daily allowance, retire three web pages ([a5638f8](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/a5638f8281e702b0418f07a21e238f7af1294b2e))
* publish dated updates, and give the reasoning a page of its own ([e7f1e80](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/e7f1e80ddbb32a82b47cddfcb14448b9bfa5deba))

## [0.6.0](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/compare/sdk-py-v0.5.0...sdk-py-v0.6.0) (2026-09-17)


### Added

* serve the API reference to code at /v1/docs ([febef92](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/febef920fa472dfc1071918e40694e510e1e57fe))


### Fixed

* document GET /v1/data/tasks/summary, and test the docs resources in both SDKs ([e17812f](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/e17812ff4db2dae84a76dda638fb7238c8f83af5))
* require an Explorer key for /v1/docs ([bccd31b](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/bccd31b4680c216e7bc8dce8975a053f2aee8abb))

## [0.5.0](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/compare/sdk-py-v0.4.0...sdk-py-v0.5.0) (2026-09-17)


### Added

* **sdk:** workflow tools, MCP usage and manufacturer status in both SDKs ([eefc1c2](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/eefc1c2e966ee3392feccd75ef9d26d4451fab60))

## [0.4.0](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/compare/sdk-py-v0.3.0...sdk-py-v0.4.0) (2026-09-13)


### Added

* publish whether the reference is still true, and run the cURL samples ([7803ed0](https://github.com/BuunGroupCore/gunspec-vite-v6-cloudflare/commit/7803ed0b76eab49d8a1d7abd7a5ca60cd1d67896))

## [0.3.0] - 2026-09-13

### Changed

- **`FavoriteFirearm` was corrected to what `GET /v1/me/favorites` actually returns.** It carried `firearm_id` and `created_at`; the endpoint has never sent `created_at`. The model is now the firearm record the endpoint answers under its own column names: `id`, `firearm_id`, `favorited_at`, `name`, `manufacturer_id`, `manufacturer_name`, `category_id`, `category_name`, `status`, `year_introduced`, `action_type`, `country_of_origin`, `svg_line_art_url`, `model_3d_url`, `favorite_count`, `images`. A breaking change to the model rather than to the payload: the bytes are unchanged, so only the attribute names you read need updating. Running the documented examples against the live API is what surfaced it.

### Fixed

- `IMAGE_TYPES` gains the labels the API actually stores: `gallery`, `primary`, `thumbnail`, `render`, `profile`, `angle` and `detail`. `gallery` is the default an upload lands on, and its absence made a correct value fail validation.

## [0.2.2] - 2026-09-12

### Added
- `source_kinds` (a list of `SourceCitation`: `url`, `kind`) and `best_source_kind` on `Provenance`, with the `SourceKind` Literal and `SOURCE_KINDS` tuple (strongest first: `manufacturer`, `standards_body`, `government`, `reference`, `aggregator`, `press`, `retailer`, `community`, `other`). Each cited page is classed on the API's source hierarchy; weigh a figure by `best_source_kind`, never by `len(sources)`.

## [0.2.1] - 2026-09-12

### Added
- `provenance` on `Firearm` (detail), `Caliber` and `AttachmentDetail`, with the `Provenance` model: `sources`, `data_confidence`, `verified_at`, `verified_fields`, `spec_source`, `updated_at`, `version`.
- `source: Optional[FitSource]` on `AttachmentFit` and `AttachmentFirearmFit`: the weakest evidence behind a fit (`curated`, `universal`, `inferred`, `inherited:parent`, `inherited:platform`).
- Every closed vocabulary the API serves, generated from the API source into `gunspec.types.vocabulary`: `FIREARM_STATUSES`, `FIREARM_ACTION_TYPES`, `ATTACHMENT_STATUSES`, `MEDIA_KINDS`, `IMAGE_TYPES`, `SCHEMATIC_TYPES`, `TICKET_STATUSES`, `TICKET_PRIORITIES`, `TICKET_CATEGORIES`, `REPORT_ISSUE_TYPES`, `REPORT_STATUSES`, `INTERFACE_SOURCES`, `FIT_TYPES`, `FIT_SOURCES`, `GAME_ARCHETYPES`, `CHANGELOG_CATEGORIES`, `NOTICE_VARIANTS`, `OFFER_STATUSES`, `OFFER_TARGET_KINDS`, `ADOPTION_TYPES`, each a tuple beside a `Literal` of the same name (`FirearmStatus`, `FitSource` ...). The models use the Literals.
- Models for shapes that were `Dict[str, Any]`: `AttachmentDetail`, `StandardRef`, `CaliberRating`, `FirearmAttachments`, `FirearmAttachmentsGroup`, `AttachmentFirearmFit`, `InterfaceFirearm`, `PlatformInterface`, `OfferVendor`, `UnmatchedOffer`, `InlineMediaItem`, `ResolveManyResult`, `FirearmSchematic`, `WebhookEndpointCreated`.
- Caliber geometry: `shoulder_diameter_mm`, `rim_diameter_mm`, `rim_thickness_mm`, `bullet_length_mm`, `case_shape`, `case_material`, `projectile_kind`, `bullet_profile`, `closure`, `marking_color`, `marking_meaning`, `spec_source`, `spec_standard`, `data_confidence`, `verified_at`, `verified_fields`, `version` on `Caliber` (with `CaseShape`, `CaseMaterial`, `ProjectileKind`, `BulletProfile`, `Closure`, `MarkingColor`, `SpecStandard` Literals), and the drawing fields on `FirearmCaliberEntry`.
- `version` on `Firearm`, `FirearmListItem` and `Manufacturer`; `updated_at` and `images` on `FirearmListItem`; `schematics` on `FirearmDetail`; `kind`, `storage`, `author`, `source_url`, `alt`, `width`, `height`, `sort_order` on `FirearmImage`.
- `tests/unit/test_types_mirror.py`: every property on the API's OpenAPI schema for a response exists on the corresponding pydantic model, and every Literal-typed field matches the schema's enum.

### Fixed
Model corrections where a field disagreed with the API, found by the mirror test. None changes what the API sends.
- `Firearm.status`, `FirearmListItem.status`, `FirearmVariant.status` are `FirearmStatus` (`out_of_production`, `in_service`, `limited_production` were not listed anywhere).
- `Firearm.has_3d_model` is an `int`, never None.
- `FirearmImage.type` is `ImageType`; `FitVia.source` and `FirearmInterface.source` are `InterfaceSource`; `PlatformDetail.interfaces` is typed.
- `WebhookEndpoint` no longer requires `secret` (only `WebhookEndpointCreated` carries it); `WebhookTestResult` is `delivered`, `http_status`, `error`.
- `SupportTicket` gained `reply_count` and `closed_at`, `description` is optional on list rows, `priority` and `status` are Literals; `SupportTicketReply` dropped `is_staff`, which the API never sent.
- `DataReport` carries `reviewed_at` rather than `updated_at`; `issue_type` and `status` are Literals; `references` defaults to an empty list.
- `SiteNotice.variant` is `NoticeVariant`; `FirearmMedia.kind` is `MediaKind`; `VendorOffer.target_kind` and `status` are `OfferTargetKind` and `OfferStatus`, `source` defaults to `feed`.

## [0.2.0] - 2026-09-11

### Added
- Resources: `attachments`, `interfaces`, `platforms`, `vendor`; `firearms.resolve`, `resolve_many`, `media_catalog`, `list_media`, `get_media`, `download_media`, `get_image_asset`, `get_model`, `get_offers`, `get_interfaces`, `get_attachments`; `content.list_notices`. Sync and async.
- Errors carry `reason`, `details`, `retry_after` and `action`, stringify as `Name(status REASON): message [request_id=...]` and serialise with `to_dict()`; new `ConflictError` (409), `PayloadTooLargeError` (413, `max_bytes`), `ServiceUnavailableError` (503), `ConfigurationError`; `PermissionDeniedError.required_tier`, `RateLimitError.is_daily_cap`.
- `ERROR_REASONS` and `WEBHOOK_EVENT_TYPES`, generated from the API source by `scripts/sync_api_contracts.py`.
- `etag_cache` option: conditional requests with `If-None-Match`, a 304 served from the held body with `from_cache=True`; `ETagStore` and `MemoryETagStore`; `etag` and `cache_control` on every response; `request_conditional` on both transports.
- `auth_scheme="bearer"`; an explicit `api_key=None` for anonymous use (the environment is not read); `allow_insecure`.
- Transport: `request_raw`, `get_text`, `get_bytes` (follows the CDN redirect), `resolve_redirect`, `url_for`, `patch`, `is_authenticated`; `GunSpec.http` for endpoints the resources do not cover.
- Webhook verification: `verify_webhook_signature`, `construct_webhook_event`, `sign_webhook_payload`, `parse_signature_header`, `WEBHOOK_HEADERS`.
- Typed surface: every resource method takes the matching `TypedDict` from `gunspec.types.params` and returns `APIResponse[Dict[str, Any]]` / `PaginatedResponse[Dict[str, Any]]`; the package passes `mypy --strict`.
- `types.models` and `types.params` split into domain packages; `_core._http` package (base, sync, async).
- Integration suite against a live API (`tests/integration`), a README smoke runner (`scripts/smoke_readme.py`), and `examples/`.
- `LICENSE` and this changelog ship in the sdist and wheel; `__version__` is read from package metadata so `pyproject.toml` is the only place the version lives.

### Changed
- Retries honour `Retry-After` on 429 and 503, never retry a spent daily cap, and refuse to sleep past `RetryConfig.max_retry_after_s` (default 30 s).
- A key is refused over plain `http://` to any host but localhost; `repr(client)` masks the key.
- `PaginatedResponse` gained `per_page` and optional `meta`.
- Pydantic model fields use `Optional[...]` rather than `X | None`, so the models build on Python 3.9.

### Fixed
- Endpoints whose body is a list (`get_variants`, `get_similar`, `get_offers`, `interfaces.list`, `vendor.shops`, the statistics lists ...) are annotated `APIResponse[List[Dict[str, Any]]]` so a type checker sees the list.
- `ammunition.get_bullet_svg` parsed an SVG as JSON and returned nothing.
- `favorites.list_ids` is documented as returning `{"ids": [...]}`; `FavoriteIds` model added.
- A caller-supplied empty `MemoryETagStore` was treated as "no cache" because the store is falsy when empty.

## [0.1.0] - 2026-08-22

Initial release: firearms, manufacturers, calibers, categories, stats, game, game stats, ammunition, countries, conflicts, content, collections, data quality, favorites, reports, support, webhooks, usage; sync and async clients; retry with backoff; auto-pagination.
