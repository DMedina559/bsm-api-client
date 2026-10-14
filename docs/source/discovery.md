# Live discovery and plugin operations

Discovery extends the bundled core contract with the running backend's schema. Refresh when plugins or server contracts change. The last validated snapshot remains available if a refresh fails; it is not proof that the backend still supports those operations.

```python
operations = await client.discovery.discover()
for operation_id, operation in operations.items():
    print(operation_id, operation.method, operation.path)

result = await client.discovery.call("get_application_health")
print(result)
```

Use `path_params`, `query`, `headers`, `json_data`, `form_data`, and `files` with `discovery.call`. Responses follow advertised media types: JSON values, text or bytes. Plugin operations are grouped under `client.discovery.plugins`; inspect their contracts instead of inventing argument names. Runtime discovery does not install missing backend features.

```python
result = await client.discovery.call(
    "get_server_status",
    path_params={"server_name": "example"},
)
```

Stream an advertised GET inside its context so cancellation and partial reads release the connection:

```python
async with client.discovery.stream("get_diagnostic_report") as response:
    with open("support-report.json", "wb") as output:
        async for chunk in response.aiter_bytes():
            output.write(chunk)
```

This minimal example overwrites the destination and uses synchronous local file I/O. Applications should use an atomic destination and move large file writes off the event loop. Review support metadata before sharing it.
