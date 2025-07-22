import click
import questionary
from .decorators import pass_async_context
from bsm_api_client.models import InstallServerPayload, CommandPayload

@click.group()
def server():
    """Manages servers."""
    pass

@server.command("list")
@pass_async_context
async def list_servers(ctx):
    """Lists all servers."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        response = await client.async_get_servers_details()
        if response.servers:
            for server in response.servers:
                click.echo(f"- {server['name']}: {server['status']}")
        else:
            click.echo("No servers found.")
    except Exception as e:
        click.secho(f"Failed to list servers: {e}", fg="red")

@server.command("start")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server to start.")
@pass_async_context
async def start_server(ctx, server_name: str):
    """Starts a specific Bedrock server instance."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.echo(f"Attempting to start server '{server_name}'...")
    try:
        response = await client.async_start_server(server_name)
        if response.status == "success":
            click.secho(f"Server '{server_name}' started successfully.", fg="green")
        else:
            click.secho(f"Failed to start server: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"Failed to start server: {e}", fg="red")

@server.command("stop")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server to stop.")
@pass_async_context
async def stop_server(ctx, server_name: str):
    """Sends a graceful stop command to a running Bedrock server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.echo(f"Attempting to stop server '{server_name}'...")
    try:
        response = await client.async_stop_server(server_name)
        if response.status == "success":
            click.secho(f"Stop signal sent to server '{server_name}'.", fg="green")
        else:
            click.secho(f"Failed to stop server: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"Failed to stop server: {e}", fg="red")

@server.command("restart")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server to restart.")
@pass_async_context
async def restart_server(ctx, server_name: str):
    """Gracefully restarts a specific Bedrock server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.echo(f"Attempting to restart server '{server_name}'...")
    try:
        response = await client.async_restart_server(server_name)
        if response.status == "success":
            click.secho(f"Restart signal sent to server '{server_name}'.", fg="green")
        else:
            click.secho(f"Failed to restart server: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"Failed to restart server: {e}", fg="red")

@server.command("install")
@pass_async_context
async def install(ctx):
    """Guides you through installing and configuring a new Bedrock server instance."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        click.secho("--- New Bedrock Server Installation ---", bold=True)
        server_name = await questionary.text("Enter a name for the new server:").ask_async()
        if not server_name:
            raise click.Abort()

        target_version = await questionary.text(
            "Enter server version (e.g., LATEST, PREVIEW, CUSTOM, 1.20.81.01):",
            default="LATEST",
        ).ask_async()
        if not target_version:
            raise click.Abort()

        overwrite = await questionary.confirm("Overwrite existing server if it exists?", default=False).ask_async()

        click.echo(f"\nInstalling server '{server_name}' version '{target_version}'...")
        
        payload = InstallServerPayload(server_name=server_name, server_version=target_version, overwrite=overwrite)
        install_result = await client.async_install_new_server(payload)

        if install_result.status == "success":
            click.secho("Server files installed successfully.", fg="green")
        else:
            click.secho(f"Failed to install server: {install_result.message}", fg="red")

    except Exception as e:
        click.secho(f"An application error occurred: {e}", fg="red")

@server.command("update")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server to update.")
@pass_async_context
async def update(ctx, server_name: str):
    """Checks for and applies updates to an existing Bedrock server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return
        
    click.echo(f"Checking for updates for server '{server_name}'...")
    try:
        response = await client.async_update_server(server_name)
        if response.status == "success":
            click.secho("Update check complete.", fg="green")
        else:
            click.secho(f"Failed to update server: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"A server update error occurred: {e}", fg="red")

@server.command("delete")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server to delete.")
@click.option("-y", "--yes", is_flag=True, help="Bypass the confirmation prompt.")
@pass_async_context
async def delete_server(ctx, server_name: str, yes: bool):
    """Deletes all data for a server, including world, configs, and backups."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    if not yes:
        click.secho(
            f"WARNING: This will permanently delete all data for server '{server_name}',\n"
            "including the installation, worlds, and all associated backups.",
            fg="red",
            bold=True,
        )
        click.confirm(
            f"\nAre you absolutely sure you want to delete '{server_name}'?", abort=True
        )

    click.echo(f"Proceeding with deletion of server '{server_name}'...")
    try:
        response = await client.async_delete_server(server_name)
        if response.status == "success":
            click.secho(f"Server '{server_name}' and all its data have been deleted.", fg="green")
        else:
            click.secho(f"Failed to delete server: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"Failed to delete server: {e}", fg="red")


@server.command("send-command")
@click.option("-s", "--server", "server_name", required=True, help="Name of the target server.")
@click.argument("command_parts", nargs=-1, required=True)
@pass_async_context
async def send_command(ctx, server_name: str, command_parts: str):
    """Sends a command to a running Bedrock server's console."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    command_string = " ".join(command_parts)
    click.echo(f"Sending command to '{server_name}': {command_string}")
    try:
        payload = CommandPayload(command=command_string)
        response = await client.async_send_server_command(server_name, payload)
        if response.status == "success":
            click.secho("Command sent successfully.", fg="green")
        else:
            click.secho(f"Failed to send command: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"Failed to send command: {e}", fg="red")

