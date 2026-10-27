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
@click.option(
    "--kind",
    type=click.Choice(
        [
            "manual",
            "scheduled",
            "pre_update",
            "pre_start",
            "pre_restore",
            "imported",
            "pinned",
        ]
    ),
)
@click.option("--search", default="", help="Match labels, notes, or filenames.")
@pass_async_context
async def list_backups(ctx, server_name, kind, search):
    """List completed portable backup archives."""
    try:
        result = await get_client(ctx).backups.async_list(server_name)
        if kind or search:
            result["backups"] = [
                item
                for item in result["backups"]
                if (
                    not kind
                    or item.get("purpose") == kind
                    or item.get("origin") == kind
                    or kind == "pinned"
                    and item.get("pinned")
                )
                and search.lower()
                in " ".join(
                    str(item.get(key, "")) for key in ("filename", "label", "notes")
                ).lower()
            ]
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
@click.option("--mode", type=click.Choice(["world", "selected", "full"]))
@click.option(
    "--component",
    "components",
    multiple=True,
    help="Component to capture in selected mode. Repeat for multiple components.",
)
@pass_async_context
async def create_backup(ctx, server_name, encrypted, unencrypted, mode, components):
    """Create one archive containing the server's supported data and settings."""
    try:
        client = get_client(ctx)
        if encrypted and unencrypted:
            raise click.UsageError("Choose only one encryption override.")
        policy = True if encrypted else False if unencrypted else None
        if components and mode not in (None, "selected"):
            raise click.UsageError("--component requires --mode selected")
        overrides = {}
        if mode or components:
            overrides["mode"] = mode or "selected"
        if components:
            overrides["components"] = list(components)
        accepted = await client.backups.async_create(server_name, policy, **overrides)
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
            "behavior_packs",
            "resource_packs",
            "development_behavior_packs",
            "development_resource_packs",
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


@backup.command("health")
@server_option
@pass_async_context
async def backup_health(ctx, server_name):
    """Show verification, storage copies, and recovery-key health."""
    try:
        result = await get_client(ctx).backups.async_health(server_name)
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("manage")
@server_option
@archive_option
@click.argument(
    "action",
    type=click.Choice(
        ["verify", "pin", "unpin", "copy", "test_key", "drill", "delete"]
    ),
)
@click.option("--destination", help="Configured destination name for copy.")
@click.option(
    "--unlock",
    is_flag=True,
    help="Privately prompt for the emergency-kit recovery key.",
)
@pass_async_context
async def manage_backup(ctx, server_name, backup_id, action, destination, unlock):
    """Verify or pin archives, retry copies, or test a recovery key."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        key = await unlock_key(unlock or action == "test_key")
        result = await client.backups.async_wait(
            await client.backups.async_manage(
                server_name,
                identifier,
                action,
                destination=destination,
                recovery_key=key,
            )
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("prepare-copy")
@server_option
@archive_option
@click.option("--name", required=True, help="New server name.")
@click.option("--port", required=True, type=click.IntRange(1, 65535))
@click.option("--portv6", required=True, type=click.IntRange(1, 65535))
@click.option("--version", default="LATEST", show_default=True)
@click.option("--unlock", is_flag=True)
@click.option("--yes", is_flag=True, help="Skip installation confirmation.")
@pass_async_context
async def prepare_backup_copy(
    ctx, server_name, backup_id, name, port, portv6, version, unlock, yes
):
    """Install a stopped destination; review its archive before restoring."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        if (
            not yes
            and not await questionary.confirm(
                f"Install a stopped server named {name}?", default=False
            ).ask_async()
        ):
            raise click.Abort()
        key = await unlock_key(unlock)
        result = await client.backups.async_wait(
            await client.backups.async_prepare_copy(
                server_name,
                identifier,
                name,
                port,
                portv6,
                target_version=version,
                recovery_key=key,
            )
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


# Both names use the same native multipart implementation.
backup.add_command(import_backup, "upload")


@backup.command("dry-run")
@server_option
@archive_option
@click.option("--component", "components", multiple=True, required=True)
@click.option("--unlock", is_flag=True)
@pass_async_context
async def dry_run_backup(ctx, server_name, backup_id, components, unlock):
    """Exercise selected replacement copies in isolation and report free space."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        key = await unlock_key(unlock)
        result = await client.backups.async_wait(
            await client.backups.async_dry_run(
                server_name, identifier, list(components), key
            )
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("annotate")
@server_option
@archive_option
@click.option("--label", default=None)
@click.option("--notes", default=None)
@pass_async_context
async def annotate_backup(ctx, server_name, backup_id, label, notes):
    """Edit manager-local labels and notes without rewriting archive contents."""
    try:
        client = get_client(ctx)
        identifier = await choose_archive(client, server_name, backup_id)
        result = await client.backups.async_wait(
            await client.backups.async_manage(
                server_name, identifier, "annotate", label=label, notes=notes
            )
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("schedule")
@server_option
@click.option("--time", "local_time", default="03:00", show_default=True)
@click.option("--timezone", "zone", default="UTC", show_default=True)
@click.option(
    "--days", default="0,1,2,3,4,5,6", help="Weekdays: Monday=0 through Sunday=6."
)
@click.option("--stagger", default=15, type=click.IntRange(0, 120))
@click.option("--catch-up/--skip-missed", default=True)
@click.option("--disable", is_flag=True)
@click.option("--remove", is_flag=True)
@pass_async_context
async def schedule_backup(
    ctx, server_name, local_time, zone, days, stagger, catch_up, disable, remove
):
    """Configure one timezone-aware daily server schedule."""
    try:
        weekdays = [int(day.strip()) for day in days.split(",")]
        result = await get_client(ctx).backups.async_set_schedule(
            server_name,
            (
                None
                if remove
                else {
                    "enabled": not disable,
                    "time": local_time,
                    "timezone": zone,
                    "weekdays": weekdays,
                    "catch_up": catch_up,
                    "stagger_minutes": stagger,
                }
            ),
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("cleanup-destination")
@server_option
@click.option("--destination", required=True)
@click.option(
    "--apply", is_flag=True, help="Confirm and apply the displayed cleanup preview."
)
@pass_async_context
async def cleanup_backup_destination(ctx, server_name, destination, apply):
    """Review external-copy retention before explicitly deleting eligible copies."""
    try:
        client = get_client(ctx)
        result = await client.backups.async_wait(
            await client.backups.async_cleanup_destination(server_name, destination)
        )
        click.echo(json.dumps(result, indent=2))
        plan = result["plan"]
        if (
            apply
            and plan["delete"]
            and click.confirm(
                "Permanently delete the reviewed external copies?", default=False
            )
        ):
            result = await client.backups.async_wait(
                await client.backups.async_cleanup_destination(
                    server_name, destination, plan["token"]
                )
            )
            click.echo(json.dumps(result, indent=2))
    except Exception as error:
        fail(error)


@backup.command("report")
@server_option
@click.option("--output", required=True, type=click.Path(path_type=Path))
@pass_async_context
async def recovery_report(ctx, server_name, output):
    """Save a redacted JSON recovery report to a new file."""
    created = False
    try:
        report = await get_client(ctx).backups.async_recovery_report(server_name)
        with output.open("x", encoding="utf-8") as stream:
            created = True
            json.dump(report, stream, indent=2)
            stream.write("\n")
        click.echo(f"Recovery report saved to {output}.")
    except Exception as error:
        if created:
            output.unlink(missing_ok=True)
        fail(error)
