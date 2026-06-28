import click
import questionary
from bsm_cli.decorators import pass_async_context


async def interactive_user_workflow(ctx, client):  # noqa: C901
    """Interactive menu for managing users."""
    while True:
        try:
            users_list = await client.async_get_users()
            click.clear()
            click.secho("--- Manage Users ---", fg="magenta", bold=True)
            for user in users_list:
                click.echo(
                    f"ID: {user.id} | Username: {user.username} | Role: {user.role} | Active: {user.is_active} | Type: {user.identity_type}"
                )

            choices = [
                "List Users",
                "Delete User",
                "Set User Role",
                "Enable User",
                "Disable User",
                "Generate Invite Link",
                "Back",
            ]
            choice = await questionary.select(
                "\nChoose an action:",
                choices=choices,
                use_indicator=True,
            ).ask_async()

            if choice is None or choice == "Back":
                return

            if choice == "List Users":
                click.echo("\nUsers List:")
                for user in users_list:
                    click.echo(
                        f"ID: {user.id} | Username: {user.username} | Role: {user.role} | Active: {user.is_active} | Type: {user.identity_type}"
                    )
                await questionary.press_any_key_to_continue().ask_async()

            elif choice == "Delete User":
                if not users_list:
                    click.secho("No users found.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                user_choices = [
                    questionary.Choice(title=f"{u.username} (ID: {u.id})", value=u.id)
                    for u in users_list
                ]
                user_choices.append(questionary.Choice(title="Cancel", value="Cancel"))

                user_id = await questionary.select(
                    "Select user to delete:", choices=user_choices
                ).ask_async()

                if user_id and user_id != "Cancel":
                    confirm = await questionary.confirm(
                        f"Are you sure you want to delete user {user_id}?"
                    ).ask_async()
                    if confirm:
                        response = await client.async_delete_user(user_id)
                        click.echo(response.model_dump_json(indent=2))
                        await questionary.press_any_key_to_continue().ask_async()

            elif choice == "Set User Role":
                if not users_list:
                    click.secho("No users found.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                user_choices = [
                    questionary.Choice(title=f"{u.username} (ID: {u.id})", value=u.id)
                    for u in users_list
                ]
                user_choices.append(questionary.Choice(title="Cancel", value="Cancel"))

                user_id = await questionary.select(
                    "Select user to modify:", choices=user_choices
                ).ask_async()

                if user_id and user_id != "Cancel":
                    role = await questionary.select(
                        "Select new role:",
                        choices=["user", "moderator", "admin"],
                    ).ask_async()
                    if role:
                        response = await client.async_update_user_role(user_id, role)
                        click.echo(response.model_dump_json(indent=2))
                        await questionary.press_any_key_to_continue().ask_async()

            elif choice == "Enable User":
                if not users_list:
                    click.secho("No users found.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                disabled_users = [u for u in users_list if not u.is_active]
                if not disabled_users:
                    click.secho("No disabled users found.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                user_choices = [
                    questionary.Choice(title=f"{u.username} (ID: {u.id})", value=u.id)
                    for u in disabled_users
                ]
                user_choices.append(questionary.Choice(title="Cancel", value="Cancel"))

                user_id = await questionary.select(
                    "Select user to enable:", choices=user_choices
                ).ask_async()

                if user_id and user_id != "Cancel":
                    response = await client.async_enable_user(user_id)
                    click.echo(response.model_dump_json(indent=2))
                    await questionary.press_any_key_to_continue().ask_async()

            elif choice == "Disable User":
                if not users_list:
                    click.secho("No users found.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                enabled_users = [u for u in users_list if u.is_active]
                if not enabled_users:
                    click.secho("No enabled users found.", fg="yellow")
                    await questionary.press_any_key_to_continue().ask_async()
                    continue

                user_choices = [
                    questionary.Choice(title=f"{u.username} (ID: {u.id})", value=u.id)
                    for u in enabled_users
                ]
                user_choices.append(questionary.Choice(title="Cancel", value="Cancel"))

                user_id = await questionary.select(
                    "Select user to disable:", choices=user_choices
                ).ask_async()

                if user_id and user_id != "Cancel":
                    response = await client.async_disable_user(user_id)
                    click.echo(response.model_dump_json(indent=2))
                    await questionary.press_any_key_to_continue().ask_async()

            elif choice == "Generate Invite Link":
                role = await questionary.select(
                    "Select role for invite:",
                    choices=["user", "moderator", "admin"],
                ).ask_async()
                if role:
                    response = await client.async_generate_invite_token(role)
                    click.echo(f"Invite Link: {response.registration_url}")
                    await questionary.press_any_key_to_continue().ask_async()

        except Exception as e:
            click.secho(f"An error occurred: {e}", fg="red")
            await questionary.press_any_key_to_continue().ask_async()


@click.group(invoke_without_command=True)
@click.pass_context
async def users(ctx):
    """Commands for managing users."""
    if ctx.invoked_subcommand is None:
        client = ctx.obj.get("client")
        if not client:
            click.secho("You are not logged in.", fg="red")
            return
        await interactive_user_workflow(ctx, client)


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
    click.echo(f"Invite Link: {response.registration_url}")
