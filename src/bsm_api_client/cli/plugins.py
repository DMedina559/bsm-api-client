import click
import json
import questionary
from bsm_api_client.models import PluginStatusSetPayload, TriggerEventPayload


def _print_plugin_table(plugins):
    """
    Internal helper to print a formatted table of plugins, their statuses, and versions.
    """
    if not plugins:
        click.secho("No plugins found or configured.", fg="yellow")
        return

    click.secho("BSM API Client - Plugin Statuses & Versions", fg="magenta", bold=True)

    plugin_names = list(plugins.keys())
    versions = [config.get("version", "N/A") for config in plugins.values()]

    max_name_len = max(len(name) for name in plugin_names) if plugin_names else 20
    max_version_len = max(
        (max(len(v) for v in versions) if versions else 0), len("Version")
    )
    max_status_len = len("Disabled")

    header = f"{'Plugin Name':<{max_name_len}} | {'Status':<{max_status_len}} | {'Version':<{max_version_len}}"
    click.secho(header, underline=True)
    click.secho("-" * len(header))

    for name, config in sorted(plugins.items()):
        is_enabled = config.get("enabled", False)
        version = config.get("version", "N/A")

        status_str = "Enabled" if is_enabled else "Disabled"
        status_color = "green" if is_enabled else "red"

        click.echo(f"{name:<{max_name_len}} | ", nl=False)
        click.secho(f"{status_str:<{max_status_len}}", fg=status_color, nl=False)
        click.echo(f" | {version:<{max_version_len}}")


async def interactive_plugin_workflow(client):
    """Guides the user through an interactive session to enable or disable plugins."""
    try:
        response = await client.async_get_plugin_statuses()
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

        initial_enabled_plugins = {
            name
            for name, config_dict in plugins.items()
            if config_dict.get("enabled", False)
        }

        while True:
            click.clear()
            click.secho("--- Manage Plugins ---", fg="magenta", bold=True)
            
            response = await client.async_get_plugin_statuses()
            if response.status != "success":
                click.secho(f"Failed to retrieve plugin statuses: {response.message}", fg="red")
                return
            
            plugins = response.plugins
            if not plugins:
                click.secho("No plugins found or configured to edit.", fg="yellow")
                return

            menu_choices = []
            for name, config_dict in sorted(plugins.items()):
                is_enabled = config_dict.get("enabled", False)
                version = config_dict.get("version", "N/A")
                status = "🟢" if is_enabled else "⚪"
                menu_choices.append(
                    questionary.Choice(title=f"{status} {name} (v{version})", value=name)
                )
                
            menu_choices.extend([
                questionary.Separator("--- Actions ---"),
                questionary.Choice(title="Reload All Plugins", value="RELOAD"),
                questionary.Choice(title="Back", value="BACK")
            ])
            
            choice = await questionary.select(
                "Select a plugin to manage or an action:",
                choices=menu_choices
            ).ask_async()
            
            if not choice or choice == "BACK":
                return
                
            if choice == "RELOAD":
                click.secho("Reloading plugins...", fg="cyan")
                try:
                    reload_response = await client.async_reload_plugins()
                    if reload_response.status == "success":
                        click.secho(reload_response.message, fg="green")
                    else:
                        click.secho(f"Failed to reload plugins: {reload_response.message}", fg="red")
                except Exception as e_reload:
                    click.secho(f"Error reloading plugins: {e_reload}", fg="red")
                click.pause()
                continue
                
            # Handle specific plugin
            plugin_name = choice
            config_dict = plugins.get(plugin_name)
            
            if not config_dict:
                continue
                
            is_enabled = config_dict.get("enabled", False)
            pack_menu = []
            if is_enabled:
                pack_menu.append("Disable")
            else:
                pack_menu.append("Enable")
                
            pack_menu.append("Back")
            
            action_choice = await questionary.select(
                f"Actions for {plugin_name}:",
                choices=pack_menu
            ).ask_async()
            
            if not action_choice or action_choice == "Back":
                continue
                
            if action_choice == "Enable":
                payload = PluginStatusSetPayload(enabled=True)
                res = await client.async_set_plugin_status(plugin_name, payload)
                if res.status == "success":
                    click.secho(f"Plugin '{plugin_name}' enabled successfully.", fg="green")
                else:
                    click.secho(f"Failed to enable plugin '{plugin_name}': {res.message}", fg="red")
            elif action_choice == "Disable":
                payload = PluginStatusSetPayload(enabled=False)
                res = await client.async_set_plugin_status(plugin_name, payload)
                if res.status == "success":
                    click.secho(f"Plugin '{plugin_name}' disabled successfully.", fg="green")
                else:
                    click.secho(f"Failed to disable plugin '{plugin_name}': {res.message}", fg="red")
            
            click.pause()

    except Exception as e:
        click.secho(f"An error occurred during plugin configuration: {e}", fg="red")


@click.group(invoke_without_command=True)
@click.pass_context
async def plugin(ctx):
    """Manages plugins."""
    if ctx.invoked_subcommand is None:
        client = ctx.obj.get("client")
        if not client:
            click.secho("You are not logged in.", fg="red")
            return
        await interactive_plugin_workflow(client)


@plugin.command("list")
@click.pass_context
async def list_plugins(ctx):
    """Lists all discoverable plugins."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        response = await client.async_get_plugin_statuses()
        if response.status == "success":
            plugins = response.plugins
            if not plugins:
                click.secho("No plugins found.", fg="yellow")
                return

            _print_plugin_table(plugins)
        else:
            click.secho(f"Failed to list plugins: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@plugin.command("enable")
@click.argument("plugin_name")
@click.pass_context
async def enable_plugin(ctx, plugin_name: str):
    """Enables a plugin."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        payload = PluginStatusSetPayload(enabled=True)
        response = await client.async_set_plugin_status(plugin_name, payload)
        if response.status == "success":
            click.secho(f"Plugin '{plugin_name}' enabled successfully.", fg="green")
        else:
            click.secho(f"Failed to enable plugin: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@plugin.command("disable")
@click.argument("plugin_name")
@click.pass_context
async def disable_plugin(ctx, plugin_name: str):
    """Disables a plugin."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        payload = PluginStatusSetPayload(enabled=False)
        response = await client.async_set_plugin_status(plugin_name, payload)
        if response.status == "success":
            click.secho(f"Plugin '{plugin_name}' disabled successfully.", fg="green")
        else:
            click.secho(f"Failed to disable plugin: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@plugin.command("reload")
@click.pass_context
async def reload_plugins(ctx):
    """Reloads all plugins."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        response = await client.async_reload_plugins()
        if response.status == "success":
            click.secho("Plugins reloaded successfully.", fg="green")
        else:
            click.secho(f"Failed to reload plugins: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@plugin.command("trigger-event")
@click.argument("event_name")
@click.option(
    "--payload-json", help="Optional JSON string to use as the event payload."
)
@click.pass_context
async def trigger_event(ctx, event_name: str, payload_json: str):
    """Triggers a custom plugin event."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        payload = None
        if payload_json:
            payload = json.loads(payload_json)

        event_payload = TriggerEventPayload(event_name=event_name, payload=payload)
        response = await client.async_trigger_plugin_event(event_payload)
        if response.status == "success":
            click.secho(f"Event '{event_name}' triggered successfully.", fg="green")
        else:
            click.secho(f"Failed to trigger event: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")
