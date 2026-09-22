# gunspec/types/models

Pydantic response models, split by domain to mirror `packages/sdk/src/types/models/`. `__init__.py` re-exports everything, so `from gunspec.types.models import X` keeps working.

Governed by: [`../README.md`](../README.md).

| File | Purpose |
|---|---|
| `shared.py` | `_MODEL_CONFIG` (frozen, camelCase aliases) and the generic envelope wrappers |
| `firearm.py` | `Firearm`, list items, images, adopters |
| `firearm_analysis.py` | comparisons, head-to-head, family tree, similar, adoption map, top, power rating, timeline, dimensions, filter options, silhouette |
| `catalog.py` | manufacturers, calibers, categories, countries, conflicts |
| `caliber_geometry.py` | the cartridge-drawing Literals (`CaseShape`, `CaseMaterial`, `ProjectileKind`, `BulletProfile`, `Closure`, `MarkingColor`, `SpecStandard`) |
| `ammunition.py` | ammunition loads and ballistics results |
| `game.py` | game stats, game endpoints, snapshots, balance report, role roster |
| `stats.py` | statistics and data-quality aggregates |
| `account.py` | favorites, reports, support, webhooks, usage |
| `provenance.py` | `Provenance`: sources, confidence and verification state on a firearm, caliber or attachment detail |
