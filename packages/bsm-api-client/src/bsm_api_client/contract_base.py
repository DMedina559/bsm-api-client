"""Common conveniences for generated public contracts."""

from typing import Any, Mapping, Self, cast

from pydantic import BaseModel, ConfigDict, SecretBytes, SecretStr, TypeAdapter


class ContractModel(BaseModel):
    """Canonical Pydantic fields with mapping access for SDK and CLI consumers."""

    model_config = ConfigDict(hide_input_in_errors=True)

    def get(self, key: str, default: Any = None) -> Any:
        """Read a model field by name, using the default when absent."""
        return getattr(self, key) if key in type(self).model_fields else default

    def __getitem__(self, key: str) -> Any:
        if key not in type(self).model_fields:
            raise KeyError(key)
        return getattr(self, key)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Self:
        """OpenAPI generator protocol backed by the public Pydantic contract."""
        return cast(Self, cls.model_validate(value))

    def to_dict(self) -> dict[str, Any]:
        """Serialize supplied fields with OpenAPI aliases, revealing secrets for the wire."""
        value = self.model_dump(mode="python", by_alias=True, exclude_unset=True)
        return cast(
            dict[str, Any],
            TypeAdapter(dict[str, Any]).dump_python(_wire_secrets(value), mode="json"),
        )


def _wire_secrets(value: Any) -> Any:
    """Reveal secret values only for explicit request wire serialization."""
    if isinstance(value, (SecretStr, SecretBytes)):
        return value.get_secret_value()
    if isinstance(value, dict):
        return {key: _wire_secrets(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_wire_secrets(item) for item in value]
    return value
