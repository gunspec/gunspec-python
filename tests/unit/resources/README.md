# tests/unit/resources

One test module per resource class, sync and async, over the MagicMock / AsyncMock transports from `tests/conftest.py`. Each test asserts the path, method and query the resource sends; nothing here parses a response.
