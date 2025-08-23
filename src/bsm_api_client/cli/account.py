# src/bsm_api_client/cli/account.py
"""CLI commands for account management."""
import click
from .decorators import pass_async_context


@click.group()
def account():
    """Commands for managing your account."""
    pass


@account.command()
@pass_async_context
async def details(ctx):
    """Get your account details."""
    client = ctx.obj["client"]
    details = await client.async_get_account_details()
    click.echo(details.model_dump_json(indent=2))


@account.command()
@click.option("--theme", prompt="Theme name", help="The name of the theme to set.")
@pass_async_context
async def update_theme(ctx, theme):
    """Update your theme."""
    from bsm_api_client.models import ThemeUpdate

    client = ctx.obj["client"]
    payload = ThemeUpdate(theme=theme)
    response = await client.async_update_theme(payload)
    click.echo(response.model_dump_json(indent=2))


@account.command()
@click.option("--full-name", prompt="Full Name", help="Your full name.")
@click.option("--email", prompt="Email", help="Your email address.")
@pass_async_context
async def update_profile(ctx, full_name, email):
    """Update your profile."""
    from bsm_api_client.models import ProfileUpdate

    client = ctx.obj["client"]
    payload = ProfileUpdate(full_name=full_name, email=email)
    response = await client.async_update_profile(payload)
    click.echo(response.model_dump_json(indent=2))


@account.command()
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
@pass_async_context
async def change_password(ctx, current_password, new_password):
    """Change your password."""
    from bsm_api_client.models import ChangePasswordRequest

    client = ctx.obj["client"]
    payload = ChangePasswordRequest(
        current_password=current_password, new_password=new_password
    )
    response = await client.async_change_password(payload)
    click.echo(response.model_dump_json(indent=2))
