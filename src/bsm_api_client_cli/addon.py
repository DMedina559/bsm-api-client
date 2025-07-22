import click
import os
import questionary
from bsm_api_client.models import FileNamePayload

@click.group()
def addon():
    """Manages server addons."""
    pass

@addon.command("install")
@click.option("-s", "--server", "server_name", required=True, help="Name of the target server.")
@click.option(
    "-f",
    "--file",
    "addon_file_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Path to the addon file (.mcpack, .mcaddon); skips interactive menu.",
)
@click.pass_context
async def install_addon(ctx, server_name: str, addon_file_path: str):
    """Installs a behavior or resource pack addon to a specified server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        selected_addon_path = addon_file_path

        if not selected_addon_path:
            click.secho(
                f"Entering interactive addon installation for server: {server_name}",
                fg="yellow",
            )
            response = await client.async_get_content_addons()
            available_files = response.files

            if not available_files:
                click.secho(
                    "No addon files found in the content/addons directory. Nothing to install.",
                    fg="yellow",
                )
                return

            file_map = {os.path.basename(f): f for f in available_files}
            choices = sorted(list(file_map.keys())) + ["Cancel"]
            selection = await questionary.select(
                "Select an addon to install:", choices=choices
            ).ask_async()

            if not selection or selection == "Cancel":
                raise click.Abort()
            selected_addon_path = file_map[selection]

        addon_filename = os.path.basename(selected_addon_path)
        click.echo(f"Installing addon '{addon_filename}' to server '{server_name}'...")

        payload = FileNamePayload(filename=addon_filename)
        response = await client.async_install_server_addon(server_name, payload)
        if response.status == "success":
            click.secho(f"Addon '{addon_filename}' installed successfully.", fg="green")
        else:
            click.secho(f"Failed to install addon: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")
