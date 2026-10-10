"""Offline shell completion scoped to the selected BSM server."""

from collections.abc import Mapping

from click.shell_completion import CompletionItem


# Completion reads only a locally cached schema; no network or auth on Tab.
def cached_schema(ctx):
    config = (ctx.obj or {}).get("config")
    if config is None:
        from bsm_cli.config import Config

        config = Config()
    cached = config.get("openapi_cache", {})
    if not isinstance(cached, Mapping) or cached.get("base_url") != config.base_url:
        return {}
    if "username" in cached and cached["username"] != config.username:
        return {}
    schema = cached.get("schema")
    if not isinstance(schema, Mapping):
        return {}
    from bsm_api_client.exceptions import InvalidInputError
    from bsm_api_client.openapi import index_operations, schema_fingerprint

    try:
        index_operations(schema)
        fingerprint = cached.get("fingerprint")
        if fingerprint is not None and fingerprint != schema_fingerprint(schema):
            return {}
    except (InvalidInputError, TypeError, ValueError, KeyError, AttributeError):
        return {}
    return schema


def complete_operation(ctx, param, incomplete):
    from bsm_api_client.openapi import index_operations

    plugin_name = ctx.params.get("plugin_name")
    return [
        CompletionItem(op.operation_id, help=op.summary)
        for op in index_operations(cached_schema(ctx) or {"paths": {}}).values()
        if op.operation_id.startswith(incomplete)
        and (not plugin_name or op.plugin == plugin_name)
    ]


def complete_plugin(ctx, param, incomplete):
    from bsm_api_client.openapi import ApiCapabilities, index_operations

    return [
        name
        for name in ApiCapabilities(
            index_operations(cached_schema(ctx) or {"paths": {}})
        ).plugins
        if name.startswith(incomplete)
    ]


def complete_parameter(ctx, param, incomplete):
    from bsm_api_client.openapi import index_operations

    schema = cached_schema(ctx)
    operation = index_operations(schema or {"paths": {}}).get(
        ctx.params.get("operation_id")
    )
    if operation is None:
        return []
    if "=" in incomplete:
        from bsm_api_client.openapi import resolve

        name, prefix = incomplete.split("=", 1)
        parameter = next((p for p in operation.parameters if p["name"] == name), None)
        if parameter is None:
            return []
        spec = resolve(schema, parameter.get("schema", {}))
        values = spec.get(
            "enum", [True, False] if spec.get("type") == "boolean" else []
        )
        return [
            (
                name + "=" + str(value).lower()
                if isinstance(value, bool)
                else name + "=" + str(value)
            )
            for value in values
            if str(value).lower().startswith(prefix.lower())
        ]
    return [
        p["name"] + "="
        for p in operation.parameters
        if (p["name"] + "=").startswith(incomplete)
    ]


def complete_server(ctx, param, incomplete):
    config = (ctx.obj or {}).get("config")
    if config is None:
        from bsm_cli.config import Config

        config = Config()
    cache = config.get("server_cache", {})
    if not isinstance(cache, Mapping) or cache.get("base_url") != config.base_url:
        return []
    names = cache.get("names")
    if not isinstance(names, list):
        return []
    return [
        name for name in names if isinstance(name, str) and name.startswith(incomplete)
    ]
