import click
import os
import questionary
from .decorators import pass_async_context
from bsm_api_client.models import BackupActionPayload, RestoreActionPayload

@click.group()
def backup():
    """Manages server backups."""
    pass

@backup.command("create")
@click.option("-s", "--server", "server_name", required=True, help="Name of the target server.")
@click.option(
    "-t",
    "--type",
    "backup_type",
    type=click.Choice(["world", "config", "all"], case_sensitive=False),
    help="Type of backup to create; skips interactive menu.",
)
@click.option(
    "-f",
    "--file",
    "file_to_backup",
    help="Specific file to back up (required if --type=config).",
)
@pass_async_context
async def create_backup(ctx, server_name: str, backup_type: str, file_to_backup: str):
    """Creates a backup of specified server data."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        if not backup_type:
            backup_type, file_to_backup, _ = _interactive_backup_menu(server_name)

        if backup_type == "config" and not file_to_backup:
            raise click.UsageError("Option '--file' is required when using '--type config'.")

        click.echo(f"Starting '{backup_type}' backup for server '{server_name}'...")
        
        payload = BackupActionPayload(backup_type=backup_type, file_to_backup=file_to_backup)
        response = await client.async_trigger_server_backup(server_name, payload)

        if response.status == "success":
            click.secho("Backup completed successfully.", fg="green")
            click.echo("Pruning old backups...")
            prune_response = await client.async_prune_server_backups(server_name)
            if prune_response.status == "success":
                click.secho("Pruning complete.", fg="green")
            else:
                click.secho(f"Failed to prune backups: {prune_response.message}", fg="red")
        else:
            click.secho(f"Failed to create backup: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")

@backup.command("restore")
@click.option("-s", "--server", "server_name", required=True, help="Name of the target server.")
@click.option(
    "-f",
    "--file",
    "backup_file_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Path to the backup file to restore; skips interactive menu.",
)
@pass_async_context
async def restore_backup(ctx, server_name: str, backup_file_path: str):
    """Restores server data from a specified backup file."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        if not backup_file_path:
            restore_type, backup_file_path, _ = await _interactive_restore_menu(client, server_name)
        else:
            filename = os.path.basename(backup_file_path).lower()
            if "world" in filename:
                restore_type = "world"
            elif "allowlist" in filename:
                restore_type = "allowlist"
            elif "permissions" in filename:
                restore_type = "permissions"
            elif "properties" in filename:
                restore_type = "properties"
            else:
                raise click.UsageError(f"Could not determine restore type from filename '{filename}'.")

        click.echo(f"Starting '{restore_type}' restore for server '{server_name}' from '{os.path.basename(backup_file_path)}'...")
        
        payload = RestoreActionPayload(restore_type=restore_type, backup_file=os.path.basename(backup_file_path))
        response = await client.async_restore_server_backup(server_name, payload)

        if response.status == "success":
            click.secho("Restore completed successfully.", fg="green")
        else:
            click.secho(f"Failed to restore backup: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@backup.command("prune")
@click.option("-s", "--server", "server_name", required=True, help="Name of the server whose backups to prune.")
@pass_async_context
async def prune_backups(ctx, server_name: str):
    """Deletes old backups for a server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        click.echo(f"Pruning old backups for server '{server_name}'...")
        response = await client.async_prune_server_backups(server_name)
        if response.status == "success":
            click.secho("Pruning complete.", fg="green")
        else:
            click.secho(f"Failed to prune backups: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred during pruning: {e}", fg="red")


def _interactive_backup_menu(server_name: str):
    click.secho(f"Entering interactive backup for server: {server_name}", fg="yellow")

    backup_type_map = {
        "Backup World Only": ("world", None, True),
        "Backup Everything (World + Configs)": ("all", None, True),
        "Backup a Specific Configuration File": ("config", None, False),
    }

    choice = questionary.select(
        "Select a backup option:",
        choices=list(backup_type_map.keys()) + ["Cancel"],
    ).ask()

    if not choice or choice == "Cancel":
        raise click.Abort()

    b_type, b_file, b_change_status = backup_type_map[choice]

    if b_type == "config":
        config_file_map = {
            "allowlist.json": "allowlist.json",
            "permissions.json": "permissions.json",
            "server.properties": "server.properties",
        }
        file_choice = questionary.select(
            "Which configuration file do you want to back up?",
            choices=list(config_file_map.keys()) + ["Cancel"],
        ).ask()

        if not file_choice or file_choice == "Cancel":
            raise click.Abort()
        b_file = config_file_map[file_choice]

    return b_type, b_file, b_change_status


async def _interactive_restore_menu(client, server_name: str):
    click.secho(f"Entering interactive restore for server: {server_name}", fg="yellow")

    restore_type_map = {
        "Restore World": "world",
        "Restore Allowlist": "allowlist",
        "Restore Permissions": "permissions",
        "Restore Properties": "properties",
    }

    choice = await questionary.select(
        "What do you want to restore?",
        choices=list(restore_type_map.keys()) + ["Cancel"],
    ).ask_async()

    if not choice or choice == "Cancel":
        raise click.Abort()
    restore_type = restore_type_map[choice]

    response = await client.async_list_server_backups(server_name, restore_type)
    backup_files = response.backups
    if not backup_files:
        click.secho(
            f"No '{restore_type}' backups found for server '{server_name}'.",
            fg="yellow",
        )
        raise click.Abort()

    file_map = {os.path.basename(f): f for f in backup_files}
    file_choices = sorted(list(file_map.keys()), reverse=True)

    file_to_restore_basename = await questionary.select(
        f"Select a '{restore_type}' backup to restore:",
        choices=file_choices + ["Cancel"],
    ).ask_async()

    if not file_to_restore_basename or file_to_restore_basename == "Cancel":
        raise click.Abort()
    selected_file_path = file_map[file_to_restore_basename]

    return restore_type, selected_file_path, True
