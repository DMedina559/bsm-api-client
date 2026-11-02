"""Manage persistent application schedules."""

import json
from pathlib import Path

import click

from bsm_api_client.models import ScheduledTask

from .output import get_client
from .presentation import table


@click.group()
def scheduler():
    """Manage scheduled server tasks, built-in operations, and plugin schedules."""


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


@scheduler.command("tasks")
@click.pass_context
async def list_tasks(ctx):
    """Show registered scheduled task types and their definitions."""
    result = await get_client(ctx).scheduler.async_list_schedules()
    if not ctx.obj.get("json_output"):
        definitions = result.task_definitions or {}
        names = sorted(set(result.task_types or []) | set(definitions))
        table(
            "Scheduled Tasks",
            ["Task", "Owner", "Timeout (s)", "Server lock", "Description"],
            [
                [
                    name,
                    (definitions.get(name) or {}).get("owner", "application"),
                    (definitions.get(name) or {}).get("timeout_seconds"),
                    (definitions.get(name) or {}).get("requires_server_lock", True),
                    (definitions.get(name) or {}).get("description", ""),
                ]
                for name in names
            ],
        )
    return result


@scheduler.command("save")
@click.argument("schedule_id")
@click.argument(
    "configuration",
    required=False,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--task", help="Task name (e.g. backup:create, backup:verify, server:restart)."
)
@click.option("--server-name", help="Target server name.")
@click.option("--time", "run_time", help="24-hour local run time (HH:MM).")
@click.option(
    "--timezone", help="IANA timezone name (defaults to application timezone)."
)
@click.option(
    "--enabled/--disabled",
    default=None,
    help="Enable or pause the schedule.",
)
@click.option(
    "--catch-up/--no-catch-up",
    default=None,
    help="Run the latest missed occurrence after downtime.",
)
@click.option(
    "--stagger-minutes",
    type=click.IntRange(0, 120),
    help="Deterministic per-server stagger window in minutes.",
)
@click.option(
    "--options-json",
    help="JSON object of task options.",
)
@click.pass_context
async def save_schedule(  # noqa: C901
    ctx,
    schedule_id,
    configuration,
    task,
    server_name,
    run_time,
    timezone,
    enabled,
    catch_up,
    stagger_minutes,
    options_json,
):
    """Create or replace SCHEDULE_ID using a JSON file or CLI options."""
    try:
        payload = (
            json.loads(configuration.read_text(encoding="utf-8"))
            if configuration is not None
            else {}
        )
        if not isinstance(payload, dict):
            raise ValueError("Schedule configuration must be a JSON object.")
        if task is not None:
            payload["task"] = task
        if server_name is not None:
            payload["server_name"] = server_name
        if run_time is not None:
            payload["time"] = run_time
        if timezone is not None:
            payload["timezone"] = timezone
        if enabled is not None:
            payload["enabled"] = enabled
        if catch_up is not None:
            payload["catch_up"] = catch_up
        if stagger_minutes is not None:
            payload["stagger_minutes"] = stagger_minutes
        if options_json is not None:
            parsed_options = json.loads(options_json)
            if not isinstance(parsed_options, dict):
                raise ValueError("--options-json must be a JSON object.")
            payload["options"] = parsed_options
        config = ScheduledTask.model_validate_json(json.dumps(payload))
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
