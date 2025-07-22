import click
import json
import questionary
from .decorators import pass_async_context, AsyncGroup
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
    max_version_len = max((max(len(v) for v in versions) if versions else 0), len("Version"))
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
            click.secho(f"Failed to retrieve plugin statuses: {response.message}", fg="red")
            return

        plugins = response.data
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

        choices = []
        for name, config_dict in sorted(plugins.items()):
            is_enabled = config_dict.get("enabled", False)
            version = config_dict.get("version", "N/A")
            choice_title = f"{name} (v{version})"
            choices.append(
                questionary.Choice(title=choice_title, value=name, checked=is_enabled)
            )

        selected_plugin_names_list = await questionary.checkbox(
            "Toggle plugins (space to select/deselect, enter to confirm):",
            choices=choices,
        ).ask_async()

        if selected_plugin_names_list is None:
            click.secho("\nOperation cancelled by user.", fg="yellow")
            return

        final_enabled_plugins = set(selected_plugin_names_list)
        plugins_to_enable = sorted(list(final_enabled_plugins - initial_enabled_plugins))
        plugins_to_disable = sorted(list(initial_enabled_plugins - final_enabled_plugins))

        if not plugins_to_enable and not plugins_to_disable:
            click.secho("\nNo changes made to plugin statuses.", fg="cyan")
            return

        click.echo("\nApplying changes...")
        changes_made_successfully = False
        for name in plugins_to_enable:
            click.echo(f"Enabling plugin '{name}'... ", nl=False)
            payload = PluginStatusSetPayload(enabled=True)
            api_response = await client.async_set_plugin_status(name, payload)
            if api_response.status == "success":
                click.secho("OK", fg="green")
                changes_made_successfully = True
            else:
                error_msg = api_response.message
                click.secho(f"Failed: {error_msg}", fg="red")

        for name in plugins_to_disable:
            click.echo(f"Disabling plugin '{name}'... ", nl=False)
            payload = PluginStatusSetPayload(enabled=False)
            api_response = await client.async_set_plugin_status(name, payload)
            if api_response.status == "success":
                click.secho("OK", fg="green")
                changes_made_successfully = True
            else:
                error_msg = api_response.message
                click.secho(f"Failed: {error_msg}", fg="red")

        if changes_made_successfully:
            click.secho("\nPlugin configuration updated.", fg="green")
            try:
                click.secho("Reloading plugins...", fg="cyan")
                reload_response = await client.async_reload_plugins()
                if reload_response.status == "success":
                    click.secho(reload_response.message, fg="green")
                else:
                    click.secho(f"Failed to reload plugins: {reload_response.message}", fg="red")
            except Exception as e_reload:
                click.secho(f"\nError reloading plugins: {e_reload}", fg="red")
        else:
            click.secho("\nNo changes were successfully applied to plugin statuses.", fg="yellow")

        click.echo("\nFetching updated plugin statuses...")
        final_response = await client.async_get_plugin_statuses()
        if final_response.status == "success":
            _print_plugin_table(final_response.data)
        else:
            click.secho("Could not retrieve final plugin statuses after update.", fg="red")

    except Exception as e:
        click.secho(f"An error occurred during plugin configuration: {e}", fg="red")

@click.group(cls=AsyncGroup, invoke_without_command=True)
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
@pass_async_context
async def list_plugins(ctx):
    """Lists all discoverable plugins."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        response = await client.async_get_plugin_statuses()
        if response.status == "success":
            plugins = response.data
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
@pass_async_context
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
@pass_async_context
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
@pass_async_context
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
@click.option("--payload-json", help="Optional JSON string to use as the event payload.")
@pass_async_context
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
