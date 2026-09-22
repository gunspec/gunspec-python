# gunspec

Source of the `gunspec` PyPI package. One `GunSpec` (and `AsyncGunSpec`) class exposes a resource object per API tag; every resource is a thin wrapper over the httpx transport in `_core/`.

Governed by: [`packages/sdk-python/README.md`](../../README.md).

| Path | Purpose |
|---|---|
| `_client.py` | `GunSpec` / `AsyncGunSpec` and their options; wires every resource to one transport |
| `__init__.py` | Public barrel |
| `_version.py` | `__version__`, bumped with `pyproject.toml` |
| `_core/` | Transport, auth, errors, retry, pagination, ETag cache, webhook verification |
| `_resources/` | One sync and one async class per API tag |
| `types/` | Models, parameters, and the two generated contract lists |

## Declaring the endpoint a method calls

The docs' SDK reference is generated: `scripts/sdk-python-reference.py` reads
these classes with `ast` and pairs each method with its TypeScript counterpart
through the endpoint it calls. A method whose path the parser cannot read is
dropped from that reference - and a dropped method is the docs telling a Python
reader it does not exist.

That is not hypothetical. Eleven methods were documented as missing from this
SDK while being in it: every firearm media call, `ammunition.get_bullet_svg`
and both vendor click helpers. Their paths are built from a helper
(`f"{_slug(id)}/media"`) or fetched through a transport verb the parser did not
model, so it read a fragment (`/media`) and matched nothing.

Two tags, in the docstring, mirroring the TypeScript SDK's TSDoc:

```python
def list_media(self, id: str) -> APIResponse[List[Dict[str, Any]]]:
    """Every asset on one firearm, with credit and derivative sizes.

    @endpoint GET /v1/firearms/{id}/media
    """
```

- **`@endpoint VERB /v1/...`** - the call this method makes, when the parser
  cannot read it from the source. A declared endpoint always wins over an
  inferred one: it is the contract, stated where a reader of the source looks.
- **`@sdk_only`** - the method makes no request at all.

Neither is optional in practice: the generator **fails the build** for a method
that resolves to no endpoint and declares nothing, the same rule the TypeScript
SDK has. A new method is documented, or CI stops.

The return annotation is load-bearing too. The generated sample prints
`response.data` for an `APIResponse`, the content type and length for a
`RawResponse`, and the value itself for a `str` - and the nightly verifier runs
every one of those samples against production, so a wrong annotation becomes a
failing example rather than a quiet mistake.
