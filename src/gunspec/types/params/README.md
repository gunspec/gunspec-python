# gunspec/types/params

Request parameter TypedDicts, split by domain to mirror `packages/sdk/src/types/params/`. `__init__.py` re-exports everything, so `from gunspec.types.params import X` keeps working.

Governed by: [`../README.md`](../README.md).

| File | Purpose |
|---|---|
| `shared.py` | `PaginationParams` |
| `firearm.py` | list, search, compare, discovery and per-firearm endpoints |
| `firearm_analysis.py` | silhouette |
| `catalog.py` | manufacturers, calibers, countries, conflicts |
| `ammunition.py` | ammunition list and ballistics |
| `game.py` | game endpoints and snapshots |
| `stats.py` | statistics and data quality |
| `content.py` | changelog and blog |
| `account.py` | favorites, reports, support, webhooks, usage |
