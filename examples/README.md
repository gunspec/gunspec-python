# sdk-python/examples

Runnable scripts, mirroring `packages/sdk/examples`. Each reads its key from the environment; none has a web-framework dependency.

| File | Shows |
|---|---|
| `basic_usage.py` | List with filters, resolve a name, fetch a record, the ETag cache answering 304, an error's `reason` and `action` |
| `webhooks.py` | A WSGI receiver that verifies `X-Webhook-Signature` with `construct_webhook_event` and dedupes on the event id |

```bash
GUNSPEC_API_KEY=... uv run python examples/basic_usage.py
GUNSPEC_WEBHOOK_SECRET=... uv run python examples/webhooks.py
```
