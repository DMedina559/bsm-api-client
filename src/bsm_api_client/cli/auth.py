import click
from .config import Config
from bsm_api_client import BedrockServerManagerApi, AuthError


@click.group()
def auth():
    """Manages authentication."""
    pass


@auth.command()
@click.option(
    "--base-url", prompt=True, help="The base URL of the Bedrock Server Manager API."
)
@click.option(
    "--verify-ssl/--no-verify-ssl",
    is_flag=True,
    default=True,
    prompt=True,
    help="Enable/disable SSL verification.",
)
@click.option("--username", prompt=True, help="The username for authentication.")
@click.option(
    "--password", prompt=True, hide_input=True, help="The password for authentication."
)
@click.pass_context
async def login(ctx, base_url, username, password, verify_ssl):
    """Logs in to the Bedrock Server Manager API."""
    config = ctx.obj["config"]

    if base_url:
        config.set("base_url", base_url)

    config.set("verify_ssl", verify_ssl)

    client = BedrockServerManagerApi(
        base_url=config.base_url,
        username=username,
        password=password,
        verify_ssl=config.verify_ssl,
    )
    try:
        token = await client.authenticate()
        config.jwt_token = token.access_token
        click.echo("Login successful.")
    except AuthError as e:
        click.secho(f"Login failed: {e}", fg="red")
    finally:
        await client.close()


@auth.command()
@click.pass_context
async def logout(ctx):
    """Logs out from the Bedrock Server Manager API."""
    config = ctx.obj["config"]
    config.jwt_token = None
    click.echo("Logged out.")
