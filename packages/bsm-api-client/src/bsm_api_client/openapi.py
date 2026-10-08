"""Shared, non-executable OpenAPI metadata and contract comparison."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import asdict, dataclass, field
from importlib.resources import files
from typing import Any, Mapping, cast

from .exceptions import InvalidInputError

HTTP_METHODS = frozenset(
    ("get", "put", "post", "delete", "options", "head", "patch", "trace")
)


def resolve(
    schema: Mapping[str, Any], value: Any, seen: frozenset[str] = frozenset()
) -> Any:
    """Resolve local references for inspection without executing remote content."""
    if not isinstance(value, Mapping) or "$ref" not in value:
        return copy.deepcopy(value)
    ref = value["$ref"]
    if not isinstance(ref, str) or not ref.startswith("#/") or ref in seen:
        return copy.deepcopy(value)
    target: Any = schema
    try:
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
    except (KeyError, TypeError) as exc:
        raise InvalidInputError(f"Unresolved OpenAPI reference: {ref}") from exc
    result = resolve(schema, target, seen | {ref})
    return {**result, **{k: copy.deepcopy(v) for k, v in value.items() if k != "$ref"}}


@dataclass(frozen=True)
class ApiOperation:
    """Common operation contract for generated, dynamic, and CLI consumers."""

    operation_id: str
    method: str
    path: str
    tags: tuple[str, ...] = ()
    summary: str | None = None
    description: str | None = None
    deprecated: bool = False
    parameters: tuple[dict[str, Any], ...] = ()
    request_body: dict[str, Any] = field(default_factory=dict)
    responses: dict[str, Any] = field(default_factory=dict)
    security: tuple[dict[str, Any], ...] = ()
    plugin: str | None = None
    generated: bool = False

    @property
    def requires_authentication(self) -> bool:
        """OpenAPI security is optional when any alternative is empty."""
        return bool(self.security) and {} not in self.security

    @property
    def namespace(self) -> str:
        return self.tags[0] if self.tags else "default"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Preserve the discovery layer's public name.
DiscoveredOperation = ApiOperation


def index_operations(
    schema: Mapping[str, Any], generated_ids: set[str] | None = None
) -> dict[str, ApiOperation]:
    result = {}
    for path, raw_item in schema.get("paths", {}).items():
        item = resolve(schema, raw_item)
        for method, raw_details in item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(
                raw_details, Mapping
            ):
                continue
            details = resolve(schema, raw_details)
            identifier = (
                details.get("operationId")
                or f"{method.lower()}_{re.sub(r'[^a-zA-Z0-9]+', '_', path).strip('_')}"
            )
            if identifier in result:
                raise InvalidInputError(f"Duplicate OpenAPI operationId: {identifier}")
            parameters = {}
            for parameter in (
                *item.get("parameters", []),
                *details.get("parameters", []),
            ):
                parameter = resolve(schema, parameter)
                parameters[(parameter["in"], parameter["name"])] = parameter
            tags = tuple(details.get("tags", ()))
            plugin = plugin_owner(path, item, details, tags)
            result[identifier] = ApiOperation(
                operation_id=identifier,
                method=method.upper(),
                path=path,
                tags=tags,
                summary=details.get("summary"),
                description=details.get("description"),
                deprecated=bool(details.get("deprecated")),
                parameters=tuple(parameters.values()),
                request_body=resolve(schema, details.get("requestBody", {})),
                responses={
                    str(k): resolve(schema, v)
                    for k, v in details.get("responses", {}).items()
                },
                security=tuple(details.get("security", schema.get("security", ()))),
                plugin=plugin,
                generated=identifier in (generated_ids or set()),
            )
    return result


def generated_schema() -> dict[str, Any]:
    """Read the exact schema shipped with this client build."""
    resource = files("bsm_api_client").joinpath("generated", "openapi.json")
    if not resource.is_file():
        raise InvalidInputError(
            "Generated schema is unavailable; generate the client first."
        )
    return cast(dict[str, Any], json.loads(resource.read_text(encoding="utf-8")))


def _contract(schema: Mapping[str, Any], operation: ApiOperation) -> dict[str, Any]:
    """Include transitive model references so component changes appear in diffs."""
    value = operation.to_dict()
    value.pop("generated")
    refs: dict[str, Any] = {}

    def visit(node: Any) -> None:
        if isinstance(node, Mapping):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/") and ref not in refs:
                refs[ref] = None
                refs[ref] = resolve(schema, {"$ref": ref})
                visit(refs[ref])
            for child in node.values():
                visit(child)
        elif isinstance(node, (list, tuple)):
            for child in node:
                visit(child)

    visit(value)
    for requirement in operation.security:
        for name in requirement:
            pointer = "#/components/securitySchemes/" + name.replace("~", "~0").replace(
                "/", "~1"
            )
            if name in schema.get("components", {}).get("securitySchemes", {}):
                refs[pointer] = resolve(schema, {"$ref": pointer})
    return {"operation": value, "components": refs}


def diff_schemas(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    generated_ids: set[str] | None = None,
) -> dict[str, list[str]]:
    old, new = index_operations(before), index_operations(after)
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "changed": sorted(
            k
            for k in old.keys() & new.keys()
            if _contract(before, old[k]) != _contract(after, new[k])
        ),
        "generated": sorted(new.keys() & (generated_ids or set())),
    }


@dataclass(frozen=True)
class ApiCapabilities:
    operations: Mapping[str, ApiOperation]

    def has(self, operation_id: str) -> bool:
        return operation_id in self.operations

    @property
    def plugins(self) -> Mapping[str, tuple[ApiOperation, ...]]:
        names = sorted({op.plugin for op in self.operations.values() if op.plugin})
        return {
            name: tuple(op for op in self.operations.values() if op.plugin == name)
            for name in names
        }

    @property
    def runtime_only(self) -> tuple[str, ...]:
        return tuple(sorted(k for k, op in self.operations.items() if not op.generated))


def plugin_owner(
    path: str,
    item: Mapping[str, Any],
    details: Mapping[str, Any],
    tags: tuple[str, ...],
) -> str | None:
    explicit = details.get("x-bsm-plugin") or item.get("x-bsm-plugin")
    if explicit:
        return str(explicit)
    for tag in tags:
        for prefix in ("plugin:", "plugin."):
            if tag.lower().startswith(prefix):
                offset = len(prefix)
                return tag[offset:]
    parts = path.strip("/").split("/")
    if parts and parts[0] == "api":
        parts = parts[1:]
    if len(parts) > 1 and parts[0] in ("plugin", "plugins") and "{" not in parts[1]:
        if any(tag.lower() == "plugin management" for tag in tags):
            return None
        return parts[1]
    # Built-in backend routers use human-readable tags such as
    # "Download Page Plugin", while plugin management uses module names.
    owners = {
        re.sub(r"[^a-z0-9]+", "_", tag.lower()).strip("_")
        for tag in tags
        if tag.lower().endswith(" plugin")
    }
    if len(owners) == 1:
        return owners.pop()
    return None


def serialize_query(
    parameters: tuple[dict[str, Any], ...], values: Mapping[str, Any]
) -> dict[str, Any]:
    """Serialize OpenAPI form query arrays/objects, including explode defaults."""
    result = dict(values)

    def scalar(value):
        return str(value).lower() if isinstance(value, bool) else str(value)

    for parameter in parameters:
        name = parameter["name"]
        if parameter["in"] != "query" or name not in result:
            continue
        value = result[name]
        style = parameter.get("style", "form")
        if style != "form":
            raise InvalidInputError(
                f"Unsupported query serialization style {style!r} for {name}."
            )
        explode = parameter.get("explode", True)
        if isinstance(value, Mapping):
            if explode:
                del result[name]
                for key, item in value.items():
                    if key in result:
                        raise InvalidInputError(
                            f"Conflicting exploded query parameter: {key}"
                        )
                    result[str(key)] = item
            else:
                result[name] = ",".join(
                    scalar(item) for pair in value.items() for item in pair
                )
        elif isinstance(value, (list, tuple)) and not explode:
            result[name] = ",".join(scalar(item) for item in value)
    return result


def serialize_headers(
    parameters: tuple[dict[str, Any], ...], values: Mapping[str, Any]
) -> dict[str, str]:
    """Serialize OpenAPI simple header values before handing them to HTTP."""

    def scalar(value):
        return str(value).lower() if isinstance(value, bool) else str(value)

    result = {key: scalar(value) for key, value in values.items()}
    for parameter in parameters:
        name = parameter["name"]
        if parameter["in"] != "header" or name not in values:
            continue
        if parameter.get("style", "simple") != "simple":
            raise InvalidInputError(f"Unsupported header style for {name}.")
        value = values[name]
        if isinstance(value, Mapping):
            result[name] = (
                ",".join(f"{key}={scalar(item)}" for key, item in value.items())
                if parameter.get("explode", False)
                else ",".join(scalar(item) for pair in value.items() for item in pair)
            )
        elif isinstance(value, (list, tuple)):
            result[name] = ",".join(scalar(item) for item in value)
    return result
