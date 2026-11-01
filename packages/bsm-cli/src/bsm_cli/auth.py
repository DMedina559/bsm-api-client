import sys

import click

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.exceptions import AuthError
from bsm_cli.output import emit, get_client


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
@click.option("--token", help="A JWT or named integration bearer credential.")
@click.option(
    "--otp", default="", help="Authenticator or one-use recovery code. Never saved."
)
@click.option(
    "--mfa",
    is_flag=True,
    help="Enter an authenticator or recovery code in a hidden prompt.",
)
@click.option(
    "--remember-me",
    is_flag=True,
    default=False,
    help="Request a longer-lived token when signing in with username and password.",
)
@click.option(
    "--remember-device",
    is_flag=True,
    help="Remember this second factor for 30 days after a fresh OTP. Your password remains required.",
)
@click.pass_context
async def login(
    ctx,
    base_url,
    username,
    password,
    verify_ssl,
    token,
    remember_me,
    otp,
    mfa,
    remember_device,
):
    """Sign in; --remember-me requests the backend-configured longer token lifetime.

    A supplied --token keeps its existing expiry.
    """
    if mfa and not token:
        otp = click.prompt("Authenticator or recovery code", hide_input=True)
    return await _login(
        ctx,
        base_url,
        username,
        password,
        verify_ssl,
        token,
        remember_me,
        otp,
        remember_device,
    )


async def _login(
    ctx,
    base_url,
    username,
    password,
    verify_ssl,
    token,
    remember_me=False,
    otp="",
    remember_device=False,
):
    config = ctx.obj["config"]
    validated_url = _validate_and_get_url(base_url or config.base_url)
    supplied_token = bool(token)
    device_values = {}
    if not token:
        username = username or click.prompt("Username")
        password = password or click.prompt("Password", hide_input=True)
        async with BedrockServerManagerApi(
            base_url=validated_url,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            client_name="BSM CLI",
            remember_me=remember_me,
            **({"otp": otp} if otp else {}),
            **({"remember_device": True} if remember_device else {}),
            **(
                {"trusted_device_token": config.trusted_device(username, validated_url)}
                if config.trusted_device(username, validated_url)
                else {}
            ),
        ) as client:
            try:
                authenticated = await client.authenticate()
            except AuthError as failure:
                if failure.passkey_required:
                    raise click.ClickException(
                        "This account requires a passkey. Sign in through the web UI; the CLI does not implement WebAuthn."
                    ) from None
                if (
                    not failure.mfa_required
                    or otp
                    or ctx.obj.get("json_output")
                    or not sys.stdin.isatty()
                ):
                    raise
                # Retry only the explicit login challenge, never a failed mutation.
                code = click.prompt("Authenticator or recovery code", hide_input=True)
                authenticated = await client.authenticate(otp=code)
            token = authenticated.access_token
            if remember_device and isinstance(authenticated.trusted_device_token, str):
                device_values = {
                    "trusted_device_token": authenticated.trusted_device_token,
                    "trusted_device_expires_at": authenticated.trusted_device_expires_at,
                    "trusted_device_owner": username,
                    "trusted_device_backend": validated_url,
                }

    # Commit the destination and credentials together only after login succeeds.
    config.update(
        base_url=validated_url,
        verify_ssl=verify_ssl,
        jwt_token=token,
        active_username=None if supplied_token else username,
        **device_values,
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
    remember_me = click.confirm("Request a longer-lived login token?", default=False)
    return await _login(
        ctx, config.base_url, None, None, config.verify_ssl, None, remember_me
    )


@auth.command()
@click.pass_context
async def logout(ctx):
    """Logs out from the Bedrock Server Manager API."""
    config = ctx.obj["config"]
    result = {"status": "success", "message": "Logged out."}
    token = config.jwt_token
    client = ctx.obj.get("client")
    try:
        if client:
            await client.async_logout()
        elif token:
            async with BedrockServerManagerApi(
                base_url=config.base_url,
                jwt_token=token,
                verify_ssl=config.verify_ssl,
                client_name="BSM CLI",
            ) as temporary:
                await temporary.async_logout()
    finally:
        config.update(
            jwt_token=None, username=None, password=None, active_username=None
        )
        if client:
            await client.close()
    return emit(ctx, result)


@auth.command("setup")
@click.option(
    "--base-url", prompt=True, help="The base URL of a new manager installation."
)
@click.option("--verify-ssl/--no-verify-ssl", default=True)
@click.option("--username", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.pass_context
async def setup(ctx, base_url, verify_ssl, username, password):
    """Create the first administrator and securely save the session token."""
    from bsm_api_client.models import UserLoginPayload

    url = _validate_and_get_url(base_url)
    async with BedrockServerManagerApi(
        url,
        username=username,
        password=password,
        verify_ssl=verify_ssl,
        client_name="BSM CLI",
    ) as client:
        if not (await client.application.async_get_setup_status()).needs_setup:
            raise click.ClickException("Setup is already complete. Use auth login.")
        response = await client.application.async_create_first_user(
            UserLoginPayload(username=username, password=password)
        )
    ctx.obj["config"].update(
        base_url=url,
        verify_ssl=verify_ssl,
        jwt_token=response.access_token,
        active_username=username,
        username=None,
        password=None,
        openapi_cache=None,
        server_cache=None,
    )
    return emit(
        ctx, {"status": "success", "message": "Administrator created. Logged in."}
    )


@auth.command("verify")
@click.option("--password", prompt=True, hide_input=True)
@click.option("--otp", default="", help="Authenticator or recovery code, if enabled.")
@click.option(
    "--mfa",
    is_flag=True,
    help="Prompt privately for an authenticator or recovery code.",
)
@click.option(
    "--remember-device",
    is_flag=True,
    help="Remember this second factor after a fresh OTP.",
)
@click.pass_context
async def verify(ctx, password, otp, mfa, remember_device):
    """Verify the existing session for five minutes of security management."""
    if mfa:
        otp = click.prompt("Authenticator or recovery code", hide_input=True)
    account = (
        await get_client(ctx).async_call_operation("get_account")
        if remember_device
        else None
    )
    payload = {
        "password": password,
        "otp": otp,
        **({"remember_device": True} if remember_device else {}),
    }
    try:
        result = await get_client(ctx).async_call_operation(
            "verify_account_security", json_data=payload
        )
    except AuthError as failure:
        if failure.passkey_required:
            raise click.ClickException(
                "Verify this account with a passkey in the web UI; the CLI does not implement WebAuthn."
            ) from None
        if (
            not failure.mfa_required
            or otp
            or ctx.obj.get("json_output")
            or not sys.stdin.isatty()
        ):
            raise
        payload["otp"] = click.prompt("Authenticator or recovery code", hide_input=True)
        result = await get_client(ctx).async_call_operation(
            "verify_account_security", json_data=payload
        )
    credential = result.pop("trusted_device_token", None)
    if credential and account:
        config = ctx.obj["config"]
        username = account["username"]
        config.update(
            trusted_device_token=credential,
            trusted_device_expires_at=result.get("trusted_device_expires_at"),
            trusted_device_owner=username,
            trusted_device_backend=config.base_url,
            active_username=username,
        )
    return emit(ctx, result)


@auth.command("whoami")
@click.pass_context
async def details(ctx):
    """Get your account details."""
    client = get_client(ctx)
    details = await client.account.async_get_account_details()
    return emit(ctx, details)


@auth.command("change-password")
@click.option(
    "--current-password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=False,
    help="Your current password.",
)
@click.option(
    "--new-password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Your new password.",
)
@click.pass_context
async def change_password(ctx, current_password, new_password):
    """Change your password."""
    from bsm_api_client.models import ChangePasswordPayload

    client = get_client(ctx)
    payload = ChangePasswordPayload(
        current_password=current_password, new_password=new_password
    )
    response = await client.account.async_change_password(payload)
    return emit(ctx, response)
