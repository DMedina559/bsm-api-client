import click
from .decorators import pass_async_context
import questionary


@click.group()
def users():
    """Commands for managing users."""
    pass


@users.command()
@pass_async_context
async def list(ctx):
    """List all users."""
    client = ctx.obj["client"]
    users = await client.async_get_users()
    for user in users:
        click.echo(
            f"ID: {user.id} | Username: {user.username} | Role: {user.role} | Active: {user.is_active} | Type: {user.identity_type}"
        )


@users.command()
@click.argument("user_id", type=int)
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
@pass_async_context
async def delete(ctx, user_id: int, yes: bool):
    """Delete a user."""
    client = ctx.obj["client"]
    if not yes:
        confirm = await questionary.confirm(
            f"Are you sure you want to delete user {user_id}?"
        ).ask_async()
        if not confirm:
            click.echo("Aborted.")
            return

    response = await client.async_delete_user(user_id)
    click.echo(response.model_dump_json(indent=2))


@users.command()
@click.argument("user_id", type=int)
@click.argument("role", type=click.Choice(["user", "moderator", "admin"]))
@pass_async_context
async def set_role(ctx, user_id: int, role: str):
    """Set a user's role."""
    client = ctx.obj["client"]
    response = await client.async_update_user_role(user_id, role)
    click.echo(response.model_dump_json(indent=2))


@users.command()
@click.argument("user_id", type=int)
@pass_async_context
async def enable(ctx, user_id: int):
    """Enable a user account."""
    client = ctx.obj["client"]
    response = await client.async_enable_user(user_id)
    click.echo(response.model_dump_json(indent=2))


@users.command()
@click.argument("user_id", type=int)
@pass_async_context
async def disable(ctx, user_id: int):
    """Disable a user account."""
    client = ctx.obj["client"]
    response = await client.async_disable_user(user_id)
    click.echo(response.model_dump_json(indent=2))


@users.command()
@click.argument("role", type=click.Choice(["user", "moderator", "admin"]))
@pass_async_context
async def invite(ctx, role: str):
    """Generate an invite link for a new user."""
    client = ctx.obj["client"]
    response = await client.async_generate_invite_token(role)
    click.echo(response)
