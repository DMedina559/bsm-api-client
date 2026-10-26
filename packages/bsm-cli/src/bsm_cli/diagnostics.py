"""Administrator snapshots, retained history and correlated traces."""

from pathlib import Path

import click

from bsm_cli.api import download
from bsm_cli.decorators import pass_async_context
from bsm_cli.manager import outcome
from bsm_cli.output import get_client
from bsm_cli.presentation import table


@click.group()
def diagnostics():
    """Inspect administrator observations and retained history."""


@diagnostics.command("activity")
@click.option("--limit", type=click.IntRange(1, 200), default=100, show_default=True)
@click.option("--event-name", "name", help="Filter by event name.")
@click.option("--owner")
@click.option("--source")
@click.option("--server-name")
@click.option("--operation-name")
@click.option("--operation-id")
@click.option("--sequence-id")
@click.option("--correlation-id")
@click.option("--phase", type=click.Choice(["before", "after", "custom", "lifecycle"]))
@click.option(
    "--status",
    type=click.Choice(
        ["dispatching", "completed", "partial", "cancelled", "suppressed"]
    ),
)
@click.pass_context
async def diagnostic_activity(ctx, **filters):
    """Inspect activity across all execution chains, not just one correlation."""
    result = await get_client(ctx).diagnostics.async_get_diagnostic_activity(**filters)
    if not ctx.obj.get("json_output"):
        click.echo(
            "Global activity: bounded current-instance metadata; history resets on restart."
        )
        outcome(result.model_dump(mode="json"))
        if result.truncated:
            click.echo(
                "Partial activity view; narrow the filters to inspect specific work."
            )
    return result


@diagnostics.command("snapshot")
@click.option("--subsystem", help="Inspect one registered subsystem.")
@click.pass_context
async def diagnostic_snapshot(ctx, subsystem):
    """Show current health, readiness and subsystem observations."""
    service = get_client(ctx).diagnostics
    result = (
        await service.async_get_subsystem_diagnostics(subsystem)
        if subsystem
        else await service.async_get_application_diagnostics()
    )
    if not ctx.obj.get("json_output"):
        if subsystem:
            outcome(result.model_dump(mode="json"))
        else:
            ready = result.summary.ready
            click.echo(
                f"Health: {result.summary.status} | Ready: {ready if ready is not None else 'Not assessed'}"
            )
            table(
                "Subsystems",
                ("Name", "Health", "Observation"),
                [
                    (
                        item.name,
                        item.status,
                        (
                            "Stale"
                            if item.stale
                            else "Not reported" if item.data is None else "Reported"
                        ),
                    )
                    for item in result.sections
                ],
            )
            for finding in result.summary.findings:
                click.echo(f"{finding.subsystem}: {finding.issue.message}")
    return result


@diagnostics.command("history")
@click.option("--limit", type=click.IntRange(1, 200), default=100, show_default=True)
@click.option("--subsystem")
@click.option("--instance-id")
@click.option("--correlation-id")
@click.option("--cursor")
@click.option("--owner")
@click.option("--code")
@click.option("--outcome", type=click.Choice(["completed", "failed", "cancelled"]))
@click.option("--operation-id")
@click.pass_context
async def diagnostic_history(ctx, **filters):
    """Read one retained page; continue with the returned cursor."""
    result = await get_client(ctx).diagnostics.async_get_diagnostic_history(**filters)
    if not ctx.obj.get("json_output"):
        if not result.available:
            click.echo("Retained history is unavailable.")
        else:
            table(
                "Retained records",
                ("Time", "Subsystem", "Operation", "Outcome", "Correlation"),
                [
                    (
                        record.timestamp,
                        record.subsystem,
                        record.operation,
                        record.outcome,
                        record.correlation_id or "No correlation ID",
                    )
                    for record in result.records
                ],
            )
            if not result.records:
                click.echo("No matching retained records.")
            if result.next_cursor:
                click.echo(f"Next cursor: {result.next_cursor}")
            if result.truncated:
                click.echo("Additional retained records may be available.")
    return result


@diagnostics.command("runs")
@click.option("--limit", type=click.IntRange(1, 50), default=20, show_default=True)
@click.pass_context
async def diagnostic_runs(ctx, limit):
    """Inspect retained application instances across restarts."""
    result = await get_client(ctx).diagnostics.async_get_diagnostic_runs(limit=limit)
    if not ctx.obj.get("json_output"):
        if not result.available:
            click.echo("Instance summaries are unavailable.")
        else:
            table(
                "Application instances",
                ("Instance", "Current", "Records", "Failures", "Last phase"),
                [
                    (
                        run.instance_id,
                        run.current_instance,
                        run.retained_records,
                        run.failed_records,
                        run.last_observed_phase or "Not reported",
                    )
                    for run in result.runs
                ],
            )
            if result.truncated:
                click.echo("Additional retained instances were omitted.")
    return result


@diagnostics.command("trace")
@click.argument("correlation_id")
@click.option("--limit", type=click.IntRange(1, 200), default=100, show_default=True)
@click.option("--cursor")
@click.pass_context
async def diagnostic_trace(ctx, correlation_id, limit, cursor):
    """Inspect a correlated operation with partial-source availability."""
    result = await get_client(ctx).diagnostics.async_get_diagnostic_trace(
        correlation_id, limit=limit, cursor=cursor
    )
    if not ctx.obj.get("json_output"):
        click.echo(
            f"Operations: {'available' if result.operations_available else 'unavailable'} | Events: {'available' if result.events_available else 'unavailable'} | Tasks: {'available' if result.tasks_available else 'unavailable'} | History: {'available' if result.history.available else 'unavailable'}"
        )
        outcome(result.model_dump(mode="json"))
        if result.truncated:
            click.echo("This trace is partial; use history filters or its next cursor.")
    return result


@diagnostics.command("compare")
@click.argument("before", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("after", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.pass_context
async def diagnostic_compare(ctx, before, after):
    """Compare two saved snapshots or support-report snapshots."""
    import json

    from bsm_api_client.models import CompareDiagnosticSnapshotsRequest

    def read(path):
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("snapshot", data) if isinstance(data, dict) else data

    payload = CompareDiagnosticSnapshotsRequest(before=read(before), after=read(after))
    result = await get_client(ctx).diagnostics.async_compare_diagnostic_snapshots(
        payload
    )
    if not ctx.obj.get("json_output"):
        if not result.same_instance:
            click.echo("Application instance changed; counter deltas are unavailable.")
        outcome(result.model_dump(mode="json"))
        if not result.changes:
            click.echo("No changes in compared fields.")
    return result


@diagnostics.command("report")
@click.option(
    "--output",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Destination for the JSON support report.",
)
@click.option("--force", is_flag=True, help="Replace an existing destination.")
@pass_async_context
async def report(ctx, output: Path, force: bool):
    """Save a complete administrator report using live OpenAPI discovery."""
    if output.exists() and not force:
        raise click.BadParameter(
            "Destination exists; use --force to replace it.", param_hint="--output"
        )
    return await ctx.invoke(
        download, operation_id="get_diagnostic_report", output=output, param=()
    )
