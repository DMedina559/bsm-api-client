"""Runtime plugin contracts extend the generated REST API."""

from .base import Service


class DiscoveryService(Service):
    @property
    def schema(self):
        return self._owner.schema

    @property
    def operations(self):
        return self._owner.operations

    @property
    def plugins(self):
        return self._owner.plugin_operations

    async def discover(self, *, force=False):
        return await self._owner.async_discover_api(force=force)

    async def refresh(self):
        return await self._owner.async_refresh_api()

    async def call(self, operation_id, **kwargs):
        return await self._owner.async_call_operation(operation_id, **kwargs)

    def stream(self, operation_id, **kwargs):
        return self._owner.async_stream_operation(operation_id, **kwargs)
