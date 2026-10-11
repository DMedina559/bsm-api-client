"""Persistent terminal display preferences."""

import click


@click.group()
def appearance():
    """Configure terminal units and layout density."""


@appearance.command("show")
@click.pass_context
async def show(ctx):
    config = ctx.obj["config"]
    values = {
        "memory_unit": config.get("memory_unit", "auto"),
        "density": config.get("density", "comfortable"),
    }
    for key, value in values.items():
        click.echo(f"{key.replace('_', ' ')}: {value}")
    return values


@appearance.command("set")
@click.option("--memory-unit", type=click.Choice(["auto", "MB", "GB", "TB"]))
@click.option("--density", type=click.Choice(["comfortable", "compact"]))
@click.pass_context
async def configure(ctx, memory_unit, density):
    changes = {}
    if memory_unit:
        changes["memory_unit"] = memory_unit
    if density:
        changes["density"] = density
    ctx.obj["config"].update(**changes)
    click.echo("Display preferences saved.")
    return changes


def preferred_unit(ctx, unit):
    value = unit or ctx.obj["config"].get("memory_unit", "auto")
    return value if value in {"auto", "MB", "GB", "TB"} else "auto"


def comfortable():
    ctx = click.get_current_context(silent=True)
    return (
        not ctx
        or not ctx.obj
        or ctx.obj.get("config") is None
        or ctx.obj["config"].get("density", "comfortable") != "compact"
    )
