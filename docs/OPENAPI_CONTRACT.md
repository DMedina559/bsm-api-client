# BSM OpenAPI contract

The server owns operation IDs, tags, URLs, security declarations, and schemas.
Clients preserve them rather than renaming the contract during generation.
The BSM dev revision targeted by this client already sets explicit operation IDs.

## Server and plugin conventions

| Metadata | Convention |
| --- | --- |
| `operationId` | Explicit, unique, stable machine identifier; keep it when a route moves. Core examples: `start_server`, `list_servers`. Plugin example: `discord_status`. |
| `tags` | Stable feature tags shared across clients. Prefer consistent names such as `Server Management`, `Backup & Restore`, `World Management`, `Addon Management`, `User Management`, and `Plugin:<name>`. |
| `summary` / `description` | Describe the action and required preconditions. |
| `parameters` | Declare locations, types, required flags, defaults, and serialization. |
| `requestBody` | Typed JSON/form/multipart body and supported content types. |
| `responses` | Typed successful responses plus documented validation, authentication, missing-resource, and server errors. |
| `security` | Declare auth requirements; use an explicit empty list for public operations. |
| `deprecated` | Advertise migrations before removing an operation. |
| `x-bsm-plugin` | Plugin ownership at the operation or path-item level; takes precedence over tags/path inference. |

```python
router.get(
    "/api/plugin/discord/status",
    operation_id="discord_status",
    tags=["Plugin:discord"],
    summary="Read Discord integration status",
    response_model=DiscordStatus,
    openapi_extra={"x-bsm-plugin": "discord"},
)(status_handler)
```

Plugin routes must be registered before OpenAPI is generated. If a running server
adds/removes routers later, clear its cached `app.openapi_schema` before generating
the next schema; refreshing a client cannot repair a stale server schema.
Schema-hidden routes and WebSockets require an explicit separate contract.

## Client guarantees

Discovery rejects duplicate operation IDs instead of silently losing endpoints.
Path-level parameters and local component references are resolved for inspection.
Explicit plugin ownership wins; `Plugin:`/`plugin.` tags and plugin URL prefixes
are backward-compatible fallbacks. Core plugin-management endpoints are excluded
from plugin ownership inference.

`client.capabilities.has(id)` matches exact operation IDs. `client.plugins` groups
operations by ownership. Runtime-only operations are callable without rebuilding;
they gain generated typed modules only after a deliberate regeneration.
The CLI exposes generic calls under `api call` and `plugin call`; curated commands
remain stable. No remote schema is executed as Python.

Tags in the pinned schema are preserved, including existing upstream spelling.
Tag normalization, additional error schemas, and plugin metadata adoption are
server-side contract changes; this client consumes them when the server publishes
them. Consumers should use stable operation IDs instead of hard-coding generated
module locations, which depend on tags.
