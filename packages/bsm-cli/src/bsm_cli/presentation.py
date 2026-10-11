"""Consistent terminal tables for dashboard data."""

import sys

from rich.console import Console
from rich.table import Table


def table(title, columns, rows):
    view = Table(
        title=title, title_justify="left", header_style="bold cyan", expand=False
    )
    for column in columns:
        view.add_column(column)
    for row in rows:
        view.add_row(
            *(str(value) if value is not None else "Unavailable" for value in row)
        )
    Console(file=sys.stdout, highlight=False).print(view)


def screen_header(title=None):
    """Render the same backend identity on every interactive screen."""
    import click

    ctx = click.get_current_context(silent=True)
    obj = ctx.obj if ctx and ctx.obj else {}
    info = obj.get("app_info", {})
    click.clear()
    version = info.get("app_version")
    heading = "Bedrock Server Manager"
    if version:
        heading += f" · {version}"
    click.secho(heading, fg="magenta", bold=True)
    if info.get("splash_text"):
        click.secho(info["splash_text"], fg="yellow")
    if title:
        click.secho(title, bold=True)
    click.echo()


async def load_header(ctx, client):
    if "app_info" in ctx.obj:
        return
    try:
        response = await client.application.async_get_info()
        info = response.info
        if isinstance(info, dict):
            ctx.obj["app_info"] = info
    except Exception:
        # Header metadata must never prevent access to the menu.
        pass
