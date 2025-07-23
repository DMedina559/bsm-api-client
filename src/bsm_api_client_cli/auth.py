import click
from .config import Config
from bsm_api_client import BedrockServerManagerApi, AuthError


@click.group()
def auth():
    """Manages authentication."""
    pass


@auth.command()
@click.option("--host", help="The host of the Bedrock Server Manager API.")
@click.option("--port", help="The port of the Bedrock Server Manager API.", type=int)
@click.option("--username", prompt=True, help="The username for authentication.")
@click.option(
    "--password", prompt=True, hide_input=True, help="The password for authentication."
)
@click.pass_context
async def login(ctx, host, port, username, password):
    """Logs in to the Bedrock Server Manager API."""
    config = ctx.obj["config"]

    if host:
        config.set("host", host)
    if port:
        config.set("port", port)

    client = BedrockServerManagerApi(
        host=config.host,
        port=config.port,
        username=username,
        password=password,
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
