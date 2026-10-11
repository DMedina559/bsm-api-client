"""Common conveniences for generated public contracts."""

from typing import Any

from pydantic import BaseModel


class ContractModel(BaseModel):
    """Typed fields with mapping access for existing convenience consumers."""

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key) if key in type(self).model_fields else default

    def __getitem__(self, key: str) -> Any:
        if key not in type(self).model_fields:
            raise KeyError(key)
        return getattr(self, key)
