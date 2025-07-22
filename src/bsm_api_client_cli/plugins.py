import click
import json
from .decorators import pass_async_context
from bsm_api_client.models import PluginStatusSetPayload, TriggerEventPayload

@click.group(invoke_without_command=True)
@click.pass_context
def plugin(ctx):
    """Manages plugins."""
    if ctx.invoked_subcommand is None:
        click.echo("use one of the subcommands: list, enable, disable, reload, trigger-event")

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
            plugins = response.plugins
            if not plugins:
                click.secho("No plugins found.", fg="yellow")
                return
            
            for plugin_name, plugin_data in plugins.items():
                status = "enabled" if plugin_data["enabled"] else "disabled"
                version = plugin_data["version"]
                click.echo(f"- {plugin_name} (v{version}): {status}")
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
