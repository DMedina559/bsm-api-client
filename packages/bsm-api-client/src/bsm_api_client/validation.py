"""Validate runtime inputs against the advertised local JSON Schema contract."""

from typing import Any, Mapping, TypeVar, overload

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from pydantic import BaseModel, TypeAdapter, ValidationError
from referencing import Registry
from referencing.exceptions import Unresolvable

from .exceptions import APIError, InvalidInputError

Model = TypeVar("Model", bound=BaseModel)


@overload
def parse_response(model: type[Model], value: Any) -> Model: ...


@overload
def parse_response(model: Any, value: Any) -> Any: ...


def parse_response(model: Any, value: Any) -> Any:
    """Keep response contract failures in the API exception hierarchy."""
    try:
        return TypeAdapter(model).validate_python(value)
    except ValidationError as exc:
        raise APIError(
            f"API response did not match {getattr(model, '__name__', 'operation contract')}.",
            response_data={
                "validation_errors": exc.errors(
                    include_input=False, include_context=False, include_url=False
                )
            },
        ) from exc


def _nullable(value: Any) -> Any:
    """Translate OpenAPI 3.0 nullable without changing the cached document."""
    if isinstance(value, Mapping):
        result = {key: _nullable(child) for key, child in value.items()}
        if result.pop("nullable", False) and isinstance(result.get("type"), str):
            result["type"] = [result["type"], "null"]
        return result
    if isinstance(value, (tuple, list)):
        return [_nullable(child) for child in value]
    return value


def validate_input(
    document: Mapping[str, Any], spec: Mapping[str, Any], value: Any, label: str
) -> None:
    """Validate locally; external references are never fetched from the network."""
    if not spec:
        return
    root = _nullable(document)
    contract = _nullable(spec)
    try:
        Draft202012Validator.check_schema(contract)
        validator = Draft202012Validator(root, registry=Registry()).evolve(
            schema=contract
        )
        error = next(validator.iter_errors(value), None)
    except (SchemaError, Unresolvable) as exc:
        raise InvalidInputError(f"Unsupported schema for {label}.") from exc
    if error is not None:
        location = ".".join(str(part) for part in error.absolute_path)
        # Do not include values in diagnostics: request bodies may contain secrets.
        raise InvalidInputError(
            f"Invalid {label}{'.' + location if location else ''}: failed {error.validator} validation."
        )
