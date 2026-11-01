"""Common integration-token and login-session workflows."""

import click

from bsm_cli.decorators import pass_async_context
from bsm_cli.output import emit, get_client


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
