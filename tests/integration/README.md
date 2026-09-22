# tests/integration

Runs the SDK against a live API. Skipped unless both environment variables are set:

```bash
GUNSPEC_INTEGRATION_BASE_URL=http://localhost:8788 \
GUNSPEC_INTEGRATION_API_KEY=<dev key> \
uv run pytest tests/integration
```

The local worker (`pnpm dev:api`) with the dev enterprise key seeded (`pnpm --filter @gunspec/api db:seed:dev-key`) is the target. Assertions are on the shapes the SDK promises, never on catalog figures.
