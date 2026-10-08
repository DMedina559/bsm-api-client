"""Stable adapter around the disposable generated endpoint modules."""

from __future__ import annotations

import importlib
import json
from functools import lru_cache
from importlib.resources import files
from typing import Any, cast, get_args, get_type_hints

import httpx

from .exceptions import APIError, InvalidInputError, NotFoundError


class SharedTransport(httpx.AsyncBaseTransport):
    """Run generated HTTP requests through the facade's auth/error transport."""

    def __init__(self, owner: Any, authenticated: bool):
        self.owner = owner
        self.authenticated = authenticated

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.raw_path.decode("ascii").split("?", 1)[0]
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
    module = operation_module(operation_id)
    from .generated import Client

    kwargs = dict(parameters or {})
    try:
        if body is not None:
            kwargs["body"] = generated_body(module, body)
        import inspect

        inspect.signature(module.asyncio_detailed).bind(client=None, **kwargs)
    except (TypeError, ValueError, KeyError) as exc:
        raise InvalidInputError(
            f"Invalid generated operation {operation_id}: {exc}"
        ) from exc
    try:
        async with httpx.AsyncClient(
            base_url=owner._server_root_url,
            transport=SharedTransport(owner, authenticated),
        ) as transport:
            client = Client(base_url=owner._server_root_url).set_async_httpx_client(
                transport
            )
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


def response_value(response: Any) -> Any:
    if not response.content:
        return None
    try:
        return json.loads(response.content)
    except (ValueError, UnicodeDecodeError):
        return response.content


@lru_cache(maxsize=128)
def operation_module(operation_id: str) -> Any:
    root = files("bsm_api_client").joinpath("generated")
    try:
        registry = json.loads(
            root.joinpath("operations.json").read_text(encoding="utf-8")
        )
    except FileNotFoundError as exc:
        raise InvalidInputError(
            "Generated client is unavailable; run tools/generate_client.py."
        ) from exc
    if operation_id not in registry:
        raise NotFoundError(f"Operation is not generated: {operation_id}")
    return importlib.import_module(f"bsm_api_client.generated.{registry[operation_id]}")


def generated_body(module: Any, body: Any) -> Any:
    annotation = get_type_hints(module.asyncio_detailed).get("body")
    candidates = get_args(annotation) or (annotation,)
    model = next((t for t in candidates if hasattr(t, "from_dict")), None)
    return model.from_dict(body) if model and isinstance(body, dict) else body


class GeneratedOperationMethods:
    """Shared operation invocation used by every compatibility mixin."""

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
        return await call_generated(
            self,
            operation_id,
            parameters=parameters,
            body=body,
            authenticated=authenticated,
            detailed=detailed,
            typed=typed,
        )
