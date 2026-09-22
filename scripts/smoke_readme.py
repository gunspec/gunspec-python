#!/usr/bin/env python3
"""Execute the README's Python code blocks against a live API.

A README snippet that no longer runs is a support ticket, so this runs each
``python`` fenced block in ``README.md`` with the SDK imported and the client
pointed at ``GUNSPEC_INTEGRATION_BASE_URL`` with ``GUNSPEC_INTEGRATION_API_KEY``.
Blocks marked ``<!-- smoke: skip -->`` on the line before the fence are shown
but not run (a web-framework handler, an async snippet needing an event loop).

    GUNSPEC_INTEGRATION_BASE_URL=http://localhost:8788 \\
    GUNSPEC_INTEGRATION_API_KEY=... python scripts/smoke_readme.py

Exit 1 on the first block that raises, with the block and the traceback.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple

README = Path(__file__).resolve().parents[1] / "README.md"
FENCE = re.compile(r"^(<!-- smoke: (\w+) -->\n)?```python\n(.*?)^```", re.M | re.S)


def blocks(text: str) -> List[Tuple[int, str, str]]:
    """``(line_number, mode, code)`` for every python fence, in order."""
    out = []
    for m in FENCE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        out.append((line, m.group(2) or "run", m.group(3)))
    return out


def prepare(code: str, base_url: str, api_key: str) -> str:
    """Rewrite the snippet so it targets the test API rather than production."""
    code = code.replace('base_url="https://api.gunspec.io"', f'base_url="{base_url}"')
    code = re.sub(r'api_key="gs_[^"]*"', 'api_key=os.environ["GUNSPEC_INTEGRATION_API_KEY"]', code)
    code = code.replace('os.environ["GUNSPEC_API_KEY"]', 'os.environ["GUNSPEC_INTEGRATION_API_KEY"]')
    # Bare constructors read GUNSPEC_API_KEY; the smoke exports it below and
    # supplies base_url through a wrapped class so production is never called.
    return code


def main() -> int:
    base_url = os.environ.get("GUNSPEC_INTEGRATION_BASE_URL")
    api_key = os.environ.get("GUNSPEC_INTEGRATION_API_KEY")
    if not base_url or not api_key:
        sys.stderr.write("set GUNSPEC_INTEGRATION_BASE_URL and GUNSPEC_INTEGRATION_API_KEY\n")
        return 2

    os.environ["GUNSPEC_API_KEY"] = api_key
    import gunspec

    real_sync, real_async = gunspec.GunSpec, gunspec.AsyncGunSpec

    class SmokeGunSpec(real_sync):  # type: ignore[misc,valid-type]
        def __init__(self, **kw: Any) -> None:
            kw.setdefault("base_url", base_url)
            super().__init__(**kw)

    class SmokeAsyncGunSpec(real_async):  # type: ignore[misc,valid-type]
        def __init__(self, **kw: Any) -> None:
            kw.setdefault("base_url", base_url)
            super().__init__(**kw)

    gunspec.GunSpec = SmokeGunSpec  # type: ignore[misc]
    gunspec.AsyncGunSpec = SmokeAsyncGunSpec  # type: ignore[misc]

    text = README.read_text()
    ran = skipped = 0
    for line, mode, code in blocks(text):
        if mode != "run":
            skipped += 1
            continue
        namespace: Dict[str, Any] = {"__name__": "readme_smoke", "os": os, "asyncio": asyncio}
        try:
            exec(compile(prepare(code, base_url, api_key), f"README.md:{line}", "exec"), namespace)  # noqa: S102
        except Exception:
            sys.stderr.write(f"\nREADME.md block at line {line} failed:\n\n{code}\n")
            traceback.print_exc()
            return 1
        ran += 1
    sys.stdout.write(f"README smoke: {ran} block(s) ran, {skipped} skipped\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
