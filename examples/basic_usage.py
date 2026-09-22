"""Basic usage of the gunspec SDK.

Run with ``GUNSPEC_API_KEY`` set (a Builder key or above for firearm detail).
Point ``GUNSPEC_BASE_URL`` at a local worker to try it without touching
production.
"""

from __future__ import annotations

import os
import sys

from gunspec import GunSpec, NotFoundError, RateLimitError


def main() -> int:
    out = sys.stdout.write
    client = GunSpec(base_url=os.environ.get("GUNSPEC_BASE_URL"), etag_cache=True)

    # List with filters; pagination is echoed back in both vocabularies.
    pistols = client.firearms.list({"category": "pistol", "sort": "name", "per_page": 5})
    out(f"{pistols.pagination.total} pistols, showing {len(pistols.data)}\n")
    for firearm in pistols.data:
        out(f"  {firearm['id']}: {firearm['name']}\n")

    # Resolve a loose name to one record, then fetch it.
    resolved = client.firearms.resolve("Glock 19").data
    if resolved["firearmId"]:
        detail = client.firearms.get(resolved["firearmId"]).data
        out(f"{detail['name']} version={detail['version']} updated={detail['updatedAt']}\n")

        # The second read is answered 304 and served from the ETag cache.
        again = client.firearms.get(resolved["firearmId"])
        out(f"from_cache={again.from_cache} status={again.status}\n")

    # Reference data.
    summary = client.stats.summary().data
    out(f"catalog summary keys: {sorted(summary)}\n")

    # Errors carry a reason to branch on and the API's advice.
    try:
        client.firearms.get("no-such-firearm-xyz")
    except NotFoundError as err:
        out(f"{err}\n  -> {err.action}\n")
    except RateLimitError as err:
        out(f"slow down: {err.reason}, retry after {err.retry_after}s\n")

    client.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
