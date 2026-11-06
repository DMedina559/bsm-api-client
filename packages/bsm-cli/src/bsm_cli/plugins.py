import json

import click
import questionary

from bsm_api_client.models import (
    PluginSettingsPayload,
    PluginStatusSetPayload,
)
from bsm_cli.output import fail, get_client
from bsm_cli.presentation import screen_header
from bsm_cli.settings_editor import edit_settings


def _print_plugin_table(plugins):
    """
    Internal helper to print a formatted table of plugins, their statuses, and versions.
    """
    if not plugins:
        click.secho("No plugins found or configured.", fg="yellow")
        return

    click.secho("BSM API Client - Plugin Statuses & Versions", fg="magenta", bold=True)

    rows = []
    for name, config in sorted(plugins.items()):
        rows.append(
            (
                name,
                "Enabled" if config.get("enabled", False) else "Disabled",
                config.get("status") or "UNKNOWN",
                config.get("version") or "N/A",
                ", ".join(config.get("permissions") or []) or "None",
            )
        )
    headings = (
        "Plugin Name",
        "Configured",
        "Runtime",
        "Version",
        "Declared Permissions",
    )
    widths = [
        max(len(row[i]) for row in [headings, *rows]) for i in range(len(headings))
    ]
    click.echo(" | ".join(value.ljust(width) for value, width in zip(headings, widths)))
    for row in rows:
        click.echo(" | ".join(value.ljust(width) for value, width in zip(row, widths)))


async def interactive_plugin_workflow(client):  # noqa: C901
    """Guides the user through an interactive session to enable or disable plugins."""
    try:
        response = await client.plugins.async_get_plugin_statuses()
        if response.status != "success":
            click.secho(
                f"Failed to retrieve plugin statuses: {response.message}", fg="red"
            )
            return

        plugins = response.plugins
        if not plugins:
            click.secho("No plugins found or configured to edit.", fg="yellow")
            return

        _print_plugin_table(plugins)
        click.echo()

        while True:
            screen_header("Plugins")
            click.secho("--- Manage Plugins ---", fg="magenta", bold=True)

            response = await client.plugins.async_get_plugin_statuses()
            if response.status != "success":
                click.secho(
                    f"Failed to retrieve plugin statuses: {response.message}", fg="red"
                )
                return

            plugins = response.plugins
            if not plugins:
                click.secho("No plugins found or configured to edit.", fg="yellow")
                return

            _print_plugin_table(plugins)
            click.echo()
            menu_choices = []
            for name, config_dict in sorted(plugins.items()):
                is_enabled = config_dict.get("enabled", False)
                version = config_dict.get("version", "N/A")
                status = "🟢" if is_enabled else "⚪"
                menu_choices.append(
                    questionary.Choice(
                        title=f"{status} {name} (v{version}) · {config_dict.get('status') or 'UNKNOWN'}",
                        value=name,
                    )
                )

            menu_choices.extend(
                [
                    questionary.Separator("--- Actions ---"),
                    questionary.Choice(title="Reload All Plugins", value="RELOAD"),
                    questionary.Choice(title="Back", value="BACK"),
                ]
            )

            choice = await questionary.select(
                "Select a plugin to manage or an action:", choices=menu_choices
            ).ask_async()

            if not choice or choice == "BACK":
                return

            if choice == "RELOAD":
                click.secho("Reloading plugins...", fg="cyan")
                try:
                    reload_response = await client.plugins.async_reload_plugins()
                    if reload_response.status == "success":
                        click.secho(reload_response.message, fg="green")
                    else:
                        click.secho(
                            f"Failed to reload plugins: {reload_response.message}",
                            fg="red",
                        )
                except Exception as e_reload:
                    fail(e_reload)
                click.pause()
                continue

            # Handle specific plugin
            plugin_name = choice
            config_dict = plugins.get(plugin_name)

            if not config_dict:
                continue

            click.echo(f"Runtime: {config_dict.get('status') or 'UNKNOWN'}")
            click.echo(
                "Declared permissions: "
                + (", ".join(config_dict.get("permissions") or []) or "None")
            )
            scopes = [
                label
                for field, label in (
                    ("has_settings", "Plugin"),
                    ("has_global_settings", "Global"),
                    ("has_server_settings", "Server"),
                )
                if config_dict.get(field)
            ]
            click.echo("Settings scopes: " + (", ".join(scopes) or "None"))
            is_enabled = config_dict.get("enabled", False)
            pack_menu = []
            if is_enabled:
                pack_menu.append("Disable")
            else:
                pack_menu.append("Enable")

            if config_dict.get("has_settings", False):
                pack_menu.append("Settings")
            pack_menu.append("Back")

            action_choice = await questionary.select(
                f"Actions for {plugin_name}:", choices=pack_menu
            ).ask_async()

            if not action_choice or action_choice == "Back":
                continue

            if action_choice == "Settings":
                await edit_plugin_settings(client, plugin_name)
            elif action_choice == "Enable":
                payload = PluginStatusSetPayload(enabled=True)
                res = await client.plugins.async_set_plugin_status(plugin_name, payload)
                if res.status == "success":
                    click.secho(
                        f"Plugin '{plugin_name}' enabled successfully.", fg="green"
                    )
                else:
                    click.secho(
                        f"Failed to enable plugin '{plugin_name}': {res.message}",
                        fg="red",
                    )
            elif action_choice == "Disable":
                payload = PluginStatusSetPayload(enabled=False)
                res = await client.plugins.async_set_plugin_status(plugin_name, payload)
                if res.status == "success":
                    click.secho(
                        f"Plugin '{plugin_name}' disabled successfully.", fg="green"
                    )
                else:
                    click.secho(
                        f"Failed to disable plugin '{plugin_name}': {res.message}",
                        fg="red",
                    )

            click.pause()

    except Exception as e:
        fail(e)


@click.group(invoke_without_command=True)
@click.pass_context
def plugin(ctx):
    """Manages plugins."""
    if ctx.invoked_subcommand is None:
        if ctx.obj.get("json_output"):
            raise click.UsageError("Choose a subcommand with --json.")
        return interactive_plugin_workflow(get_client(ctx))


@plugin.command("list")
@click.pass_context
async def list_plugins(ctx):
    """Lists all discoverable plugins."""
    client = get_client(ctx)

    try:
        response = await client.plugins.async_get_plugin_statuses()
        if response.status == "success":
            plugins = response.plugins
            if not plugins:
                click.secho("No plugins found.", fg="yellow")
                return

            _print_plugin_table(plugins)
        else:
            click.secho(f"Failed to list plugins: {response.message}", fg="red")
    except Exception as e:
        fail(e)


@plugin.command("enable")
@click.argument("plugin_name")
@click.pass_context
async def enable_plugin(ctx, plugin_name: str):
    """Enables a plugin."""
    client = get_client(ctx)

    try:
        payload = PluginStatusSetPayload(enabled=True)
        response = await client.plugins.async_set_plugin_status(plugin_name, payload)
        if response.status == "success":
            click.secho(f"Plugin '{plugin_name}' enabled successfully.", fg="green")
        else:
            click.secho(f"Failed to enable plugin: {response.message}", fg="red")
    except Exception as e:
        fail(e)


@plugin.command("disable")
@click.argument("plugin_name")
@click.pass_context
async def disable_plugin(ctx, plugin_name: str):
    """Disables a plugin."""
    client = get_client(ctx)

    try:
        payload = PluginStatusSetPayload(enabled=False)
        response = await client.plugins.async_set_plugin_status(plugin_name, payload)
        if response.status == "success":
            click.secho(f"Plugin '{plugin_name}' disabled successfully.", fg="green")
        else:
            click.secho(f"Failed to disable plugin: {response.message}", fg="red")
    except Exception as e:
        fail(e)


@plugin.command("reload")
@click.pass_context
async def reload_plugins(ctx):
    """Reloads all plugins."""
    client = get_client(ctx)

    try:
        response = await client.plugins.async_reload_plugins()
        if response.status == "success":
            click.secho("Plugins reloaded successfully.", fg="green")
        else:
            click.secho(f"Failed to reload plugins: {response.message}", fg="red")
    except Exception as e:
        fail(e)


def scoped_options(scope, server_name):
    if (scope == "server") != (server_name is not None):
        raise click.UsageError(
            "Server scope requires --server; other scopes must omit it"
        )
    if scope == "plugin":
        return {}
    return {"scope": scope, **({"server_name": server_name} if server_name else {})}


async def edit_plugin_settings(
    client, plugin_name, *, scope="plugin", server_name=None
):
    options = scoped_options(scope, server_name)
    response = await client.plugins.async_get_plugin_settings(plugin_name, **options)
    original = response.settings
    draft = await edit_settings(original, response.settings_schema)
    if draft is None:
        return
    latest = await client.plugins.async_get_plugin_settings(plugin_name, **options)
    if latest.settings != original:
        raise click.ClickException(
            "Settings changed in another session. Reopen the editor to review the current values."
        )
    result = await client.plugins.async_update_plugin_settings(
        plugin_name, PluginSettingsPayload(settings=draft, **options)
    )
    click.echo(result.message)


@plugin.group("settings")
def plugin_settings():
    """View or edit settings for a plugin, including disabled plugins."""


@plugin_settings.command("show")
@click.argument("plugin_name")
@click.option(
    "--scope",
    type=click.Choice(["plugin", "global", "server"]),
    default="plugin",
    show_default=True,
)
@click.option("--server", "server_name", help="Server for server-scoped settings.")
@click.pass_context
async def show_settings(ctx, plugin_name, scope, server_name):
    response = await get_client(ctx).plugins.async_get_plugin_settings(
        plugin_name, **scoped_options(scope, server_name)
    )
    # The interactive editor masks credential fields; JSON is an explicit export.
    from bsm_cli.settings_editor import display, fields

    schema = response.settings_schema
    if schema:
        for path, spec, value in fields(schema, schema, response.settings):
            click.echo(f"{'.'.join(path)}: {display(value, path, spec)}")
    else:
        click.echo("Use settings edit to inspect and configure these settings.")


@plugin_settings.command("edit")
@click.argument("plugin_name")
@click.option(
    "--scope",
    type=click.Choice(["plugin", "global", "server"]),
    default="plugin",
    show_default=True,
)
@click.option("--server", "server_name", help="Server for server-scoped settings.")
@click.pass_context
async def configure_settings(ctx, plugin_name, scope, server_name):
    if ctx.obj.get("json_output"):
        raise click.UsageError("Use settings set with --json.")
    await edit_plugin_settings(
        get_client(ctx), plugin_name, scope=scope, server_name=server_name
    )


@plugin_settings.command("set")
@click.argument("plugin_name")
@click.argument("settings_file", type=click.File("r"))
@click.option(
    "--scope",
    type=click.Choice(["plugin", "global", "server"]),
    default="plugin",
    show_default=True,
)
@click.option("--server", "server_name", help="Server for server-scoped settings.")
@click.pass_context
async def set_settings(ctx, plugin_name, settings_file, scope, server_name):
    """Replace settings from a JSON object file."""
    values = json.load(settings_file)
    response = await get_client(ctx).plugins.async_update_plugin_settings(
        plugin_name,
        PluginSettingsPayload(settings=values, **scoped_options(scope, server_name)),
    )
    click.echo(response.message)
