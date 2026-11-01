# src/bsm_cli/content.py
"""CLI commands for content management."""

from pathlib import Path

import click
import questionary

from bsm_cli.decorators import pass_async_context
from bsm_cli.output import emit, fail, get_client


@click.group()
def content():
    """Commands for managing content."""
    pass


@content.command("list")
@click.option(
    "-c",
    "--category",
    type=click.Choice(["worlds", "addons"]),
    default=None,
    help="Filter by content category.",
)
@pass_async_context
async def list_content(ctx, category):
    """List available world and addon files in the content library."""
    try:
        client = get_client(ctx)
        if category == "worlds":
            response = await client.content.async_get_content_worlds()
            return emit(ctx, response)
        if category == "addons":
            response = await client.content.async_get_content_addons()
            return emit(ctx, response)
        worlds = await client.content.async_get_content_worlds()
        addons = await client.content.async_get_content_addons()
        return emit(
            ctx,
            {
                "status": "success",
                "worlds": worlds.files or [],
                "addons": addons.files or [],
            },
        )
    except Exception as error:
        fail(error)


@content.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@pass_async_context
async def upload(ctx, file_path):
    """Upload a content file (.mcworld, .mcpack, .mcaddon)."""
    try:
        client = get_client(ctx)
        response = await client.content.async_upload_content(file_path)
        return emit(ctx, response)
    except Exception as error:
        fail(error)


@content.command("download")
@click.option(
    "-c",
    "--category",
    type=click.Choice(["worlds", "addons"]),
    required=True,
    help="Content category ('worlds' or 'addons').",
)
@click.option(
    "-f",
    "--file",
    "filename",
    required=True,
    help="Filename in the content category.",
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(path_type=Path),
    help="New destination file; existing files are preserved.",
)
@pass_async_context
async def download_content(ctx, category, filename, output):
    """Download a content file from the backend library."""
    try:
        client = get_client(ctx)
        saved = await client.content.async_download_content_to(
            category, filename, output
        )
        return emit(
            ctx,
            {
                "status": "success",
                "category": category,
                "filename": filename,
                "output": str(saved),
            },
        )
    except Exception as error:
        fail(error)


@content.command("delete")
@click.option(
    "-c",
    "--category",
    type=click.Choice(["worlds", "addons"]),
    required=True,
    help="Content category ('worlds' or 'addons').",
)
@click.option(
    "-f",
    "--file",
    "filename",
    required=True,
    help="Filename in the content category.",
)
@click.option("-y", "--yes", is_flag=True, help="Bypass the confirmation prompt.")
@pass_async_context
async def delete_content(ctx, category, filename, yes):
    """Delete a content file from the backend library."""
    try:
        client = get_client(ctx)
        if (
            not yes
            and not await questionary.confirm(
                f"Permanently delete '{filename}' from content/{category}?",
                default=False,
            ).ask_async()
        ):
            raise click.Abort()
        response = await client.content.async_delete_content(category, filename)
        return emit(ctx, response)
    except Exception as error:
        fail(error)
