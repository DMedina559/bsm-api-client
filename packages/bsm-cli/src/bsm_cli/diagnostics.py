"""Download backend support reports through the authenticated live contract."""

from pathlib import Path

import click

from bsm_cli.api import download
from bsm_cli.decorators import pass_async_context


@click.group()
def diagnostics():
    """Inspect backend diagnostic metadata and save support reports."""


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
