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
@pass_async_context
async def list_tokens(ctx):
    """List metadata; credential secrets are never returned again."""
    return emit(
        ctx,
        await get_client(ctx).async_call_operation("list_integration_tokens"),
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
@pass_async_context
async def create_token(ctx, name, permission, server_id, expires_days):
    """Create a credential and print its secret once. Store the output securely."""
    result = await get_client(ctx).async_call_operation(
        "create_integration_token",
        json_data={
            "name": name,
            "permissions": list(permission),
            "server_ids": list(server_id) if server_id else None,
            "expires_in_days": expires_days,
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
