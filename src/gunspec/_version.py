"""Package version, read from the installed metadata.

``pyproject.toml`` is the single source of truth: ``uv version 0.2.0b12`` sets a
prerelease without touching a second file. A source checkout that is not
installed reports ``0.0.0+unknown``.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("gunspec")
except PackageNotFoundError:  # pragma: no cover - only in an uninstalled checkout
    __version__ = "0.0.0+unknown"
