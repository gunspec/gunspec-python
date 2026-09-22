# gunspec/_core/_http

The httpx transport, split so each file has one job. `gunspec._core._http_client` re-exports this package for older imports.

| File | Purpose |
|---|---|
| `base.py` | `HttpClientConfig`, `serialize_query`, and `_BaseHttpClient`: key resolution, transport-security check, default headers, ETag cache lookup and store, request assembly, masking `__repr__` |
| `sync.py` | `SyncHttpClient` over `httpx.Client`: request, paginated, conditional, raw, redirect resolution, the verb helpers |
| `async_.py` | `AsyncHttpClient`, the same surface over `httpx.AsyncClient` |
| `__init__.py` | Barrel |
