# src/bsm_cli/content.py
"""CLI commands for content management."""

import click
from bsm_cli.decorators import pass_async_context


@click.group()
def content():
    """Commands for managing content."""
    pass


@content.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@pass_async_context
async def upload(ctx, file_path):
    """Upload a content file."""
    client = ctx.obj["client"]
    response = await client.async_upload_content(file_path)
    click.echo(response)
