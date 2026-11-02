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
    "--base-url",
    "--url",
    default=None,
    help="The base URL of the Bedrock Server Manager API (defaults to configured URL).",
)
@click.option(
    "--verify-ssl/--no-verify-ssl",
    is_flag=True,
    default=None,
    help="Enable/disable SSL verification (defaults to current setting).",
)
@click.option(
    "-k",
    "--insecure",
    is_flag=True,
    default=False,
    help="Disable SSL certificate verification (shorthand for --no-verify-ssl).",
)
@click.option("-u", "--username", help="The username for authentication.")
@click.option("-p", "--password", help="The password for authentication.")
@click.option(
    "--password-stdin",
    is_flag=True,
    default=False,
    help="Read the password from standard input.",
)
@click.option(
    "-t",
    "--token",
    help="A JWT or long-lived integration bearer credential (bsm_it_...).",
)
@click.option(
    "--with-token",
    is_flag=True,
    default=False,
    help="Read a bearer token from standard input or a hidden prompt.",
)
@click.option(
    "--long-lived",
    is_flag=True,
    default=False,
    help="Mint and store a long-lived integration token (bsm_it_...) after password sign-in.",
)
@click.option(
    "--token-name",
    default="BSM CLI",
    show_default=True,
    help="Name for the minted integration token when using --long-lived.",
)
@click.option(
    "--token-days",
    type=click.IntRange(1, 365),
    default=90,
    show_default=True,
    help="Validity in days for a minted --long-lived token.",
)
@click.option(
    "--never-expire",
    is_flag=True,
    default=False,
    help="Allow a minted --long-lived integration token to remain valid until revoked.",
)
@click.option(
    "--permission",
    "permissions",
    multiple=True,
    help="Restrict a minted --long-lived token to specific permissions.",
)
@click.option(
    "--otp", default="", help="Authenticator or one-use recovery code. Never saved."
)
@click.option(
    "--mfa",
    is_flag=True,
    default=False,
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
    default=False,
    help="Remember this second factor for 30 days after a fresh OTP. Your password remains required.",
)
@click.pass_context
async def login(  # noqa: C901
    ctx,
    base_url,
    verify_ssl,
    insecure,
    username,
    password,
    password_stdin,
    token,
    with_token,
    long_lived,
    token_name,
    token_days,
    never_expire,
    permissions,
    remember_me,
    otp,
    mfa,
    remember_device,
):
    """Sign in with username/password or a bearer/integration token.

    Use --token or --with-token to authenticate with an existing integration
    token (bsm_it_...), or --long-lived to mint a new integration token during
    password login.
    """
    config = ctx.obj["config"]
    if password_stdin and (password or token or with_token):
        raise click.UsageError(
            "Cannot combine --password-stdin with --password or token options."
        )
    if with_token and token:
        raise click.UsageError("Specify either --token or --with-token, not both.")
    if password_stdin:
        password = sys.stdin.read().rstrip("\r\n")
        if not password:
            raise click.UsageError("No password was provided on standard input.")
    if with_token:
        if not sys.stdin.isatty():
            token = sys.stdin.read().strip()
        else:
            token = click.prompt("API or integration token", hide_input=True).strip()
        if not token:
            raise click.UsageError("Token must not be empty.")

    interactive = (
        sys.stdin.isatty()
        and not ctx.obj.get("json_output")
        and not any((username, password, token, with_token, password_stdin))
    )
    if base_url is None and interactive:
        base_url = click.prompt("Base URL", default=config.base_url)

    resolved_verify_ssl = (
        False
        if insecure
        else (config.verify_ssl if verify_ssl is None else bool(verify_ssl))
    )

    if interactive and not long_lived and not remember_me and not mfa:
        method = click.prompt(
            "Authentication method",
            type=click.Choice(["password", "token"], case_sensitive=False),
            default="password",
        )
        if method.lower() == "token":
            token = click.prompt("API or integration token", hide_input=True).strip()
            if not token:
                raise click.UsageError("Token must not be empty.")

    if mfa and not token:
        otp = click.prompt("Authenticator or recovery code", hide_input=True)
    return await _login(
        ctx,
        base_url,
        username,
        password,
        resolved_verify_ssl,
        token,
        remember_me,
        otp,
        remember_device,
        long_lived=long_lived,
        token_name=token_name,
        token_days=token_days,
        never_expire=never_expire,
        permissions=permissions,
    )


async def _login(  # noqa: C901
    ctx,
    base_url,
    username,
    password,
    verify_ssl,
    token,
    remember_me=False,
    otp="",
    remember_device=False,
    *,
    long_lived=False,
    token_name="BSM CLI",
    token_days=90,
    never_expire=False,
    permissions=(),
):
    config = ctx.obj["config"]
    validated_url = _validate_and_get_url(base_url or config.base_url)
    resolved_verify_ssl = config.verify_ssl if verify_ssl is None else bool(verify_ssl)
    supplied_token = bool(token)
    device_values = {}
    resolved_username = username
    if supplied_token:
        token = token.strip()
        async with BedrockServerManagerApi(
            base_url=validated_url,
            jwt_token=token,
            verify_ssl=resolved_verify_ssl,
            client_name="BSM CLI",
        ) as client:
            account = await client.account.async_get_account_details()
            resolved_username = getattr(account, "username", None) or (
                account.get("username") if isinstance(account, dict) else None
            )
    else:
        username = username or click.prompt("Username")
        password = password or click.prompt("Password", hide_input=True)
        resolved_username = username
        async with BedrockServerManagerApi(
            base_url=validated_url,
            username=username,
            password=password,
            verify_ssl=resolved_verify_ssl,
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
            if long_lived:
                token_perms = list(permissions)
                if not token_perms:
                    try:
                        policy = await client.async_call_operation("get_access_policy")
                    except Exception:
                        policy = None
                    if isinstance(policy, dict) and policy.get("token_permissions"):
                        token_perms = list(policy["token_permissions"])
                    else:
                        token_perms = [
                            "account:read",
                            "health:read",
                            "servers:read",
                            "tasks:read",
                        ]
                created = await client.async_call_operation(
                    "create_integration_token",
                    json_data={
                        "name": token_name or "BSM CLI",
                        "permissions": token_perms,
                        "server_ids": None,
                        "expires_in_days": None if never_expire else token_days,
                    },
                )
                minted = (
                    created.get("token")
                    if isinstance(created, dict)
                    else getattr(created, "token", None)
                )
                if not minted:
                    raise AuthError(
                        "Backend did not return a minted integration token."
                    )
                try:
                    await client.async_logout()
                except Exception:
                    pass
                token = minted

    # Commit the destination and credentials together only after login succeeds.
    config.update(
        base_url=validated_url,
        verify_ssl=resolved_verify_ssl,
        jwt_token=token,
        active_username=resolved_username,
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
            "message": (
                "Token set."
                if supplied_token
                else (
                    "Long-lived integration token created and saved."
                    if long_lived
                    else "Login successful."
                )
            ),
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


@auth.command("status")
@click.pass_context
async def status(ctx):
    """Show local authentication status and credential storage details."""
    config = ctx.obj["config"]
    token = config.jwt_token
    credential_type = (
        "integration_token"
        if isinstance(token, str) and token.startswith("bsm_it_")
        else ("session_jwt" if token else None)
    )
    return emit(
        ctx,
        {
            "authenticated": bool(token),
            "base_url": config.base_url,
            "verify_ssl": config.verify_ssl,
            "active_username": config.get("active_username"),
            "credential_type": credential_type,
            "credential_store": getattr(config, "credential_store", "file"),
            "trusted_device_remembered": bool(config.trusted_device()),
        },
    )


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
