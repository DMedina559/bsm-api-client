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
        value = await _prompt_parameter(ctx, param)
        if value is _CANCEL:
            return
        kwargs[param.name] = value
    result = ctx.invoke(command, **kwargs)
    if inspect.isawaitable(result):
        await result


_CANCEL = object()


def _multiple_values(param, value):
    try:
        values = json.loads(value) if value.lstrip().startswith("[") else [value]
    except ValueError as exc:
        raise click.BadParameter("Expected a JSON array.", param=param) from exc
    if not isinstance(values, list):
        raise click.BadParameter("Expected a JSON array.", param=param)
    return values


async def _prompt_parameter(ctx, param):
    prompt = param.name.replace("_", " ")
    multiple = getattr(param, "multiple", False) or param.nargs == -1
    if multiple:
        prompt += " (one value or a JSON array)"
    prompt += " (blank for default):" if not param.required else ":"
    ask = (
        questionary.password
        if getattr(param, "hide_input", False)
        else questionary.text
    )
    value = await ask(prompt).ask_async()
    if value is None:
        return _CANCEL
    if not value and not param.required:
        return param.process_value(ctx, param.get_default(ctx))
    if getattr(param, "confirmation_prompt", False):
        confirmation = await ask(
            "Confirm " + param.name.replace("_", " ") + ":"
        ).ask_async()
        if confirmation is None:
            return _CANCEL
        if confirmation != value:
            raise click.BadParameter("Confirmation does not match.", param=param)
    return param.process_value(
        ctx, _multiple_values(param, value) if multiple else value
    )


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
