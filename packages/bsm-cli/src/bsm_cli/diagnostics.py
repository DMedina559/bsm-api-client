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
