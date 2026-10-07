"""Interactive command browsing from Click's registry and API capabilities."""

import inspect
import json

import click
import questionary
from bsm_cli.api import invoke
from bsm_cli.output import get_client


async def command_menu(ctx, group):
    """Browse a registered command group without maintaining a feature list."""
    name = await questionary.select(
        group.help or group.name, choices=[*sorted(group.commands), "Back"]
    ).ask_async()
    if not name or name == "Back":
        return
    command = group.commands[name]
    if isinstance(command, click.Group):
        return await command_menu(ctx, command)
    kwargs = {}
    for param in command.params:
        # process_value applies Click's missing/default handling, including UNSET.
        default = (
            param.process_value(ctx, param.get_default(ctx))
            if not param.required
            else None
        )
        if (
            param.required
            or getattr(param, "prompt", None)
            or isinstance(param, click.Option)
        ):
            value = await questionary.text(
                param.name.replace("_", " ")
                + (" (blank for default):" if not param.required else ":")
            ).ask_async()
            if value is None:
                return
            if not value and not param.required:
                kwargs[param.name] = default
                continue
            kwargs[param.name] = param.type_cast_value(
                ctx,
                (
                    value.split()
                    if param.nargs == -1 or getattr(param, "multiple", False)
                    else value
                ),
            )
        else:
            kwargs[param.name] = default
    result = ctx.invoke(command, **kwargs)
    if inspect.isawaitable(result):
        await result


async def plugin_api_menu(ctx):
    """Show only plugin operations actually advertised by this server."""
    client = get_client(ctx)
    await client.async_discover_api()
    plugin = await questionary.select(
        "Plugin API:", choices=[*sorted(client.plugins), "Back"]
    ).ask_async()
    if not plugin or plugin == "Back":
        return
    identifier = await questionary.select(
        "Operation:",
        choices=[op.operation_id for op in client.plugins[plugin]] + ["Back"],
    ).ask_async()
    if not identifier or identifier == "Back":
        return
    op = client.operations[identifier]
    values = []
    for parameter in op.parameters:
        value = await questionary.text(
            f"{parameter['name']} ({parameter['in']}, {'required' if parameter.get('required') else 'optional'}):"
        ).ask_async()
        if value is None:
            return
        if value:
            values.append(f"{parameter['name']}={value}")
    body = None
    if op.request_body:
        body = await questionary.text("Request body (JSON; blank to omit):").ask_async()
        if body is None:
            return
        body = body or None
        if body:
            json.loads(body)
    await invoke(ctx, identifier, values, body, (), plugin_name=plugin)
