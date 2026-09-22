"""The one way a caller's value becomes a segment of a request path."""

from __future__ import annotations

from typing import Union
from urllib.parse import quote

_DOT_SEGMENTS = frozenset({"", ".", ".."})


def _seg(value: Union[str, int]) -> str:
    """Percent-encode ``value`` as a single path segment.

    ``quote(..., safe="")`` already encodes ``/``, but it leaves dots alone, and
    httpx resolves ``.`` and ``..`` like any URL: ``firearms.get_variants("..")``
    would request ``/v1/variants`` and ``webhooks.test("..")`` would become
    ``POST /v1/me/test``. An empty value collapses the segment the same way.
    None of the three is an id, so they are refused before a request is made.

    Raises:
        ValueError: ``value`` is empty, ``.`` or ``..``.
    """
    text = str(value)
    if text in _DOT_SEGMENTS:
        raise ValueError(f"{text!r} is not a valid id: it would change the request path")
    return quote(text, safe="")
