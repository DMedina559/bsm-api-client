"""OpenAPI inspection and invocation without generated top-level commands."""

from __future__ import annotations

import json
import mimetypes
import os
import tempfile
from contextlib import ExitStack
from pathlib import Path
from typing import Any

import click

from bsm_api_client.exceptions import InvalidInputError, NotFoundError
from bsm_api_client.openapi import resolve
from bsm_cli.completion import (
    cached_schema,
    complete_operation,
    complete_parameter,
    complete_plugin,
)
from bsm_cli.decorators import pass_async_context
from bsm_cli.output import emit, get_client


async def discover(ctx, *, force=False):
    client = get_client(ctx)
    await client.async_discover_api(force=force)
    return client


def assignments(values):
    result = {}
    for value in values:
        name, separator, text = value.partition("=")
        if not separator or not name:
            raise click.BadParameter("Expected NAME=VALUE.")
        if name in result:
            raise click.BadParameter(f"Duplicate parameter: {name}")
        result[name] = text
    return result


def _non_null_schema(schema, spec):
    if "anyOf" in spec:
        choices = [resolve(schema, item) for item in spec["anyOf"]]
        return next((item for item in choices if item.get("type") != "null"), spec)
    return spec


def parameter_value(schema, parameter, value):
    spec = resolve(schema, parameter.get("schema", {}))
    spec = _non_null_schema(schema, spec)
    kind = spec.get("type", "string")
    parsed: Any
    try:
        if kind == "integer":
            parsed = int(value)
        elif kind == "number":
            parsed = float(value)
        elif kind == "boolean":
            if value.lower() not in ("true", "false"):
                raise ValueError("Expected true or false")
            parsed = value.lower() == "true"
        elif kind in ("array", "object"):
            parsed = json.loads(value)
            if not isinstance(parsed, list if kind == "array" else dict):
                raise ValueError(f"Expected JSON {kind}")
        else:
            parsed = value
    except (ValueError, TypeError) as exc:
        raise click.BadParameter(f"Invalid {parameter['name']}: {exc}") from exc
    if "enum" in spec and parsed not in spec["enum"]:
        raise click.BadParameter(f"{parameter['name']} must be one of {spec['enum']}")
    return parsed


async def invoke(ctx, operation_id, param, json_body, form, plugin_name=None, file=()):
    client = await discover(ctx)
    operation = client.operations.get(operation_id)
    if operation is None or (plugin_name and operation.plugin != plugin_name):
        raise NotFoundError(f"Unknown operation: {operation_id}")
    locations = operation_arguments(client.schema, operation, param)
    if file and json_body is not None:
        raise click.BadParameter("Choose --json or --file/--form.")
    body = request_body(operation, json_body, form or file)
    with ExitStack() as stack:
        files = {}
        for name, path in assignments(file).items():
            try:
                stream = stack.enter_context(Path(path).open("rb"))
                files[name] = (
                    Path(path).name,
                    stream,
                    mimetypes.guess_type(path)[0] or "application/octet-stream",
                )
            except OSError as exc:
                raise click.BadParameter(
                    f"Cannot read file '{path}': {exc}", param_hint="--file"
                ) from exc
        result = await client.async_call_operation(
            operation_id,
            path_params=locations["path"],
            query=locations["query"],
            headers=locations["header"],
            json_data=body,
            form_data=assignments(form) if form else None,
            authenticated=operation.requires_authentication,
            **({"files": files} if files else {}),
        )
    return emit(ctx, result)


def operation_arguments(schema, operation, param):
    values = assignments(param)
    locations: dict[str, dict[str, Any]] = {"path": {}, "query": {}, "header": {}}
    for parameter in operation.parameters:
        name, location = parameter["name"], parameter["in"]
        if name not in values:
            if parameter.get("required"):
                raise click.BadParameter(f"Missing required parameter: {name}")
            continue
        if location not in locations:
            raise InvalidInputError(
                f"Cookie parameter {name} is not supported by this command."
            )
        locations[location][name] = parameter_value(schema, parameter, values.pop(name))
    if values:
        raise click.BadParameter("Unknown parameters: " + ", ".join(sorted(values)))
    return locations


def request_body(operation, json_body, form):
    if json_body is not None and form:
        raise click.BadParameter("Choose --json or --form.")
    body = None
    if json_body is not None:
        try:
            body = json.loads(json_body)
        except ValueError as exc:
            raise click.BadParameter(f"Invalid JSON: {exc}") from exc
    if operation.request_body.get("required") and json_body is None and not form:
        raise click.BadParameter("This operation requires --json or --form.")
    return body


def call_options(fn):
    fn = click.option("--file", multiple=True, help="Multipart file FIELD=PATH.")(fn)
    fn = click.option("--form", multiple=True, help="Form field NAME=VALUE.")(fn)
    fn = click.option("--json", "json_body", help="JSON request body.")(fn)
    fn = click.option(
        "--param",
        multiple=True,
        shell_complete=complete_parameter,
        help="Path/query/header NAME=VALUE; arrays/objects use JSON.",
    )(fn)
    return click.argument("operation_id", shell_complete=complete_operation)(fn)


@click.group()
def api():
    """Inspect and call the server's OpenAPI contract."""


@api.command("info")
@pass_async_context
async def info(ctx):
    """Show server version, fingerprint, and capabilities."""
    client = await discover(ctx)
    return emit(
        ctx,
        {
            "info": client.schema.get("info", {}),
            "fingerprint": client.schema_fingerprint,
            "operations": len(client.operations),
            "plugins": sorted(client.plugins),
            "runtime_only": list(client.capabilities.runtime_only),
        },
    )


@api.command("schema")
@pass_async_context
async def schema(ctx):
    """Print the live OpenAPI document."""
    return emit(ctx, (await discover(ctx)).schema)


@api.command("operations")
@click.option("--tag", help="Filter by exact OpenAPI tag.")
@click.option(
    "--method",
    type=click.Choice(
        ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"],
        case_sensitive=False,
    ),
)
@click.option("--plugin", "plugin_name", shell_complete=complete_plugin)
@pass_async_context
async def operations(ctx, tag, method=None, plugin_name=None):
    """List HTTP operations advertised by the server."""
    client = await discover(ctx)
    rows = [
        op.to_dict()
        for op in sorted(client.operations.values(), key=lambda op: op.operation_id)
        if (not tag or tag in op.tags)
        and (not method or op.method == method.upper())
        and (not plugin_name or op.plugin == plugin_name)
    ]
    return emit(ctx, rows, columns=("method", "operation_id", "path"))


@api.command("operation")
@click.argument("operation_id", shell_complete=complete_operation)
@pass_async_context
async def operation(ctx, operation_id):
    """Inspect one operation and its request/response contract."""
    client = await discover(ctx)
    if operation_id not in client.operations:
        raise NotFoundError(f"Unknown operation: {operation_id}")
    return emit(ctx, client.operations[operation_id].to_dict())


@api.command("call")
@call_options
@pass_async_context
async def call(ctx, operation_id, param, json_body, form, file):
    """Invoke any advertised core or plugin HTTP operation."""
    return await invoke(ctx, operation_id, param, json_body, form, file=file)


@api.command("diff")
@click.option(
    "--against",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Compare against a saved OpenAPI JSON file.",
)
@click.option(
    "--against-generated",
    is_flag=True,
    help="Compare against this client build (default).",
)
@click.option(
    "--details",
    is_flag=True,
    help="Include conservative compatibility classifications.",
)
@pass_async_context
async def diff(ctx, against, against_generated, details=False):
    """Compare live operations against a saved or generated schema."""
    if against and against_generated:
        raise click.BadParameter("Choose --against or --against-generated.")
    try:
        baseline = json.loads(against.read_text(encoding="utf-8")) if against else None
    except (OSError, ValueError) as exc:
        raise click.BadParameter(
            "Cannot read a valid JSON schema.", param_hint="--against"
        ) from exc
    client = await discover(ctx)
    result = client.api_diff(baseline)
    if details:
        from bsm_api_client.openapi import compatibility_report, generated_schema

        result = {
            **result,
            "compatibility": compatibility_report(
                baseline if baseline is not None else generated_schema(), client.schema
            ),
        }
    return emit(ctx, result)


@api.command("refresh")
@pass_async_context
async def refresh(ctx):
    """Refresh discovery and cache offline shell completion."""
    client = get_client(ctx)
    config = ctx.obj.get("config")
    previous = cached_schema(ctx) if config else {}
    await discover(ctx, force=True)
    if config:
        config.set(
            "openapi_cache",
            {
                "base_url": config.base_url,
                "schema": client.schema,
                "fingerprint": client.schema_fingerprint,
                "username": config.username,
            },
        )
        if client.capabilities.has("list_servers"):
            names = await client.async_get_server_names()
            config.set(
                "server_cache", {"base_url": config.base_url, "names": sorted(names)}
            )
        else:
            config.set("server_cache", None)
    from bsm_api_client.openapi import diff_schemas

    return emit(
        ctx,
        {
            "fingerprint": client.schema_fingerprint,
            "diff": diff_schemas(
                previous,
                client.schema,
                generated_ids={
                    key for key, op in client.operations.items() if op.generated
                },
            ),
        },
    )


@api.command("export")
@click.argument("output", type=click.Path(dir_okay=False, path_type=Path))
@pass_async_context
async def export(ctx, output):
    """Save the live OpenAPI JSON document."""
    client = await discover(ctx)
    output.write_text(
        json.dumps(client.schema, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return emit(ctx, {"output": str(output), "fingerprint": client.schema_fingerprint})


@api.command("download")
@click.argument("operation_id", shell_complete=complete_operation)
@click.argument("output", type=click.Path(dir_okay=False, path_type=Path))
@click.option("--param", multiple=True, shell_complete=complete_parameter)
@pass_async_context
async def download(ctx, operation_id, output, param):
    """Stream a GET operation to a local file, publishing only complete downloads."""
    client = await discover(ctx)
    operation = client.operations.get(operation_id)
    if operation is None:
        raise NotFoundError(f"Unknown operation: {operation_id}")
    locations = operation_arguments(client.schema, operation, param)
    temporary = None
    size = 0
    try:
        async with client.async_stream_operation(
            operation_id,
            path_params=locations["path"],
            query=locations["query"],
            headers=locations["header"],
        ) as response:
            with tempfile.NamedTemporaryFile(
                dir=output.parent, prefix=".bsm-download-", delete=False
            ) as handle:
                temporary = Path(handle.name)
                async for chunk in response.content.iter_chunked(65536):
                    handle.write(chunk)
                    size += len(chunk)
            os.replace(temporary, output)
    except OSError as exc:
        raise click.BadParameter(
            "Cannot write the download destination.", param_hint="output"
        ) from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return emit(ctx, {"output": str(output), "bytes": size})


def register_plugin_commands(plugin):
    @plugin.command("operations")
    @click.argument("plugin_name", shell_complete=complete_plugin)
    @pass_async_context
    async def plugin_operations(ctx, plugin_name):
        client = await discover(ctx)
        if plugin_name not in client.plugins:
            raise NotFoundError(f"No discovered operations for plugin: {plugin_name}")
        return emit(
            ctx,
            [
                op.to_dict()
                for op in sorted(
                    client.plugins[plugin_name], key=lambda op: op.operation_id
                )
            ],
            columns=("method", "operation_id", "path"),
        )

    @plugin.command("call")
    @click.argument("plugin_name", shell_complete=complete_plugin)
    @call_options
    @pass_async_context
    async def plugin_call(ctx, plugin_name, operation_id, param, json_body, form, file):
        return await invoke(
            ctx,
            operation_id,
            param,
            json_body,
            form,
            plugin_name=plugin_name,
            file=file,
        )
