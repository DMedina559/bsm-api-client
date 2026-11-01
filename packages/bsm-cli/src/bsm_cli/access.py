"""Named integration credentials and resource assignments."""

import click

from bsm_cli.decorators import pass_async_context
from bsm_cli.output import emit, get_client


@click.group()
def access():
    """Inspect and manage server-specific access."""


@access.command("servers")
@pass_async_context
async def servers(ctx):
    """List accessible servers and their immutable grant identifiers."""
    result = await get_client(ctx).async_call_operation("list_access_servers")
    return emit(ctx, result, columns=("id", "name", "permissions"))


@access.command("show")
@click.argument("user_id", type=int)
@pass_async_context
async def show(ctx, user_id):
    """Show an account's server assignments (administrator only)."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "get_account_server_access", path_params={"user_id": user_id}
        ),
    )


@access.command("set")
@click.argument("user_id", type=int)
@click.option("--mode", type=click.Choice(["all", "assigned"]), required=True)
@click.option(
    "--grant",
    multiple=True,
    help="SERVER_ID=permission,permission. Repeat for each server; replaces the grant set.",
)
@pass_async_context
async def set_access(ctx, user_id, mode, grant):
    """Replace server assignments (administrator only)."""
    grants = []
    for value in grant:
        identity, separator, permissions = value.partition("=")
        if not separator or not identity or not permissions:
            raise click.BadParameter(
                "Use SERVER_ID=permission,permission", param_hint="--grant"
            )
        grants.append({"server_id": identity, "permissions": permissions.split(",")})
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "set_account_server_access",
            path_params={"user_id": user_id},
            json_data={"mode": mode, "grants": grants},
        ),
    )


@click.group()
def tokens():
    """Manage your integration credentials without changing your login token."""


@tokens.command("list")
@click.option("--limit", type=click.IntRange(1, 500), default=100, show_default=True)
@click.option("--offset", type=click.IntRange(min=0), default=0, show_default=True)
@click.option(
    "--status", type=click.Choice(["all", "active", "inactive"]), default="all"
)
@pass_async_context
async def list_tokens(ctx, limit, offset, status):
    """List metadata; credential secrets are never returned again."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "list_integration_tokens",
            query={"limit": limit, "offset": offset, "status": status},
        ),
        columns=("id", "name", "expires_at", "revoked_at"),
    )


@tokens.command("create")
@click.option("--name", required=True)
@click.option(
    "--permission",
    multiple=True,
    default=("account:read", "health:read", "servers:read", "tasks:read"),
)
@click.option(
    "--server-id",
    multiple=True,
    help="Limit to immutable server IDs; omission uses the owner's permitted servers.",
)
@click.option(
    "--expires-days", type=click.IntRange(1, 365), default=30, show_default=True
)
@click.option("--never-expire", is_flag=True, help="Remain valid until revoked.")
@pass_async_context
async def create_token(ctx, name, permission, server_id, expires_days, never_expire):
    """Create a credential and print its secret once. Store the output securely."""
    result = await get_client(ctx).async_call_operation(
        "create_integration_token",
        json_data={
            "name": name,
            "permissions": list(permission),
            "server_ids": list(server_id) if server_id else None,
            "expires_in_days": None if never_expire else expires_days,
        },
    )
    return emit(ctx, result)


@tokens.command("revoke")
@click.argument("token_id")
@pass_async_context
async def revoke_token(ctx, token_id):
    """Revoke one integration credential, independently of the owner account."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "revoke_integration_token", path_params={"token_id": token_id}
        ),
    )


@click.group()
def sessions():
    """Inspect or revoke interactive login sessions."""


@sessions.command("list")
@pass_async_context
async def list_sessions(ctx):
    return emit(
        ctx,
        await get_client(ctx).async_call_operation("list_login_sessions"),
        columns=("id", "name", "current", "active", "last_seen_at", "expires_at"),
    )


@sessions.command("revoke")
@click.argument("session_id")
@pass_async_context
async def revoke_session(ctx, session_id):
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "revoke_login_session", path_params={"session_id": session_id}
        ),
    )


@sessions.command("revoke-all")
@click.option(
    "--include-current",
    is_flag=True,
    help="Also revoke the login running this command.",
)
@pass_async_context
async def revoke_sessions(ctx, include_current):
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "revoke_login_sessions",
            json_data={"mode": "all" if include_current else "others"},
        ),
    )


@tokens.command("rotate")
@click.argument("token_id")
@pass_async_context
async def rotate_token(ctx, token_id):
    """Immediately replace a credential; print its new secret once."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "rotate_integration_token", path_params={"token_id": token_id}
        ),
    )


@sessions.command("rename")
@click.argument("session_id")
@click.argument("name")
@pass_async_context
async def rename_session(ctx, session_id, name):
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "rename_login_session",
            path_params={"session_id": session_id},
            json_data={"name": name},
        ),
    )


@click.group()
def mfa():
    """Manage authenticator setup and one-use recovery codes."""


@mfa.command("status")
@pass_async_context
async def mfa_status(ctx):
    return emit(ctx, await get_client(ctx).async_call_operation("get_account_security"))


@mfa.command("enroll")
@pass_async_context
async def mfa_enroll(ctx):
    """Print a private setup key and URI; confirm with an authenticator code."""
    result = await get_client(ctx).async_call_operation("enroll_account_mfa")
    return emit(
        ctx,
        {"secret": result["secret"], "provisioning_uri": result["provisioning_uri"]},
    )


@mfa.command("confirm")
@click.option("--code", prompt=True, hide_input=True)
@pass_async_context
async def mfa_confirm(ctx, code):
    """Enable MFA and print the one-time recovery code set."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "confirm_account_mfa", json_data={"code": code}
        ),
    )


@mfa.command("disable")
@click.confirmation_option(
    prompt="Disable your second factor and sign out other sessions?"
)
@pass_async_context
async def mfa_disable(ctx):
    return emit(ctx, await get_client(ctx).async_call_operation("disable_account_mfa"))


@mfa.command("recovery-codes")
@click.confirmation_option(prompt="Replace all existing recovery codes?")
@pass_async_context
async def mfa_recovery(ctx):
    return emit(
        ctx, await get_client(ctx).async_call_operation("rotate_account_recovery_codes")
    )


@access.command("sessions")
@click.argument("user_id", type=int)
@pass_async_context
async def account_sessions(ctx, user_id):
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "list_account_login_sessions", path_params={"user_id": user_id}
        ),
        columns=("id", "name", "active", "last_seen_at"),
    )


@access.command("signout")
@click.argument("user_id", type=int)
@click.argument("session_id", required=False)
@click.option("--all", "all_sessions", is_flag=True)
@pass_async_context
async def account_signout(ctx, user_id, session_id, all_sessions):
    if bool(session_id) == all_sessions:
        raise click.UsageError("Supply SESSION_ID or --all")
    operation = (
        "revoke_account_login_sessions"
        if all_sessions
        else "revoke_account_login_session"
    )
    path: dict[str, int | str] = {"user_id": user_id}
    if session_id:
        path["session_id"] = session_id
    return emit(
        ctx, await get_client(ctx).async_call_operation(operation, path_params=path)
    )


@access.command("passkeys")
@click.argument("user_id", type=int)
@pass_async_context
async def account_passkeys(ctx, user_id):
    """List WebAuthn passkeys registered on an account (administrator only)."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "list_account_passkeys", path_params={"user_id": user_id}
        ),
        columns=(
            "id",
            "name",
            "active",
            "user_verified",
            "backup_state",
            "last_used_at",
            "created_at",
        ),
    )


@access.command("reset-mfa")
@click.argument("user_id", type=int)
@click.confirmation_option(
    prompt="Reset all MFA factors, recovery codes, passkeys, and sessions for this account?"
)
@pass_async_context
async def account_reset_mfa(ctx, user_id):
    """Reset an account's second factor, passkeys, and active sessions (administrator only)."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "reset_account_mfa", path_params={"user_id": user_id}
        ),
    )


@click.group()
def passkeys():
    """Inspect, rename, or revoke registered WebAuthn passkeys."""


@passkeys.command("list")
@pass_async_context
async def list_passkeys(ctx):
    """List WebAuthn passkeys registered on your account."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation("list_passkeys"),
        columns=(
            "id",
            "name",
            "active",
            "user_verified",
            "backup_state",
            "last_used_at",
            "created_at",
        ),
    )


@passkeys.command("rename")
@click.argument("passkey_id")
@click.argument("name")
@pass_async_context
async def rename_passkey(ctx, passkey_id, name):
    """Rename a passkey on your account."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "rename_passkey",
            path_params={"passkey_id": passkey_id},
            json_data={"name": name},
        ),
    )


@passkeys.command("revoke")
@click.argument("passkey_id")
@pass_async_context
async def revoke_passkey(ctx, passkey_id):
    """Revoke a passkey on your account."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation(
            "revoke_passkey", path_params={"passkey_id": passkey_id}
        ),
    )


@click.group()
def devices():
    """List and forget remembered second-factor devices; login sessions remain signed in."""


@devices.command("list")
@pass_async_context
async def list_devices(ctx):
    return emit(
        ctx,
        await get_client(ctx).async_call_operation("list_trusted_devices"),
        columns=("id", "name", "current", "status", "expires_at"),
    )


@devices.command("forget")
@click.argument("device_id", required=False)
@click.option("--all", "all_devices", is_flag=True)
@click.option("--others", is_flag=True)
@pass_async_context
async def forget_device(ctx, device_id, all_devices, others):
    if sum([bool(device_id), all_devices, others]) != 1:
        raise click.UsageError("Choose a device ID, --all, or --others.")
    if device_id:
        result = await get_client(ctx).async_call_operation(
            "revoke_trusted_device", path_params={"device_id": device_id}
        )
    else:
        result = await get_client(ctx).async_call_operation(
            "revoke_trusted_devices",
            json_data={"mode": "all" if all_devices else "others"},
        )
    config = ctx.obj["config"]
    proof = config.trusted_device()
    if proof and (
        all_devices or (device_id and proof.split(".")[0] == "bsm_td_" + device_id)
    ):
        config.update(
            trusted_device_token=None,
            trusted_device_expires_at=None,
            trusted_device_owner=None,
            trusted_device_backend=None,
        )
    return emit(ctx, result)
