import click
import os
import questionary
from .decorators import pass_async_context
from bsm_api_client.models import FileNamePayload

@click.group()
def world():
    """Manages server worlds."""
    pass

@world.command("install")
@click.option("-s", "--server", "server_name", required=True, help="Name of the target server.")
@click.option(
    "-f",
    "--file",
    "world_file_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Path to the .mcworld file to install. Skips interactive menu.",
)
@pass_async_context
async def install_world(ctx, server_name: str, world_file_path: str):
    """Installs a world from a .mcworld file, replacing the server's current world."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        selected_file = world_file_path

        if not selected_file:
            click.secho(
                f"Entering interactive world installation for server: {server_name}",
                fg="yellow",
            )
            response = await client.async_get_content_worlds()
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
        if not await questionary.confirm(
            "This action cannot be undone. Are you sure?", default=False
        ).ask_async():
            raise click.Abort()

        click.echo(f"Installing world '{filename}'...")
        payload = FileNamePayload(filename=filename)
        response = await client.async_install_server_world(server_name, payload)
        
        if response.status == "success":
            click.secho(f"World '{filename}' installed successfully.", fg="green")
        else:
            click.secho(f"Failed to install world: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@world.command("export")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server whose world to export.")
@pass_async_context
async def export_world(ctx, server_name: str):
    """Exports the server's current active world to a .mcworld file."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return
        
    click.echo(f"Attempting to export world for server '{server_name}'...")
    try:
        response = await client.async_export_server_world(server_name)
        if response.status == "success":
            click.secho("World exported successfully.", fg="green")
        else:
            click.secho(f"Failed to export world: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred during export: {e}", fg="red")


@world.command("reset")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server whose world to reset.")
@click.option("-y", "--yes", is_flag=True, help="Bypass the confirmation prompt.")
@pass_async_context
async def reset_world(ctx, server_name: str, yes: bool):
    """Deletes the current active world data for a server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

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
        response = await client.async_reset_server_world(server_name)
        if response.status == "success":
            click.secho("World has been reset successfully.", fg="green")
        else:
            click.secho(f"Failed to reset world: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred during reset: {e}", fg="red")
