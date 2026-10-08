"""Runtime OpenAPI discovery and dynamic endpoint invocation."""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional
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
    serialize_headers,
    serialize_query,
)

_PATH_PARAMETER_RE = re.compile(r"{([^}]+)}")


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
            from .generated import AuthenticatedClient
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
        schema = await self._fetch_openapi_schema()
        canonical = json.dumps(schema, sort_keys=True, separators=(",", ":")).encode()
        try:
            generated_ids = set(index_operations(generated_schema()))
        except InvalidInputError:
            generated_ids = set()
        operations = index_operations(schema, generated_ids)
        self._openapi_schema = schema
        self._openapi_fingerprint = hashlib.sha256(canonical).hexdigest()
        self._discovered_operations = operations
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
        supplied = {
            "path": path_params or {},
            "query": query or {},
            "header": headers or {},
        }
        for parameter in operation.parameters:
            location = parameter.get("in")
            name = parameter.get("name")
            if (
                parameter.get("required")
                and location in supplied
                and name not in supplied[location]
            ):
                raise InvalidInputError(
                    f"Missing required {location} parameter: {name}"
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
        path = self._render_path(operation.path, path_params or {})
        if path.startswith("/api/"):
            path = self._api_base_segment + path[4:]
        query = serialize_query(operation.parameters, query or {})
        if headers is not None:
            headers = serialize_headers(operation.parameters, headers)
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
            self._render_path(path, path_params or {}),
            query=query,
            json_data=json_data,
            form_data=form_data,
            headers=headers,
            authenticated=authenticated,
        )

    async def _ensure_authenticated(self, stale_token: Optional[str] = None) -> None:
        async with self._auth_lock:
            if self._jwt_token is None or self._jwt_token == stale_token:
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

    async def _dynamic_request(  # noqa: C901
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
    ) -> Any:
        url = f"{self._server_root_url}{path if path.startswith('/') else '/' + path}"
        request_headers = dict(self._default_headers)
        if raw_request is not None:
            request_headers.update(raw_request.headers)
            request_headers.pop("host", None)
        if headers:
            request_headers.update(
                {
                    key: str(value).lower() if isinstance(value, bool) else str(value)
                    for key, value in headers.items()
                }
            )
        if authenticated and not self._jwt_token:
            await self._ensure_authenticated()
        token_used = self._jwt_token
        if authenticated and self._jwt_token:
            request_headers["Authorization"] = f"Bearer {self._jwt_token}"
        if json_data is not None:
            request_headers.setdefault("Content-Type", "application/json")
        upload_data = None
        if files:
            upload_data = aiohttp.FormData()
            for key, value in (form_data or {}).items():
                upload_data.add_field(key, str(value))
            for key, value in files.items():
                filename, content, content_type = value
                if hasattr(content, "seek"):
                    content.seek(0)
                upload_data.add_field(
                    key, content, filename=filename, content_type=content_type
                )
        try:
            response_context = self._session.request(
                method.upper(),
                url,
                params=(
                    raw_request.url.params.multi_items()
                    if raw_request is not None
                    else _query_values(query or {})
                ),
                json=json_data,
                data=(
                    await raw_request.aread()
                    if raw_request is not None
                    else (
                        upload_data
                        if upload_data is not None
                        else (dict(form_data) if form_data is not None else None)
                    )
                ),
                headers=request_headers,
                timeout=self._request_timeout,
            )
            response = await response_context.__aenter__()
        except Exception as exc:
            raise CannotConnectError(
                f"Unable to connect to {url}", original_exception=exc
            ) from exc
        try:
            if response.status == 401 and authenticated and not is_retry and not files:
                # Release the failed response before refreshing the token or
                # retrying. Keeping it open can starve a constrained pool.
                response.release()
                await response_context.__aexit__(None, None, None)
                response_context = None
                await self._ensure_authenticated(stale_token=token_used)
                return await self._dynamic_request(
                    method,
                    path,
                    query=query,
                    json_data=json_data,
                    form_data=form_data,
                    headers=headers,
                    authenticated=authenticated,
                    is_retry=True,
                    raw_request=raw_request,
                    files=files,
                )
            if not response.ok:
                await self._handle_api_error(response, path)
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
            try:
                return await response.json(content_type=None)
            except (ValueError, TypeError):
                if response.content_type.startswith("text/"):
                    return await response.text()
                return await response.read()
        finally:
            if response_context is not None:
                await response_context.__aexit__(None, None, None)

    @staticmethod
    def _index_operations(schema: Mapping[str, Any]) -> Dict[str, DiscoveredOperation]:
        return index_operations(schema)

    @staticmethod
    def _render_path(path: str, values: Mapping[str, Any]) -> str:
        required = set(_PATH_PARAMETER_RE.findall(path))
        missing = required.difference(values)
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


def _response_value(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.content
