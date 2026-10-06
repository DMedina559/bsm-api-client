"""Runtime OpenAPI discovery and dynamic endpoint invocation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional
from urllib.parse import quote

from .exceptions import APIError, CannotConnectError

_HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
_PATH_PARAMETER_RE = re.compile(r"{([^}]+)}")


@dataclass(frozen=True)
class DiscoveredOperation:
    """An operation discovered from a BSM OpenAPI document."""

    operation_id: str
    method: str
    path: str
    tags: tuple[str, ...] = ()
    summary: Optional[str] = None
    description: Optional[str] = None
    deprecated: bool = False

    @property
    def namespace(self) -> str:
        if self.tags:
            return self.tags[0]
        parts = [p for p in self.path.split("/") if p and not p.startswith("{")]
        return parts[0] if parts else "default"


class DynamicOpenAPIMixin:
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
    def plugins(self) -> Mapping[str, tuple[DiscoveredOperation, ...]]:
        """Group plugin operations using plugin tags or /plugins/<name> paths."""
        grouped: Dict[str, list[DiscoveredOperation]] = {}
        for operation in self.operations.values():
            plugin_name = self._plugin_name(operation)
            if plugin_name:
                grouped.setdefault(plugin_name, []).append(operation)
        return {name: tuple(items) for name, items in grouped.items()}

    async def async_get_generated_client(self) -> Any:
        """Return the generated client using the current authentication state."""
        if not self._jwt_token:
            await self.authenticate()
        try:
            from .generated import AuthenticatedClient
        except ImportError as exc:
            raise RuntimeError(
                "The generated OpenAPI client is not present. Run the OpenAPI generation tools."
            ) from exc
        return AuthenticatedClient(
            base_url=self._server_root_url,
            token=self._jwt_token,
            verify_ssl=self._verify_ssl,
        )

    async def async_discover_api(
        self, *, force: bool = False
    ) -> Mapping[str, DiscoveredOperation]:
        """Fetch /openapi.json and index every HTTP operation exposed by BSM."""
        if self._openapi_schema is not None and not force:
            return self.operations
        schema = await self._fetch_openapi_schema()
        canonical = json.dumps(schema, sort_keys=True, separators=(",", ":")).encode()
        self._openapi_schema = schema
        self._openapi_fingerprint = hashlib.sha256(canonical).hexdigest()
        self._discovered_operations = self._index_operations(schema)
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
        authenticated: bool = True,
    ) -> Any:
        """Invoke an operation discovered from the live OpenAPI schema."""
        if not self.operations:
            await self.async_discover_api()
        try:
            operation = self.operations[operation_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown OpenAPI operationId {operation_id!r}. "
                "Refresh discovery to check for newly registered routes."
            ) from exc
        path = self._render_path(operation.path, path_params or {})
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

    async def _fetch_openapi_schema(self) -> Dict[str, Any]:
        headers = dict(self._default_headers)
        if self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"
        url = f"{self._base_url}/openapi.json"
        async with self._session.get(
            url, headers=headers, timeout=self._request_timeout
        ) as response:
            if response.status == 401 and not self._jwt_token:
                await self.authenticate()
                return await self._fetch_openapi_schema()
            if not response.ok:
                await self._handle_api_error(
                    response, f"{self._api_base_segment}/openapi.json"
                )
            data = await response.json(content_type=None)
        if not isinstance(data, dict) or "paths" not in data:
            raise APIError("Server returned an invalid OpenAPI document.")
        return data

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
    ) -> Any:
        url = f"{self._server_root_url}{path if path.startswith('/') else '/' + path}"
        request_headers = dict(self._default_headers)
        if headers:
            request_headers.update(headers)
        if authenticated and not self._jwt_token:
            await self.authenticate()
        if authenticated and self._jwt_token:
            request_headers["Authorization"] = f"Bearer {self._jwt_token}"
        if json_data is not None:
            request_headers.setdefault("Content-Type", "application/json")
        try:
            response_context = self._session.request(
                method.upper(),
                url,
                params=dict(query or {}),
                json=json_data,
                data=dict(form_data) if form_data is not None else None,
                headers=request_headers,
                timeout=self._request_timeout,
            )
            response = await response_context.__aenter__()
        except Exception as exc:
            raise CannotConnectError(
                f"Unable to connect to {url}", original_exception=exc
            ) from exc
        try:
            if response.status == 401 and authenticated and not is_retry:
                self._jwt_token = None
                await self.authenticate()
                return await self._dynamic_request(
                    method,
                    path,
                    query=query,
                    json_data=json_data,
                    form_data=form_data,
                    headers=headers,
                    authenticated=authenticated,
                    is_retry=True,
                )
            if not response.ok:
                await self._handle_api_error(response, path)
            if response.status == 204 or response.content_length == 0:
                return None
            try:
                return await response.json(content_type=None)
            except (ValueError, TypeError):
                return await response.text()
        finally:
            await response_context.__aexit__(None, None, None)

    @staticmethod
    def _index_operations(schema: Mapping[str, Any]) -> Dict[str, DiscoveredOperation]:
        result: Dict[str, DiscoveredOperation] = {}
        paths = schema.get("paths", {})
        if not isinstance(paths, Mapping):
            return result
        for path, path_item in paths.items():
            if not isinstance(path_item, Mapping):
                continue
            for method, details in path_item.items():
                if method.lower() not in _HTTP_METHODS or not isinstance(
                    details, Mapping
                ):
                    continue
                operation_id = details.get("operationId")
                if not operation_id:
                    operation_id = DynamicOpenAPIMixin._fallback_operation_id(
                        method, str(path)
                    )
                result[str(operation_id)] = DiscoveredOperation(
                    operation_id=str(operation_id),
                    method=method.upper(),
                    path=str(path),
                    tags=tuple(str(tag) for tag in details.get("tags", [])),
                    summary=details.get("summary"),
                    description=details.get("description"),
                    deprecated=bool(details.get("deprecated", False)),
                )
        return result

    @staticmethod
    def _fallback_operation_id(method: str, path: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", path).strip("_")
        return f"{method.lower()}_{cleaned}"

    @staticmethod
    def _render_path(path: str, values: Mapping[str, Any]) -> str:
        required = set(_PATH_PARAMETER_RE.findall(path))
        missing = required.difference(values)
        if missing:
            raise ValueError(f"Missing path parameters: {', '.join(sorted(missing))}")
        rendered = path
        for name in required:
            rendered = rendered.replace(
                "{" + name + "}", quote(str(values[name]), safe="")
            )
        return rendered

    @staticmethod
    def _plugin_name(operation: DiscoveredOperation) -> Optional[str]:
        for tag in operation.tags:
            lowered = tag.lower()
            for prefix in ("plugin:", "plugin."):
                if lowered.startswith(prefix):
                    return tag.removeprefix(prefix)
        parts = [part for part in operation.path.split("/") if part]
        if len(parts) >= 2 and parts[0] in {"plugin", "plugins"}:
            return parts[1]
        return None
