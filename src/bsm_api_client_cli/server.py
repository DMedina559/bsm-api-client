import os
import time
import click
import questionary
from .decorators import pass_async_context
from bsm_api_client.models import InstallServerPayload, CommandPayload


def _print_server_table(servers):
    """Prints a formatted table of server information to the console."""
    header = f"{'SERVER NAME':<25} {'STATUS':<15} {'VERSION'}"
    click.secho(header, bold=True)
    click.echo("-" * 65)

    if not servers:
        click.echo("  No servers found.")
    else:
        for server_data in servers:
            name = server_data.get("name", "N/A")
            status = server_data.get("status", "UNKNOWN").upper()
            version = server_data.get("version", "UNKNOWN")

            color_map = {
                "RUNNING": "green",
                "STOPPED": "red",
                "STARTING": "yellow",
                "STOPPING": "yellow",
                "INSTALLING": "bright_cyan",
                "UPDATING": "bright_cyan",
                "INSTALLED": "bright_magenta",
                "UPDATED": "bright_magenta",
                "UNKNOWN": "bright_black",
            }
            status_color = color_map.get(status, "red")

            status_styled = click.style(f"{status:<10}", fg=status_color)
            name_styled = click.style(name, fg="cyan")
            version_styled = click.style(version, fg="bright_white")

            click.echo(f"  {name_styled:<38} {status_styled:<20} {version_styled}")
    click.echo("-" * 65)


@click.group()
def server():
    """Manages servers."""
    pass


@server.command("list")
@click.option(
    "--loop", is_flag=True, help="Continuously refresh server statuses every 5 seconds."
)
@click.option("--server-name", help="Display status for only a specific server.")
@pass_async_context
async def list_servers(ctx, loop, server_name):
    """Lists all configured Bedrock servers and their current operational status."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    async def _display_status():
        response = await client.async_get_servers_details()
        all_servers = response.servers

        if server_name:
            servers_to_show = [s for s in all_servers if s.get("name") == server_name]
        else:
            servers_to_show = all_servers

        _print_server_table(servers_to_show)

    try:
        if loop:
            while True:
                click.clear()
                click.secho(
                    "--- Bedrock Servers Status (Press CTRL+C to exit) ---",
                    fg="magenta",
                    bold=True,
                )
                await _display_status()
                time.sleep(5)
        else:
            if not server_name:
                click.secho("--- Bedrock Servers Status ---", fg="magenta", bold=True)
            await _display_status()

    except (KeyboardInterrupt, click.Abort):
        click.secho("\nExiting status monitor.", fg="green")
    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@server.command("start")
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the server to start."
)
@click.pass_context
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
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the server to stop."
)
@click.pass_context
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
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server to restart.",
)
@click.pass_context
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


from bsm_api_client.models import InstallServerPayload, CommandPayload
from .properties import interactive_properties_workflow
from .allowlist import interactive_allowlist_workflow
from .permissions import interactive_permissions_workflow


@server.command("install")
@click.pass_context
async def install(ctx):
    """Guides you through installing and configuring a new Bedrock server instance."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        click.secho("--- New Bedrock Server Installation ---", bold=True)
        server_name = await questionary.text(
            "Enter a name for the new server:"
        ).ask_async()
        if not server_name:
            raise click.Abort()

        target_version = await questionary.text(
            "Enter server version (e.g., LATEST, PREVIEW, CUSTOM, 1.20.81.01):",
            default="LATEST",
        ).ask_async()
        if not target_version:
            raise click.Abort()

        server_zip_path = None
        if target_version.upper() == "CUSTOM":
            response = await client.async_get_custom_zips()
            available_files = response["custom_zips"]

            if not available_files:
                click.secho(
                    "No custom server ZIP files found in the content/custom directory.",
                    fg="red",
                )
                return

            file_map = {os.path.basename(f): f for f in available_files}
            choices = sorted(list(file_map.keys())) + ["Cancel"]
            selection = await questionary.select(
                "Select a custom server ZIP to install:", choices=choices
            ).ask_async()

            if not selection or selection == "Cancel":
                raise click.Abort()
            server_zip_path = file_map[selection]

        overwrite = await questionary.confirm(
            "Overwrite existing server if it exists?", default=False
        ).ask_async()

        click.echo(f"\nInstalling server '{server_name}' version '{target_version}'...")

        payload = InstallServerPayload(
            server_name=server_name,
            server_version=target_version,
            overwrite=overwrite,
            server_zip_path=server_zip_path,
        )
        install_result = await client.async_install_new_server(payload)

        if install_result.task_id:
            time.sleep(5)  # Give the server time to start installation
            click.echo("Server installation started. Polling for completion...")
            while True:
                status_response = await client.async_get_install_status(
                    install_result.task_id
                )
                if status_response["status"] == "success":
                    click.secho(
                        "Server installation completed successfully.", fg="green"
                    )
                    break
                elif status_response["status"] == "error":
                    click.secho(
                        f"Installation failed: {status_response['message']}", fg="red"
                    )
                    return
                time.sleep(2)
        elif install_result.status == "success":
            click.secho("Server files installed successfully.", fg="green")
        else:
            click.secho(f"Failed to install server: {install_result.message}", fg="red")
            return

        await interactive_properties_workflow(client, server_name)
        if await questionary.confirm(
            "\nConfigure the allowlist now?", default=False
        ).ask_async():
            await interactive_allowlist_workflow(client, server_name)
        if await questionary.confirm(
            "\nConfigure player permissions now?", default=False
        ).ask_async():
            await interactive_permissions_workflow(client, server_name)

        click.secho(
            "\nInstallation and initial configuration complete!", fg="green", bold=True
        )

        if await questionary.confirm(
            f"Start server '{server_name}' now?", default=True
        ).ask_async():
            await ctx.invoke(start_server, server_name=server_name)

    except Exception as e:
        click.secho(f"An application error occurred: {e}", fg="red")


@server.command("update")
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the server to update."
)
@click.pass_context
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
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the server to delete."
)
@click.option("-y", "--yes", is_flag=True, help="Bypass the confirmation prompt.")
@click.pass_context
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
            click.secho(
                f"Server '{server_name}' and all its data have been deleted.",
                fg="green",
            )
        else:
            click.secho(f"Failed to delete server: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"Failed to delete server: {e}", fg="red")


@server.command("send-command")
@click.option(
    "-s", "--server", "server_name", required=True, help="Name of the target server."
)
@click.argument("command_parts", nargs=-1, required=True)
@click.pass_context
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
