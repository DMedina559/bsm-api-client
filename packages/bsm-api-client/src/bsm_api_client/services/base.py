"""Services share the SDK transport and generated operation core."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..api_client import BedrockServerManagerApi


class Service:
    def __init__(self, owner: "BedrockServerManagerApi") -> None:
        self._owner = owner

    async def async_call_generated(self, operation_id: str, **kwargs: Any) -> Any:
        return await self._owner.async_call_generated(operation_id, **kwargs)
