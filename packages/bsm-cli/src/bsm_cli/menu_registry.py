"""Interactive command browsing from Click's registry and API capabilities."""

import inspect
import json

import click
import questionary

from bsm_cli.api import invoke
from bsm_cli.interaction import menu_action
from bsm_cli.output import get_client
from bsm_cli.presentation import screen_header


async def command_menu(ctx, group, *, values=None):  # noqa: C901
    """Browse commands as a persistent interactive management menu."""
    resource_values = dict(values or {})
    while True:
        screen_header(group.name.replace("-", " ").title())
        if not await _show_menu_list(ctx, group, resource_values):
            return
        name = await questionary.select(
            group.help or group.name,
            choices=_command_choices(group),
        ).ask_async()
        if not name or name == "Back":
            return
        command = group.commands[name]
        if isinstance(command, click.Group):
            await command_menu(ctx, command, values=resource_values)
            continue
        kwargs = {}
        cancelled = False
        for param in command.params:
            if param.name in resource_values:
                kwargs[param.name] = resource_values[param.name]
                continue
            value = await _prompt_parameter(ctx, param)
            if value is _CANCEL:
                cancelled = True
                break
            if value is not _DEFAULT:
                kwargs[param.name] = value
        if cancelled:
            continue
        try:
            result = ctx.invoke(command, **kwargs)
            if inspect.isawaitable(result):
                await menu_action(result)
        except (click.Abort, KeyboardInterrupt):
            click.secho("Action cancelled.", fg="yellow")
        except Exception as exc:
            click.secho(f"Action failed: {exc}", fg="red")
        click.pause("Press any key to return to the menu...")


def _command_choices(group):
    sections = {"View and inspect": [], "Manage": [], "Advanced": []}
    for name in group.commands:
        if name == "list":
            continue
        if name in {
            "show",
            "get",
            "details",
            "info",
            "operations",
            "operation",
            "schema",
            "diff",
            "scan",
            "export",
            "download",
        }:
            section = "View and inspect"
        elif name in {"call", "trigger-event", "refresh"}:
            section = "Advanced"
        else:
            section = "Manage"
        sections[section].append(
            questionary.Choice(name.replace("-", " ").capitalize(), value=name)
        )
    choices = []
    for title, items in sections.items():
        if items:
            choices.extend([questionary.Separator(f"── {title} ──"), *items])
    return [*choices, questionary.Separator(), "Back"]


async def _show_menu_list(ctx, group, resource_values):
    command = group.commands.get("list")
    if command is None or isinstance(command, click.Group):
        return True
    kwargs = {}
    for param in command.params:
        if not param.required:
            continue
        if param.name not in resource_values:
            value = await _prompt_parameter(ctx, param)
            if value is _CANCEL:
                return False
            resource_values[param.name] = value
        kwargs[param.name] = resource_values[param.name]
    try:
        result = ctx.invoke(command, **kwargs)
        if inspect.isawaitable(result):
            await menu_action(result)
    except (click.Abort, KeyboardInterrupt):
        return False
    except Exception as exc:
        click.secho(f"List unavailable: {exc}", fg="yellow")
    return True


_CANCEL = object()
_DEFAULT = object()


def _multiple_values(param, value):
    try:
        values = json.loads(value) if value.lstrip().startswith("[") else [value]
    except ValueError as exc:
        raise click.BadParameter("Expected a JSON array.", param=param) from exc
    if not isinstance(values, list):
        raise click.BadParameter("Expected a JSON array.", param=param)
    return values


async def _resource_choices(ctx, name):
    """Fetch selectable resources for the interactive UI."""
    client = get_client(ctx)
    if name == "operation_id":
        await client.async_discover_api()
        return [
            questionary.Choice(
                title=f"{op.method} {op.operation_id} · {op.summary or op.path}",
                value=op.operation_id,
            )
            for op in sorted(client.operations.values(), key=lambda op: op.operation_id)
        ]
    if name in {"server", "server_name"}:
        response = await client.async_get_servers()
        return sorted(server.name for server in (response.servers or []))
    if name in {"plugin_name", "plugin"}:
        response = await client.async_get_plugin_statuses()
        plugins = response.plugins or {}
        return [
            questionary.Choice(
                title=f"{'Enabled' if data.get('enabled') else 'Disabled'} · {plugin}",
                value=plugin,
            )
            for plugin, data in sorted(plugins.items())
        ]
    return []


async def _prompt_parameter(ctx, param):  # noqa: C901
    prompt = param.name.replace("_", " ")
    multiple = getattr(param, "multiple", False) or param.nargs == -1
    if multiple:
        prompt += " (one value or a JSON array)"
    prompt += " (blank for default):" if not param.required else ":"
    if isinstance(param, click.Option) and param.is_flag:
        answer = await questionary.confirm(
            prompt, default=bool(param.get_default(ctx))
        ).ask_async()
        return _CANCEL if answer is None else answer
    if not multiple and not getattr(param, "hide_input", False):
        try:
            choices = await _resource_choices(ctx, param.name)
        except Exception as exc:
            click.secho(f"Resource lookup unavailable: {exc}", fg="yellow")
            choices = []
        if choices:
            if not param.required:
                choices = [
                    questionary.Choice(title="Use default", value=_DEFAULT),
                    *choices,
                ]
            selection = await questionary.select(prompt, choices=choices).ask_async()
            if selection is None:
                return _CANCEL
            if selection is _DEFAULT:
                return _DEFAULT
            return param.process_value(ctx, selection)
    ask = (
        questionary.password
        if getattr(param, "hide_input", False)
        else questionary.text
    )
    value = await ask(prompt).ask_async()
    if value is None:
        return _CANCEL
    if not value and not param.required:
        # Let Context.invoke resolve defaults and hide Click's internal UNSET.
        return _DEFAULT
    if getattr(param, "confirmation_prompt", False):
        confirmation = await ask(
            "Confirm " + param.name.replace("_", " ") + ":"
        ).ask_async()
        if confirmation is None:
            return _CANCEL
        if confirmation != value:
            raise click.BadParameter("Confirmation does not match.", param=param)
    converted = _multiple_values(param, value) if multiple else value
    if multiple:
        converted = tuple(converted)
    return param.process_value(ctx, converted)


async def plugin_api_menu(ctx):  # noqa: C901
    """Show only plugin operations actually advertised by this server."""
    screen_header("Plugin API")
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
        name = parameter["name"]
        try:
            choices = await _resource_choices(ctx, name)
        except Exception:
            choices = []
        if choices:
            choices = [
                *choices,
                questionary.Choice("Enter manually", value="__manual__"),
            ]
            value = await questionary.select(f"{name}:", choices=choices).ask_async()
            if value == "__manual__":
                value = await questionary.text(f"{name}:").ask_async()
        else:
            value = await questionary.text(
                f"{name} ({parameter['in']}, {'required' if parameter.get('required') else 'optional'}):"
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
