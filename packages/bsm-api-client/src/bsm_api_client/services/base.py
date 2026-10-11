"""Services share the SDK transport and generated operation core."""

from typing import Any


class Service:
    def __init__(self, owner):
        self._owner = owner

    async def async_call_generated(self, operation_id: str, **kwargs: Any) -> Any:
        return await self._owner.async_call_generated(operation_id, **kwargs)
