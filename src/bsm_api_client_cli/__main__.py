import click
import asyncio
from contextlib import asynccontextmanager
from .config import Config
from bsm_api_client import BedrockServerManagerApi
from .auth import auth
from .server import server
from .addon import addon
from .backup import backup
from .cleanup import cleanup
from .player import player
from .plugins import plugin
from .allowlist import allowlist
from .permissions import permissions
from .properties import properties
from .system import system
from .world import world
from .main_menus import main_menu
from .decorators import AsyncGroup

@click.group(cls=AsyncGroup, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A CLI for managing Bedrock servers."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(main_menu)

@cli.context
@asynccontextmanager
async def cli_context(ctx):
    config = Config()
    ctx.obj["config"] = config

    if config.jwt_token:
        client = BedrockServerManagerApi(host=config.host, port=config.port, username="", password="")
        client._jwt_token = config.jwt_token
        ctx.obj["client"] = client
    else:
        ctx.obj["client"] = None
    
    try:
        yield
    finally:
        if ctx.obj.get("client"):
            await ctx.obj["client"].close()


cli.add_command(auth)
cli.add_command(server)
cli.add_command(addon)
cli.add_command(backup)
cli.add_command(cleanup)
cli.add_command(player)
cli.add_command(plugin)
cli.add_command(allowlist)
cli.add_command(permissions)
cli.add_command(properties)
cli.add_command(system)
cli.add_command(world)

if __name__ == "__main__":
    cli()
