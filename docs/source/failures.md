# Validation, errors and retries

Local Pydantic validation rejects invalid request models. The SDK validates runtime arguments against known contracts and parses typed responses. Server failures become exceptions from `bsm_api_client.exceptions`; inspect the actual exception type and structured details rather than matching message text.

```python
from bsm_api_client.exceptions import APIError, AuthError, NotFoundError

try:
    result = await client.rest.list_servers()
except AuthError:
    raise  # Correct credentials or permissions before retrying.
except NotFoundError:
    raise  # Verify endpoint/resource and installed backend version.
except APIError as error:
    print(error)
    raise
```

Credential refresh is coalesced and limits authenticated 401 replay to one retry. Streams/uploads that cannot safely replay are not blindly retried. Redirects are rejected. A supplied JWT cannot be refreshed without credentials.

An incomplete-operation error can retain a committed result: inspect its structured details before retrying a mutation. A lost connection does not prove the operation was rolled back. Reconcile server/task state before repeating destructive calls. Keep cancellation as cancellation and close owned resources in `finally` or an async context manager.
