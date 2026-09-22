# gunspec/types

Every public type: pydantic models the API returns, TypedDict parameters the endpoints take, and the two contract lists the API publishes and clients branch on.

Governed by: [`packages/sdk-python/README.md`](../../../README.md).

| File | Purpose |
|---|---|
| `models/` | Catalog, statistics, game, account, content and provenance models (see its README) |
| `params/` | Query and body parameter TypedDicts, mirroring `apps/api/src/schemas/` (see its README) |
| `compat/` | Attachment compatibility: standards, platforms, interfaces, fits, public offers (see its README) |
| `seller.py` | Vendor shops and the seller's own offer rows and inputs |
| `media.py` | Media assets, the media catalog, name resolution results, site notices |
| `errors.py` | The error envelope shape |
| `error_reasons.py` | **Generated.** `ErrorReason` Literal and the API's summary and action for each |
| `webhook_events.py` | **Generated.** `WEBHOOK_EVENT_TYPES` and its Literal |
| `vocabulary.py` | **Generated.** Every closed vocabulary (`FIREARM_STATUSES`, `FIT_SOURCES` ...) as a tuple and a Literal; the models use the Literals |

Generated files come from `scripts/sync_api_contracts.py`; edit the API source, rerun it, commit both. `tests/unit/test_contracts.py` fails when a copy is stale.

Every model mirrors the API's OpenAPI schema for the same response: `tests/unit/test_types_mirror.py` reads `apps/api/openapi.json` and fails when a schema property has no field on the model (by alias) or a Literal field disagrees with the schema's enum. Enumerated fields use the `vocabulary.py` Literals, never an inline `Literal[...]`, so a value the API adds reaches every model in one regeneration.
