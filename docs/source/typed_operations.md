# Typed operations and models

`client.rest` exposes generated operation-ID methods. Domain services add workflows, such as `client.diagnostics`. Both share authentication and HTTP transport. The generated endpoint modules are a lower-level interface; prefer the SDK so refresh and ownership behavior stay consistent.

```python
result = await client.rest.start_server(
    server_name="example",
)
print(result.model_dump(mode="json"))
```

Inspect the method signature and installed backend OpenAPI for exact arguments. Requests and successful typed responses use canonical Pydantic contracts. Call `model_dump(mode="json")` for JSON values; do not assume every returned object is a dictionary. Omitted generated optional parameters use `UNSET`, which differs from an explicitly supplied `None`.

Detailed variants such as `client.rest.list_servers_detailed()` retain status, headers and parsed response information. Normal variants return parsed values. Task acceptance describes scheduling; inspect the task result before assuming its operation succeeded. Partial and skipped outcomes require inspection even when no exception was raised.

Use the [Python model reference](reference/contracts.rst) for canonical contracts and your installed method signature for route-specific models. Regeneration replaces generated files; keep handwritten workflows outside that package.
