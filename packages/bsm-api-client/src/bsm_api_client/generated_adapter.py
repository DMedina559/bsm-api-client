"""Shared authentication and error policy for standard generated endpoints."""

from __future__ import annotations

import asyncio
import importlib
import json
from functools import lru_cache
from importlib.resources import files
from typing import Any, cast, get_args, get_type_hints

import httpx
from pydantic import BaseModel

from .contract_base import ContractModel
from .exceptions import APIError, InvalidInputError, NotFoundError
from .openapi import generated_schema, index_operations
from .validation import validate_input


class SharedTransport(httpx.AsyncBaseTransport):
    """Apply SDK authentication and error policy using its HTTPX pool."""

    def __init__(self, owner: Any, authenticated: bool):
        self.owner = owner
        self.authenticated = authenticated

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Send a generated request through SDK authentication and error handling."""
        path = request.url.raw_path.decode("ascii").split("?", 1)[0]
        prefix = (
            httpx.URL(self.owner._server_root_url).raw_path.decode("ascii").rstrip("/")
        )
        if prefix and path.startswith(prefix + "/"):
            path = path.removeprefix(prefix)
        if path.startswith("/api/"):
            path = self.owner._api_base_segment + path[4:]
        return cast(
            httpx.Response,
            await self.owner._dynamic_request(
                request.method,
                path,
                authenticated=self.authenticated,
                raw_request=request,
            ),
        )


async def call_generated(
    owner: Any,
    operation_id: str,
    *,
    parameters: dict[str, Any] | None = None,
    body: Any = None,
    authenticated: bool = True,
    detailed: bool = False,
    typed: bool = False,
) -> Any:
    """Use generated serialization and response parsing with shared transport."""
    if detailed and typed:
        raise InvalidInputError("Choose either detailed or typed response mode.")
    if (
        getattr(owner, "schema", None) is not None
        and operation_id not in owner.operations
    ):
        raise NotFoundError(f"Operation is unavailable on this server: {operation_id}")
    module = await asyncio.to_thread(operation_module, operation_id)
    kwargs = dict(parameters or {})
    try:
        if kwargs:
            await asyncio.to_thread(validate_generated_parameters, operation_id, kwargs)
        if body is not None:
            body = await asyncio.to_thread(validate_generated_body, operation_id, body)
            kwargs["body"] = generated_body(module, body)
        import inspect

        inspect.signature(module.asyncio_detailed).bind(client=None, **kwargs)
    except (TypeError, ValueError, KeyError) as exc:
        raise InvalidInputError(
            f"Invalid generated operation {operation_id}: {exc}"
        ) from exc
    try:
        client = owner._generated_client(authenticated)
        response = await module.asyncio_detailed(client=client, **kwargs)
    except APIError:
        raise
    except (TypeError, ValueError, KeyError) as exc:
        raise APIError(
            f"Unable to parse response for generated operation {operation_id}: {exc}"
        ) from exc
    return (
        response
        if detailed
        else (response.parsed if typed else response_value(response))
    )


def validate_generated_parameters(
    operation_id: str, parameters: dict[str, Any]
) -> None:
    """Validate supplied generated arguments against canonical parameter schemas."""
    from enum import Enum

    from .generated.types import Unset

    document = generated_schema()
    operation = index_operations(document)[operation_id]
    for parameter in operation.parameters:
        name = parameter["name"]
        python_name = name.replace("-", "_").lower()
        key = name if name in parameters else python_name
        if key not in parameters or isinstance(parameters[key], Unset):
            continue
        value = parameters[key]
        if isinstance(value, Enum):
            value = value.value
        validate_input(
            document,
            parameter.get("schema", {}),
            value,
            f"{parameter['in']} parameter {name}",
        )


def validate_generated_body(operation_id: str, body: Any) -> Any:
    """Validate a request body against its generated contract."""
    if isinstance(body, ContractModel):
        body = body.to_dict()
    elif isinstance(body, BaseModel):
        body = body.model_dump(mode="json", exclude_unset=True)
    document = generated_schema()
    operation = index_operations(document)[operation_id]
    for media_type, media in operation.request_body.get("content", {}).items():
        if media_type == "application/json" or media_type.endswith("+json"):
            validate_input(document, media.get("schema", {}), body, "request body")
            break
    return body


def response_value(response: Any) -> Any:
    """Extract a validated value from a generated response."""
    if not response.content:
        return None
    content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
    if content_type.startswith("text/"):
        return httpx.Response(
            200, headers=response.headers, content=response.content
        ).text
    if content_type != "application/json" and not content_type.endswith("+json"):
        return response.content
    try:
        return json.loads(response.content)
    except (ValueError, UnicodeDecodeError) as exc:
        raise APIError(
            "API returned malformed JSON.", status_code=response.status_code
        ) from exc


@lru_cache(maxsize=1)
def _operation_registry() -> dict[str, str]:
    """Load shipped operation metadata once, outside asynchronous callers."""
    root = files("bsm_api_client").joinpath("generated")
    try:
        return cast(
            dict[str, str],
            json.loads(root.joinpath("operations.json").read_text(encoding="utf-8")),
        )
    except FileNotFoundError as exc:
        raise InvalidInputError(
            "Generated client is unavailable; run scripts/generate_client.py."
        ) from exc


@lru_cache(maxsize=128)
def operation_module(operation_id: str) -> Any:
    """Resolve a generated module; async callers must use an executor."""
    registry = _operation_registry()
    if operation_id not in registry:
        raise NotFoundError(f"Operation is not generated: {operation_id}")
    return importlib.import_module(f"bsm_api_client.generated.{registry[operation_id]}")


def generated_body(module: Any, body: Any) -> Any:
    """Convert a canonical request into its generated transport representation."""
    if isinstance(body, ContractModel):
        body = body.to_dict()
    elif isinstance(body, BaseModel):
        body = body.model_dump(mode="json", exclude_unset=True)
    annotation = get_type_hints(module.asyncio_detailed).get("body")
    candidates = get_args(annotation) or (annotation,)
    model = next((t for t in candidates if hasattr(t, "from_dict")), None)
    return model.from_dict(body) if model and isinstance(body, dict) else body


class GeneratedOperationMethods:
    """Generated operation invocation shared by SDK services."""

    async def async_call_generated(
        self,
        operation_id: str,
        *,
        parameters: dict[str, Any] | None = None,
        body: Any = None,
        authenticated: bool = True,
        detailed: bool = False,
        typed: bool = False,
    ) -> Any:
        """Invoke a bundled operation through the shared SDK transport."""
        return await call_generated(
            self,
            operation_id,
            parameters=parameters,
            body=body,
            authenticated=authenticated,
            detailed=detailed,
            typed=typed,
        )
