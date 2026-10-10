"""Runtime OpenAPI discovery and dynamic endpoint invocation."""

from __future__ import annotations

import asyncio
import logging
import re
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Mapping, Optional
from urllib.parse import quote

import aiohttp
import httpx

from .exceptions import (
    APIError,
    AuthError,
    CannotConnectError,
    InvalidInputError,
    NotFoundError,
)
from .generated_adapter import GeneratedOperationMethods, SharedTransport
from .openapi import (
    ApiCapabilities,
    DiscoveredOperation,
    diff_schemas,
    generated_schema,
    index_operations,
    schema_fingerprint,
    serialize_headers,
    serialize_query,
)
from .validation import validate_input

_PATH_PARAMETER_RE = re.compile(r"{([^}]+)}")
_LOGGER = logging.getLogger(__name__)


class DynamicOpenAPIMixin(GeneratedOperationMethods):
    """Discover and invoke API operations unknown at package build time."""

    if TYPE_CHECKING:
        _default_headers: Mapping[str, str]
        _jwt_token: Optional[str]
        _base_url: str
        _server_root_url: str
        _api_base_segment: str
        _request_timeout: Any
        _verify_ssl: bool
        _session: Any

        _auth_lock: asyncio.Lock

        async def authenticate(self) -> Any: ...
        async def _handle_api_error(self, response: Any, path: str) -> Any: ...

    _openapi_schema: Optional[Dict[str, Any]] = None
    _openapi_fingerprint: Optional[str] = None
    _discovered_operations: Dict[str, DiscoveredOperation]

    @property
    def schema(self) -> Optional[Mapping[str, Any]]:
        return self._openapi_schema

    @property
    def schema_fingerprint(self) -> Optional[str]:
        return self._openapi_fingerprint

    @property
    def operations(self) -> Mapping[str, DiscoveredOperation]:
        return getattr(self, "_discovered_operations", {})

    @property
    def discovered_operations(self) -> Mapping[str, DiscoveredOperation]:
        return self.operations

    @property
    def capabilities(self) -> ApiCapabilities:
        return ApiCapabilities(self.operations)

    @property
    def plugins(self) -> Mapping[str, tuple[DiscoveredOperation, ...]]:
        return self.capabilities.plugins

    def api_diff(
        self, against: Optional[Mapping[str, Any]] = None
    ) -> Dict[str, list[str]]:
        if self.schema is None:
            raise InvalidInputError("Discover the API before comparing schemas.")
        try:
            build_schema = generated_schema()
        except InvalidInputError:
            if against is None:
                raise
            build_schema = {"paths": {}}
        return diff_schemas(
            against if against is not None else build_schema,
            self.schema,
            generated_ids=set(index_operations(build_schema)),
        )

    async def async_get_generated_client(self) -> Any:
        """Return the generated client using the current authentication state."""
        if not self._jwt_token:
            await self._ensure_authenticated()
        try:
            from .generated.client import AuthenticatedClient
        except ImportError as exc:
            raise RuntimeError(
                "The generated OpenAPI client is not present. Run the OpenAPI generation tools."
            ) from exc
        if not self._jwt_token:
            raise AuthError("Authentication did not provide a token.")
        generated = AuthenticatedClient(
            base_url=self._server_root_url,
            token=self._jwt_token,
            verify_ssl=self._verify_ssl,
        )
        transport = httpx.AsyncClient(
            base_url=self._server_root_url, transport=SharedTransport(self, True)
        )
        generated.set_async_httpx_client(transport)
        if not hasattr(self, "_generated_http_clients"):
            self._generated_http_clients = []
        self._generated_http_clients.append(transport)
        return generated

    async def async_discover_api(
        self, *, force: bool = False
    ) -> Mapping[str, DiscoveredOperation]:
        """Fetch /openapi.json and index every HTTP operation exposed by BSM."""
        if self._openapi_schema is not None and not force:
            return self.operations
        if not hasattr(self, "_discovery_lock"):
            self._discovery_lock = asyncio.Lock()
        previous = self._openapi_schema
        async with self._discovery_lock:
            # Coalesce refreshes that were waiting for the same snapshot.
            if self._openapi_schema is not None and (
                not force or self._openapi_schema is not previous
            ):
                return self.operations
            schema = await self._fetch_openapi_schema()
            try:
                generated_ids = set(index_operations(generated_schema()))
            except InvalidInputError:
                generated_ids = set()
            operations = index_operations(schema, generated_ids)
            fingerprint = schema_fingerprint(schema)
            # Publish only after the entire document has been validated.
            self._openapi_schema = schema
            self._openapi_fingerprint = fingerprint
            self._discovered_operations = operations
            _LOGGER.debug(
                "OpenAPI discovery completed",
                extra={
                    "operation_count": len(operations),
                    "schema_fingerprint": fingerprint,
                },
            )
            return self.operations

    async def async_refresh_api(self) -> bool:
        """Refresh discovery and return True when the server schema changed."""
        previous = self._openapi_fingerprint
        await self.async_discover_api(force=True)
        return previous is not None and previous != self._openapi_fingerprint

    async def async_call_operation(
        self,
        operation_id: str,
        *,
        path_params: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        json_data: Any = None,
        form_data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        files: Optional[Mapping[str, Any]] = None,
        authenticated: bool = True,
    ) -> Any:
        """Invoke an operation discovered from the live OpenAPI schema."""
        if not self.operations:
            await self.async_discover_api()
        try:
            operation = self.operations[operation_id]
        except KeyError as exc:
            raise NotFoundError(
                f"Unknown OpenAPI operationId {operation_id!r}. "
                "Refresh discovery to check for newly registered routes."
            ) from exc
        if json_data is not None and (form_data is not None or files):
            raise InvalidInputError("Choose either JSON or form data.")
        self._validate_operation_inputs(
            operation,
            operation_id,
            path_params,
            query,
            headers,
            json_data,
            form_data,
            files,
        )
        path = self._render_path(operation.path, path_params or {})
        path = self._normalize_api_path(path)
        query = serialize_query(operation.parameters, query or {})
        if headers is not None:
            headers = serialize_headers(operation.parameters, headers)
        content = operation.request_body.get("content", {})
        if (
            form_data is not None
            and "multipart/form-data" in content
            and "application/x-www-form-urlencoded" not in content
        ):
            return await self._dynamic_request(
                operation.method,
                path,
                query=query,
                form_data=form_data,
                files=files,
                headers=headers,
                authenticated=authenticated,
                multipart=True,
            )
        if files:
            return await self._dynamic_request(
                operation.method,
                path,
                query=query,
                form_data=form_data,
                headers=headers,
                authenticated=authenticated,
                files=files,
            )
        return await self._dynamic_request(
            operation.method,
            path,
            query=query,
            json_data=json_data,
            form_data=form_data,
            headers=headers,
            authenticated=authenticated,
        )

    def _validate_operation_inputs(
        self,
        operation: DiscoveredOperation,
        operation_id: str,
        path_params: Optional[Mapping[str, Any]],
        query: Optional[Mapping[str, Any]],
        headers: Optional[Mapping[str, str]],
        json_data: Any,
        form_data: Optional[Mapping[str, Any]],
        files: Optional[Mapping[str, Any]],
    ) -> None:
        self._validate_parameters(operation, path_params, query, headers)
        content = operation.request_body.get("content", {})
        if (
            json_data is not None
            and content
            and not any(
                kind == "application/json" or kind.endswith("+json") for kind in content
            )
        ):
            raise InvalidInputError(
                f"Operation {operation_id} does not advertise a JSON request body."
            )
        if (form_data is not None or files) and content:
            expected = (
                "multipart/form-data" if files else "application/x-www-form-urlencoded"
            )
            if expected not in content and not (
                form_data is not None and "multipart/form-data" in content
            ):
                raise InvalidInputError(
                    f"Operation {operation_id} does not advertise {expected}."
                )
        if (
            operation.request_body.get("required")
            and json_data is None
            and form_data is None
            and not files
        ):
            raise InvalidInputError(
                f"Operation {operation_id} requires a request body."
            )
        if json_data is not None:
            media: Mapping[str, Any] = next(
                (
                    value
                    for kind, value in content.items()
                    if kind == "application/json" or kind.endswith("+json")
                ),
                {},
            )
            validate_input(
                self.schema or {}, media.get("schema", {}), json_data, "request body"
            )

    def _validate_parameters(self, operation, path_params, query, headers):
        supplied = {
            "path": path_params or {},
            "query": query or {},
            "header": headers or {},
        }
        for parameter in operation.parameters:
            location = parameter.get("in")
            name = parameter.get("name")
            if location == "header" and isinstance(name, str):
                name = next(
                    (key for key in supplied["header"] if key.lower() == name.lower()),
                    name,
                )
            if location == "cookie":
                raise InvalidInputError(
                    f"Cookie parameter {name} is not supported by this client."
                )
            if not isinstance(name, str):
                raise InvalidInputError("OpenAPI parameter is missing a name.")
            if (
                parameter.get("required")
                and location in supplied
                and (name not in supplied[location] or supplied[location][name] is None)
            ):
                raise InvalidInputError(
                    f"Missing required {location} parameter: {name}"
                )
            if location in supplied and name in supplied[location]:
                validate_input(
                    self.schema or {},
                    parameter.get("schema", {}),
                    supplied[location][name],
                    f"{location} parameter {name}",
                )

    async def async_call_path(
        self,
        method: str,
        path: str,
        *,
        path_params: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        json_data: Any = None,
        form_data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        authenticated: bool = True,
    ) -> Any:
        """Invoke a path directly, including endpoints without operationId."""
        return await self._dynamic_request(
            method.upper(),
            self._normalize_api_path(self._render_path(path, path_params or {})),
            query=query,
            json_data=json_data,
            form_data=form_data,
            headers=headers,
            authenticated=authenticated,
        )

    async def _ensure_authenticated(
        self, stale_token: Optional[str] = None, stale_generation: Optional[int] = None
    ) -> None:
        async with self._auth_lock:
            if self._jwt_token is None or (
                self._jwt_token == stale_token
                and (
                    stale_generation is None
                    or getattr(self, "_auth_generation", 0) == stale_generation
                )
            ):
                self._jwt_token = None
                await self.authenticate()
                if not self._jwt_token:
                    raise AuthError("Authentication did not provide a token.")

    async def _fetch_openapi_schema(self) -> Dict[str, Any]:
        data = await self._dynamic_request(
            "GET", f"{self._api_base_segment}/openapi.json", authenticated=True
        )
        if not isinstance(data, dict) or not isinstance(data.get("paths"), dict):
            raise APIError("Server returned an invalid OpenAPI document.")
        return data

    def _request_headers(self, headers, raw_request, authenticated):
        result = dict(self._default_headers)
        if raw_request is not None:
            result.update(raw_request.headers)
        result.update(headers or {})
        result = {
            key: _form_value(value)
            for key, value in result.items()
            if key.lower()
            not in {"host", "content-length", "transfer-encoding", "authorization"}
        }
        if authenticated and self._jwt_token:
            result["Authorization"] = f"Bearer {self._jwt_token}"
        return result

    @staticmethod
    def _request_body(form_data, files, raw_request, multipart=False):
        if raw_request is not None:
            return raw_request.stream
        if not files and not multipart:
            return _query_values(form_data) if form_data is not None else None
        upload = aiohttp.FormData(default_to_multipart=True)
        for key, value in (form_data or {}).items():
            for item in value if isinstance(value, (list, tuple)) else [value]:
                upload.add_field(key, _form_value(item))
        for key, value in (files or {}).items():
            entries = value if isinstance(value, list) else [value]
            for filename, content, content_type in entries:
                upload.add_field(
                    key, content, filename=filename, content_type=content_type
                )
        return upload

    @asynccontextmanager
    async def _open_response(
        self,
        method,
        path,
        *,
        query=None,
        json_data=None,
        form_data=None,
        headers=None,
        authenticated=True,
        is_retry=False,
        raw_request=None,
        files=None,
        multipart=False,
    ) -> AsyncIterator[aiohttp.ClientResponse]:
        """Own connections, authentication, and bounded replay for every transport."""
        if authenticated and not self._jwt_token:
            await self._ensure_authenticated()
        url = f"{self._server_root_url}{path if path.startswith('/') else '/' + path}"
        replayable = (
            not files
            and not multipart
            and (
                raw_request is None or isinstance(raw_request.stream, httpx.ByteStream)
            )
        )
        for attempt in range(1 if is_retry or not replayable else 2):
            token_used = self._jwt_token
            generation_used = getattr(self, "_auth_generation", 0)
            request_headers = self._request_headers(headers, raw_request, authenticated)
            try:
                context = self._session.request(
                    method.upper(),
                    url,
                    params=(
                        raw_request.url.params.multi_items()
                        if raw_request is not None
                        else _query_values(query or {})
                    ),
                    json=json_data,
                    data=self._request_body(form_data, files, raw_request, multipart),
                    headers=request_headers,
                    timeout=self._request_timeout,
                    ssl=None if self._verify_ssl else False,
                    allow_redirects=False,
                )
                response = await context.__aenter__()
            except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as exc:
                raise CannotConnectError(
                    "Unable to connect to the API.", original_exception=exc
                ) from exc
            _LOGGER.debug(
                "API response received",
                extra={
                    "http_method": method.upper(),
                    "http_status": response.status,
                    "auth_retry": bool(attempt),
                },
            )
            refresh = (
                response.status == 401
                and authenticated
                and replayable
                and attempt == 0
                and not is_retry
            )
            try:
                if not refresh:
                    await self._check_response(response, path)
                    yield response
                    return
                response.release()
            finally:
                await context.__aexit__(None, None, None)
            await self._ensure_authenticated(
                stale_token=token_used, stale_generation=generation_used
            )

    async def _check_response(self, response, path):
        if response.status >= 400:
            await self._handle_api_error(response, path)
        if 300 <= response.status < 400:
            raise APIError(
                "API redirects are not followed.", status_code=response.status
            )

    async def _dynamic_request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        json_data: Any = None,
        authenticated: bool = True,
        form_data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        is_retry: bool = False,
        raw_request: Optional[httpx.Request] = None,
        files: Optional[Mapping[str, Any]] = None,
        multipart: bool = False,
    ) -> Any:
        async with self._open_response(
            method,
            path,
            query=query,
            json_data=json_data,
            authenticated=authenticated,
            form_data=form_data,
            headers=headers,
            is_retry=is_retry,
            raw_request=raw_request,
            files=files,
            multipart=multipart,
        ) as response:
            if raw_request is not None:
                return httpx.Response(
                    response.status,
                    headers={
                        key: value
                        for key, value in response.headers.items()
                        if key.lower() not in {"content-encoding", "content-length"}
                    },
                    content=await response.read(),
                    request=raw_request,
                )
            if response.status == 204 or response.content_length == 0:
                return None
            return await _read_response(response)

    @asynccontextmanager
    async def async_stream_operation(
        self,
        operation_id: str,
        *,
        path_params: Optional[Mapping[str, Any]] = None,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        authenticated: Optional[bool] = None,
    ) -> AsyncIterator[aiohttp.ClientResponse]:
        """Stream a discovered GET response without buffering the entire file.

        Use ``async with client.async_stream_operation(id) as response`` and
        iterate ``response.content.iter_chunked(65536)``. Exiting the context
        releases the connection, including on cancellation or partial reads.
        """
        if not self.operations:
            await self.async_discover_api()
        operation = self.operations.get(operation_id)
        if operation is None:
            raise NotFoundError(f"Unknown OpenAPI operationId {operation_id!r}.")
        if operation.method != "GET":
            raise InvalidInputError("Streaming downloads require a GET operation.")
        self._validate_operation_inputs(
            operation, operation_id, path_params, query, headers, None, None, None
        )
        async with self._open_response(
            "GET",
            self._normalize_api_path(
                self._render_path(operation.path, path_params or {})
            ),
            query=serialize_query(operation.parameters, query or {}),
            headers=serialize_headers(operation.parameters, headers or {}),
            authenticated=(
                operation.requires_authentication
                if authenticated is None
                else authenticated
            ),
        ) as response:
            yield response

    def _normalize_api_path(self, path: str) -> str:
        if path == "/api" or path.startswith("/api/"):
            return self._api_base_segment + path[4:]
        return path

    @staticmethod
    def _index_operations(schema: Mapping[str, Any]) -> Dict[str, DiscoveredOperation]:
        return index_operations(schema)

    @staticmethod
    def _render_path(path: str, values: Mapping[str, Any]) -> str:
        required = set(_PATH_PARAMETER_RE.findall(path))
        missing = {
            name for name in required if name not in values or values[name] is None
        }
        if missing:
            raise InvalidInputError(
                f"Missing path parameters: {', '.join(sorted(missing))}"
            )
        rendered = path
        for name in required:
            rendered = rendered.replace(
                "{" + name + "}", quote(str(values[name]), safe="")
            )
        return rendered


def _query_values(query: Mapping[str, Any]) -> Dict[str, Any]:
    def value(item: Any) -> Any:
        if isinstance(item, bool):
            return "true" if item else "false"
        if isinstance(item, (list, tuple)):
            return [value(child) for child in item]
        return item

    return {key: value(item) for key, item in query.items() if item is not None}


def _form_value(value: Any) -> str:
    return str(value).lower() if isinstance(value, bool) else str(value)


async def _read_response(response: aiohttp.ClientResponse) -> Any:
    content_type = response.content_type
    if content_type == "application/json" or content_type.endswith("+json"):
        try:
            return await response.json(content_type=None)
        except (ValueError, UnicodeDecodeError) as exc:
            raise APIError(
                "API returned malformed JSON.", status_code=response.status
            ) from exc
    if content_type.startswith("text/"):
        return await response.text()
    return await response.read()
