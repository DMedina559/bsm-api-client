# Bedrock Server Manager API Client Documentation

This document provides a high-level overview of the `bsm_api_client.BedrockServerManagerApi` Python client, used to interact with the Bedrock Server Manager API.

**Detailed method documentation has been migrated to the source code.** The client uses standard docstrings formatted with reStructuredText (RST) for Sphinx autodoc. You can view these docstrings directly in your IDE or by building the Sphinx documentation if configured. Each method docstring includes examples of how to use it.

## Initialization

The client is initialized as follows:

```python
from bsm_api_client import BedrockServerManagerApi
import asyncio

async def main():
    client = BedrockServerManagerApi(
        base_url="http://your_server_host:11325",
        username="your_username",
        password="your_password",
        # base_path="/api", # Optional, defaults to /api
        # request_timeout=10, # Optional, defaults to 10 seconds
        # verify_ssl=True # Optional, defaults to True
    )

    try:
        # Example: Get server list
        servers = await client.async_get_servers_details()
        print(servers)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Pydantic Models

The client uses Pydantic models for request payloads and response objects. This provides better data validation and an improved developer experience. The models are defined in `bsm_api_client.models`.

## Error Handling

The client raises custom exceptions found in `bsm_api_client.exceptions`:
*   `APIError`: Base class for API related errors.
*   `CannotConnectError`: For connection issues.
*   `AuthError`: For authentication failures (401, 403).
*   `NotFoundError`: For 404 errors.
*   `ServerNotFoundError`: Specific 404 for server resources.
*   `ServerNotRunningError`: If an operation requires a running server.
*   `InvalidInputError`: For 400 Bad Request or 422 Unprocessable Entity (validation errors).
*   `OperationFailedError`: For general operation failures (e.g., 501).
*   `APIServerSideError`: For 500-level server errors.

Error responses from the API (often JSON with "message" or "detail" keys) are parsed and included in the exception.
