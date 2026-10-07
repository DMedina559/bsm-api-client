# Generated REST client

BSM's installed FastAPI application is the source of truth. This branch targets
BSM `dev` at `c9eea1c14cc4ef2ff0d01ead801ec691edb7552d`, which supplies explicit
operation IDs such as `start_server`, `list_servers`, and `create_backup`.
Both development extras and the release workflow pin that revision. Update the
pins together when adopting another BSM revision.

## Regeneration

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e './packages/bsm-api-client[dev]' -e './packages/bsm-cli[dev]'
python tools/export_bsm_openapi.py --output openapi.json
python tools/generate_client.py openapi.json
python -m pytest
```

Export creates an isolated BSM configuration/database and loads plugin routers
before calling `app.openapi()`. The release export uses an empty plugin directory.
Generation uses `openapi-python-client >=0.29.1,<0.30`, checks that every operation
was generated, and writes a module registry plus the exact input schema into
`bsm_api_client.generated`. Wheel and source-distribution builds include both JSON
files. Generated files are ignored by Git and must never be edited by hand.

For a development instance with plugins, an explicit live schema can also be used:

```bash
python tools/generate_client.py http://localhost:11325/api/openapi.json
```

Runtime discovery only interprets metadata. It never generates, imports, or runs
Python from a remotely fetched schema. Code generation remains an explicit build
step using the patched generator.

## Public surfaces

- `bsm_api_client.generated`: disposable generated endpoint modules and models.
- `BedrockServerManagerApi`: stable facade, compatibility models, and shared
  authentication, retries, timeouts, SSL/session ownership, and API exceptions.
- `ApiOperation`: parameters, bodies, responses, security, tags, plugin ownership,
  deprecation, and generated/runtime status shared by Python and the CLI.
- `async_call_generated(operation_id, parameters=..., body=..., detailed=True)`:
  generated serialization and typed parsed responses through the shared transport.
- `async_discover_api()` / `async_call_operation()`: added core and plugin routes.

Every facade REST adapter calls a generated operation by ID, including login,
logout, images, and DELETE operations. Generated requests use the facade's existing
HTTP session and auth refresh lock. `async_get_generated_client()` also uses that
transport; close it through the facade's `close()` or async context manager.
Directly constructing a generated client remains a low-level option with the
generator's native HTTPX lifecycle/error behavior.

```python
async with BedrockServerManagerApi(url, username="admin", password="...") as client:
    await client.async_discover_api()
    if client.capabilities.has("start_server"):
        await client.async_start_server("survival")
    print(client.capabilities.plugins)
    print(client.capabilities.runtime_only)
    print(client.api_diff())
    detailed = await client.async_call_generated(
        "start_server", parameters={"server_name": "survival"}, detailed=True
    )
    print(detailed.parsed)
```

Diffs report added, removed, changed, and generated operations. Changes include
transitively referenced request/response models and authentication schemes.
Discovery is cached per client; force a refresh after plugin reloads.

BSM dev currently has no content-upload route. `async_upload_content()` requires
an advertised `upload_content` operation; otherwise it raises `NotFoundError`.
Use `async_call_operation(..., files={"file": ("name.txt", data, "text/plain")})`
for any advertised multipart operation. WebSockets remain separately managed.
