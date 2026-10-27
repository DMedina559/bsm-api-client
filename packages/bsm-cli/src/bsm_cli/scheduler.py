"""Manage persistent application schedules."""

from pathlib import Path

import click

from bsm_api_client.models import ScheduledTask

from .output import get_client
from .presentation import table


@click.group()
def scheduler():
    """Manage backup and verification schedules."""


@scheduler.command("list")
@click.option("--server-name")
@click.pass_context
async def list_schedules(ctx, server_name):
    """Show schedules, availability and recent run metadata."""
    result = await get_client(ctx).scheduler.async_list_schedules(server_name)
    if not ctx.obj.get("json_output"):
        table(
            "Schedules",
            [
                "Name",
                "Server",
                "Task",
                "Local time",
                "Available",
                "Next run",
                "Last result",
            ],
            [
                [
                    s.schedule_id,
                    s.configuration.server_name,
                    s.configuration.task,
                    f"{s.configuration.time} {s.configuration.timezone}",
                    s.available,
                    s.next_run_at,
                    s.last_status,
                ]
                for s in (result.schedules or [])
            ],
        )
    return result


@scheduler.command("save")
@click.argument("schedule_id")
@click.argument(
    "configuration", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.pass_context
async def save_schedule(ctx, schedule_id, configuration):
    """Create or replace SCHEDULE_ID using a JSON configuration file."""
    try:
        config = ScheduledTask.model_validate_json(
            configuration.read_text(encoding="utf-8")
        )
    except (ValueError, OSError) as error:
        raise click.ClickException(str(error)) from error
    result = await get_client(ctx).scheduler.async_save_schedule(schedule_id, config)
    if not ctx.obj.get("json_output"):
        click.echo(result.message)
    return result


@scheduler.command("remove")
@click.argument("schedule_id")
@click.pass_context
async def remove_schedule(ctx, schedule_id):
    """Remove a schedule without deleting backup archives."""
    result = await get_client(ctx).scheduler.async_delete_schedule(schedule_id)
    if not ctx.obj.get("json_output"):
        click.echo(result.message)
    return result


@scheduler.command("control")
@click.argument("schedule_id")
@click.argument("action", type=click.Choice(["run-now", "pause", "resume", "retry"]))
@click.option("--revision", help="Revision from the most recent schedule listing.")
@click.option(
    "--yes", is_flag=True, help="Confirm immediate execution without prompting."
)
@click.pass_context
async def control_schedule(ctx, schedule_id, action, revision, yes):
    """Run, retry, pause or resume a persistent schedule."""
    if action in ("run-now", "retry") and not yes:
        click.confirm(f"{action} for {schedule_id}?", abort=True)
    result = await get_client(ctx).scheduler.async_control_schedule(
        schedule_id, action.replace("-", "_"), revision=revision
    )
    click.echo(result.message)
