# OpenAPI generation

The typed client is generated from BSM's FastAPI OpenAPI document while
`bsm_api_client.dynamic` provides forward compatibility for endpoints added
after a client release.

## Regenerate

Install development dependencies. For the release client, export the schema from
the pinned BSM beta in an isolated environment and generate from it:

```bash
python tools/export_bsm_openapi.py --output openapi.json
python tools/generate_client.py openapi.json
```

For development against a running BSM instance (including its loaded plugins),
you can also generate directly from the live schema:

```bash
python tools/generate_client.py http://localhost:11325/api/openapi.json
```

A saved schema can be used instead:

```bash
python tools/generate_client.py openapi.json
```

The generated package is written to
`packages/bsm-api-client/src/bsm_api_client/generated`.

For release builds, generate against a clean BSM installation so third-party
plugin endpoints are not baked into the core typed package. Plugin endpoints
remain available at runtime through `async_discover_api()` and
`async_call_operation()`.
