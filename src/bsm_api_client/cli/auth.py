import click
from .config import Config
from bsm_api_client import BedrockServerManagerApi, AuthError


def _validate_and_get_url(url: str) -> str:
    """Validates and returns a url with a scheme."""
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"http://{url}"
    return url


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
@click.option("--username", help="The username for authentication.")
@click.option("--password", help="The password for authentication.")
@click.option("--token", help="The JWT token for authentication.")
@click.pass_context
async def login(ctx, base_url, username, password, verify_ssl, token):
    """Logs in to the Bedrock Server Manager API."""
    config = ctx.obj["config"]

    if base_url:
        validated_url = _validate_and_get_url(base_url)
        config.set("base_url", validated_url)

    config.set("verify_ssl", verify_ssl)

    if token:
        config.jwt_token = token
        click.echo("Token set.")
        return

    if not username and not password and not token:
        await interactive_login(ctx)
        return

    if username and not password:
        password = click.prompt("Password", hide_input=True)

    client = BedrockServerManagerApi(
        base_url=config.base_url,
        username=username,
        password=password,
        verify_ssl=config.verify_ssl,
    )
    try:
        token_data = await client.authenticate()
        config.jwt_token = token_data.access_token
        click.echo("Login successful.")
    except AuthError as e:
        click.secho(f"Login failed: {e}", fg="red")
    finally:
        await client.close()


async def interactive_login(ctx):
    """Handles the interactive login prompt."""
    config = ctx.obj["config"]
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    validated_url = _validate_and_get_url(config.base_url)
    if validated_url != config.base_url:
        config.set("base_url", validated_url)

    client = BedrockServerManagerApi(
        base_url=validated_url,
        username=username,
        password=password,
        verify_ssl=config.verify_ssl,
    )
    try:
        token_data = await client.authenticate()
        config.jwt_token = token_data.access_token
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
