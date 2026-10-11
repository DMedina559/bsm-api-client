"""Runtime core and plugin contracts extend the generated REST API."""

from contextlib import AbstractAsyncContextManager
from typing import Any, Mapping

import httpx

from ..openapi import DiscoveredOperation
from .base import Service


class DiscoveryService(Service):
    """Inspect and invoke operations advertised by the connected backend."""

    @property
    def schema(self) -> Mapping[str, Any] | None:
        """Return the discovered OpenAPI snapshot, or None before discovery."""
        return self._owner.schema

    @property
    def operations(self) -> Mapping[str, DiscoveredOperation]:
        """Return operations indexed by operation ID."""
        return self._owner.operations

    @property
    def plugins(self) -> Mapping[str, tuple[DiscoveredOperation, ...]]:
        """Return advertised operations grouped by plugin identifier."""
        return self._owner.plugin_operations

    async def discover(
        self, *, force: bool = False
    ) -> Mapping[str, DiscoveredOperation]:
        """Fetch and index OpenAPI, reusing the snapshot unless force is true."""
        return await self._owner.async_discover_api(force=force)

    async def refresh(self) -> bool:
        """Fetch a fresh snapshot and report whether its fingerprint changed."""
        return await self._owner.async_refresh_api()

    async def call(self, operation_id: str, **kwargs: Any) -> Any:
        """Invoke an advertised operation using the runtime serializer.

        Keyword arguments match async_call_operation: path_params, query,
        headers, json_data, form_data, files, and authenticated. Responses are
        decoded as JSON values, text, or bytes according to Content-Type.
        """
        return await self._owner.async_call_operation(operation_id, **kwargs)

    def stream(
        self, operation_id: str, **kwargs: Any
    ) -> AbstractAsyncContextManager[httpx.Response]:
        """Open an advertised GET response as an async context manager.

        Keyword arguments match async_stream_operation. Consume aiter_bytes()
        inside the context so cancellation and partial reads release the connection.
        """
        return self._owner.async_stream_operation(operation_id, **kwargs)
