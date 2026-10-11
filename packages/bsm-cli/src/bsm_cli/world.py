import os

import click
import questionary

from bsm_api_client.models import FileNamePayload
from bsm_cli.completion import complete_server
from bsm_cli.decorators import monitor_task, pass_async_context
from bsm_cli.output import fail, get_client


@click.group()
def world():
    """Manages server worlds."""
    pass


@world.command("install")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the target server.",
    shell_complete=complete_server,
)
@click.option(
    "-f",
    "--file",
    "world_file_path",
    help="Filename in the backend content/worlds directory; skips interactive menu.",
)
@click.option("-y", "--yes", is_flag=True, help="Bypass the confirmation prompt.")
@pass_async_context
async def install_world(ctx, server_name: str, world_file_path: str, yes: bool):
    """Installs a world from a .mcworld file, replacing the server's current world."""
    client = get_client(ctx)

    try:
        selected_file = world_file_path

        if not selected_file:
            click.secho(
                f"Entering interactive world installation for server: {server_name}",
                fg="yellow",
            )
            response = await client.content.async_get_content_worlds()
            available_files = response.files

            if not available_files:
                click.secho(
                    "No .mcworld files found in the content/worlds directory. Nothing to install.",
                    fg="yellow",
                )
                return

            file_map = {os.path.basename(f): f for f in available_files}
            choices = sorted(list(file_map.keys())) + ["Cancel"]
            selection = await questionary.select(
                "Select a world to install:", choices=choices
            ).ask_async()

            if not selection or selection == "Cancel":
                raise click.Abort()
            selected_file = file_map[selection]

        filename = os.path.basename(selected_file)
        click.secho(
            f"\nWARNING: Installing '{filename}' will REPLACE the current world data for server '{server_name}'.",
            fg="red",
            bold=True,
        )
        if (
            not yes
            and not await questionary.confirm(
                "This action cannot be undone. Are you sure?", default=False
            ).ask_async()
        ):
            raise click.Abort()

        click.echo(f"Installing world '{filename}'...")
        payload = FileNamePayload(filename=filename)
        response = await client.content.async_install_server_world(server_name, payload)

        if getattr(response, "task_id", None):
            await monitor_task(
                client,
                str(getattr(response, "task_id", "")),
                f"World '{filename}' installed successfully",
                "Failed to install world",
            )
        elif response.status == "success":
            click.secho(f"World '{filename}' installed successfully.", fg="green")
        else:
            click.secho(f"Failed to install world: {response.message}", fg="red")

    except Exception as e:
        fail(e)


@world.command("export")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server whose world to export.",
    shell_complete=complete_server,
)
@pass_async_context
async def export_world(ctx, server_name: str):
    """Exports the server's current active world to a .mcworld file."""
    client = get_client(ctx)

    click.echo(f"Attempting to export world for server '{server_name}'...")
    try:
        response = await client.content.async_export_server_world(server_name)
        if getattr(response, "task_id", None):
            await monitor_task(
                client,
                str(getattr(response, "task_id", "")),
                "World exported successfully",
                "Failed to export world",
            )
        elif response.status == "success":
            click.secho("World exported successfully.", fg="green")
        else:
            click.secho(f"Failed to export world: {response.message}", fg="red")
    except Exception as e:
        fail(e)


@world.command("reset")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server whose world to reset.",
    shell_complete=complete_server,
)
@click.option("-y", "--yes", is_flag=True, help="Bypass the confirmation prompt.")
@pass_async_context
async def reset_world(ctx, server_name: str, yes: bool):
    """Deletes the current active world data for a server."""
    client = get_client(ctx)

    if not yes:
        click.secho(
            f"WARNING: This will permanently delete the current world for server '{server_name}'.",
            fg="red",
            bold=True,
        )
        click.confirm(
            "This action cannot be undone. Are you sure you want to reset the world?",
            abort=True,
        )

    click.echo(f"Resetting world for server '{server_name}'...")
    try:
        response = await client.content.async_reset_server_world(server_name)
        if getattr(response, "task_id", None):
            await monitor_task(
                client,
                str(getattr(response, "task_id", "")),
                "World has been reset successfully",
                "Failed to reset world",
            )
        elif response.status == "success":
            click.secho("World has been reset successfully.", fg="green")
        else:
            click.secho(f"Failed to reset world: {response.message}", fg="red")
    except Exception as e:
        fail(e)
