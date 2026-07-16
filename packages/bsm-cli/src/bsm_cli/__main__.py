try:
    import click

except ImportError:
    print(
        "Please install the required dependencies with `pip install bsm-api-client[cli]`"
    )
    exit(1)


from contextlib import asynccontextmanager

from bsm_cli.account import account
from bsm_cli.addon import addon
from bsm_cli.allowlist import allowlist
from bsm_cli.auth import auth
from bsm_cli.backup import backup
from bsm_cli.bans import bans
from bsm_cli.config import Config
from bsm_cli.content import content
from bsm_cli.decorators import AsyncGroup
from bsm_cli.main_menus import main_menu
from bsm_cli.permissions import permissions
from bsm_cli.player import player
from bsm_cli.plugins import plugin
from bsm_cli.properties import properties
from bsm_cli.server import server
from bsm_cli.system import system
from bsm_cli.users import users
from bsm_cli.world import world

from bsm_api_client import BedrockServerManagerApi


@click.group(cls=AsyncGroup, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A CLI for managing Bedrock servers."""
    ctx.obj["cli"] = cli
    if ctx.invoked_subcommand is None:
        return main_menu(ctx)


@cli.context
@asynccontextmanager
async def cli_context(ctx):
    config = Config()
    ctx.obj["config"] = config

    try:
        client = BedrockServerManagerApi(
            base_url=config.base_url,
            jwt_token=config.jwt_token,
            verify_ssl=config.verify_ssl,
        )
    except ValueError as e:
        # Ignore AuthError when logging out or auth group is called
        if ctx.invoked_subcommand == auth or ctx.invoked_subcommand is None:
            client = None
        else:
            raise e
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
cli.add_command(bans)
cli.add_command(permissions)
cli.add_command(properties)
cli.add_command(system)
cli.add_command(world)
cli.add_command(account)
cli.add_command(content)
cli.add_command(users)

if __name__ == "__main__":
    cli()
