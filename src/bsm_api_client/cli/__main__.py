try:
    import click
    import questionary
except ImportError:
    print(
        "Please install the required dependencies with `pip install bsm-api-client[cli]`"
    )
    exit(1)

import asyncio
from contextlib import asynccontextmanager
from .config import Config
from bsm_api_client import BedrockServerManagerApi
from .auth import auth
from .server import server
from .addon import addon
from .backup import backup
from .player import player
from .plugins import plugin
from .allowlist import allowlist
from .permissions import permissions
from .properties import properties
from .system import system
from .world import world
from .account import account
from .content import content
from .main_menus import main_menu
from .decorators import AsyncGroup


@click.group(cls=AsyncGroup, invoke_without_command=True)
@click.pass_context
async def cli(ctx):
    """A CLI for managing Bedrock servers."""
    ctx.obj["cli"] = cli
    if ctx.invoked_subcommand is None:
        await main_menu(ctx)


@cli.context
@asynccontextmanager
async def cli_context(ctx):
    config = Config()
    ctx.obj["config"] = config

    client = BedrockServerManagerApi(
        base_url=config.base_url,
        jwt_token=config.jwt_token,
        verify_ssl=config.verify_ssl,
    )
    ctx.obj["client"] = client

    try:
        yield
    finally:
        if ctx.obj.get("client"):
            await ctx.obj["client"].close()


cli.add_command(auth)
cli.add_command(server)
cli.add_command(addon)
cli.add_command(backup)
cli.add_command(player)
cli.add_command(plugin)
cli.add_command(allowlist)
cli.add_command(permissions)
cli.add_command(properties)
cli.add_command(system)
cli.add_command(world)
cli.add_command(account)
cli.add_command(content)

if __name__ == "__main__":
    cli()
