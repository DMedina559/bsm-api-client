"""Portable archive creation and reviewed component restoration."""

import json
from pathlib import Path

import click
import questionary

from bsm_cli.completion import complete_server
from bsm_cli.decorators import monitor_task, pass_async_context
from bsm_cli.output import fail, get_client


@click.group()
def backup():
    """Create, inspect and selectively restore portable server backups."""


def server_option(function):
    return click.option(
        "-s", "--server", "server_name", required=True, shell_complete=complete_server
    )(function)


def archive_option(function):
    return click.option(
        "-f",
        "--file",
        "backup_id",
        help="Archive ID from backup list; otherwise select interactively.",
    )(function)


async def choose_archive(client, server_name, backup_id):
    if backup_id:
        return backup_id
    listing = await client.backups.async_list(server_name)
    choices = [
        item["backup_id"] for item in listing["backups"] if not item.get("error")
    ]
    if not choices:
        raise click.ClickException("No portable server backups are available.")
    selected = await questionary.select(
        "Choose a backup:", choices=choices + ["Cancel"]
    ).ask_async()
    if not selected or selected == "Cancel":
        raise click.Abort()
    return selected


async def unlock_key(unlock):
    if not unlock:
        return None
    return await questionary.password("Backup recovery key:").ask_async()


@backup.command("list")
@server_option
@pass_async_context
async def list_backups(ctx, server_name):
    """List completed portable backup archives."""
    try:
        result = await get_client(ctx).backups.async_list(server_name)
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("create")
@server_option
@click.option("--encrypted", is_flag=True, help="Encrypt this backup.")
@click.option(
    "--unencrypted",
    "--no-encrypted",
    is_flag=True,
    help="Create an unencrypted backup.",
)
@pass_async_context
async def create_backup(ctx, server_name, encrypted, unencrypted):
    """Create one archive containing the server's supported data and settings."""
    try:
        client = get_client(ctx)
        if encrypted and unencrypted:
            raise click.UsageError("Choose only one encryption override.")
        policy = True if encrypted else False if unencrypted else None
        accepted = await client.backups.async_create(server_name, policy)
        await monitor_task(
            client, accepted["task_id"], "Server backup created", "Backup failed"
        )
    except Exception as error:
        fail(error)


@backup.command("inspect")
@server_option
@archive_option
@click.option(
    "--unlock",
    is_flag=True,
    help="Prompt privately for an imported backup's recovery key.",
)
@pass_async_context
async def inspect_backup(ctx, server_name, backup_id, unlock):
    """Authenticate the archive and display its component manifest."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        accepted = await client.backups.async_inspect(
            server_name, identifier, await unlock_key(unlock)
        )
        result = await client.backups.async_wait(accepted)
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("restore")
@server_option
@archive_option
@click.option(
    "--component",
    "components",
    multiple=True,
    type=click.Choice(
        [
            "world",
            "server.properties",
            "allowlist.json",
            "permissions.json",
            "script_config",
            "bsm_settings",
        ]
    ),
    help="Repeat to select complete components; otherwise choose interactively.",
)
@click.option("--unlock", is_flag=True, help="Prompt privately for the recovery key.")
@click.option(
    "--restart/--no-restart",
    default=True,
    help="Restart an originally running server after successful restoration.",
)
@click.option(
    "--yes",
    is_flag=True,
    help="Confirm the reviewed replacements without an interactive prompt.",
)
@pass_async_context
async def restore_backup(ctx, server_name, backup_id, components, unlock, restart, yes):
    """Inspect, review, then restore explicitly selected archive components."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        key = await unlock_key(unlock)
        inspected = await client.backups.async_wait(
            await client.backups.async_inspect(server_name, identifier, key)
        )
        available = [
            name
            for name, state in inspected["backup"]["manifest"]["components"].items()
            if state == "included"
        ]
        selected = (
            list(components)
            if components
            else await questionary.checkbox(
                "Components to replace:", choices=available
            ).ask_async()
        )
        if not selected or any(name not in available for name in selected):
            raise click.UsageError("Select components included in this backup.")
        planned = await client.backups.async_wait(
            await client.backups.async_plan(server_name, identifier, selected, key)
        )
        plan = planned["plan"]
        click.echo(json.dumps(plan, indent=2))
        if (
            not yes
            and not await questionary.confirm(
                f"Replace these components on {server_name}? The Minecraft server will stop during restoration.",
                default=False,
            ).ask_async()
        ):
            raise click.Abort()
        accepted = await client.backups.async_restore(
            server_name, identifier, selected, plan["token"], key, restart
        )
        await monitor_task(
            client,
            accepted["task_id"],
            "Selected components restored",
            "Restore failed",
        )
    except Exception as error:
        fail(error)


@backup.command("prune")
@server_option
@pass_async_context
async def prune_backups(ctx, server_name):
    """Apply archive retention; zero disables automatic pruning."""
    try:
        client = get_client(ctx)
        response = await client.content.async_prune_server_backups(server_name)
        await monitor_task(
            client, response.task_id, "Pruning complete", "Pruning failed"
        )
    except Exception as error:
        fail(error)


@backup.command("download")
@server_option
@archive_option
@click.option(
    "--output",
    required=True,
    type=click.Path(path_type=Path),
    help="New destination file; existing files are preserved.",
)
@pass_async_context
async def download_backup(ctx, server_name, backup_id, output):
    """Download a stored archive without removing its encryption."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        await client.backups.async_download_to(server_name, identifier, output)
        click.echo(str(output))
    except Exception as error:
        fail(error)


@backup.command("import")
@server_option
@click.argument("archive", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--unlock", is_flag=True, help="Prompt privately for the archive's recovery key."
)
@pass_async_context
async def import_backup(ctx, server_name, archive, unlock):
    """Upload and validate ARCHIVE before adding it to a server's backups."""
    try:
        key = await unlock_key(unlock)
        with archive.open("rb") as stream:
            result = await get_client(ctx).backups.async_import(
                server_name, stream, archive.name, key
            )
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)
