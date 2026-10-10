import click

from bsm_api_client import BedrockServerManagerApi
from bsm_cli.output import emit


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
    return await _login(ctx, base_url, username, password, verify_ssl, token)


async def _login(ctx, base_url, username, password, verify_ssl, token):
    config = ctx.obj["config"]
    validated_url = _validate_and_get_url(base_url or config.base_url)
    supplied_token = bool(token)
    if not token:
        username = username or click.prompt("Username")
        password = password or click.prompt("Password", hide_input=True)
        async with BedrockServerManagerApi(
            base_url=validated_url,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
        ) as client:
            token = (await client.authenticate()).access_token

    # Commit the destination and credentials together only after login succeeds.
    config.update(
        base_url=validated_url,
        verify_ssl=verify_ssl,
        jwt_token=token,
        username=None,
        password=None,
        openapi_cache=None,
        server_cache=None,
    )
    return emit(
        ctx,
        {
            "status": "success",
            "message": "Token set." if supplied_token else "Login successful.",
        },
    )


async def interactive_login(ctx):
    """Use the same login path from interactive menus."""
    config = ctx.obj["config"]
    return await _login(ctx, config.base_url, None, None, config.verify_ssl, None)


@auth.command()
@click.pass_context
async def logout(ctx):
    """Logs out from the Bedrock Server Manager API."""
    config = ctx.obj["config"]
    config.update(jwt_token=None, username=None, password=None)
    result = {"status": "success", "message": "Logged out."}
    if "client" in ctx.obj and ctx.obj["client"]:
        await ctx.obj["client"].close()
    return emit(ctx, result)
