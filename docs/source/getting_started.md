# Connect and manage resources

Install `bsm-api-client` in your Python environment. Credentials or a supplied JWT authenticate protected operations. Choose credentials through environment configuration rather than putting them in source control.

```python
import asyncio
import os
from bsm_api_client import BedrockServerManagerApi

async def main():
    async with BedrockServerManagerApi(
        base_url=os.environ["BSM_URL"],
        username=os.environ["BSM_USERNAME"],
        password=os.environ["BSM_PASSWORD"],
    ) as client:
        servers = await client.rest.list_servers()
        print(servers.model_dump(mode="json"))

asyncio.run(main())
```

Authentication is lazy; entering the context does not connect to a WebSocket. Exiting closes owned transports, including after a request failure. Explicit `await client.close()` works when a context manager is inconvenient. Caller-supplied HTTP/WebSocket sessions remain caller-owned.

`base_url` can include an ingress/proxy mount. `base_path` selects the REST prefix and defaults to `/api`; it is not a prefix for every route. Keep `verify_ssl=True` outside explicitly trusted development environments. REST `request_timeout` is measured in seconds. `remember_me=True` requests the backend-configured longer credential-login lifetime; it does not extend a supplied JWT.
