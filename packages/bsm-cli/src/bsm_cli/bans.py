import click
import questionary

from bsm_api_client.models import BanAddRequest, BanRemoveRequest


@click.group()
def bans():
    """Manages the server ban list."""
    pass


@bans.command("list")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server.",
)
@click.pass_context
async def list_bans(ctx, server_name: str):
    """Lists all players on the server's ban list."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.echo(f"Fetching ban list for server '{server_name}'...")
    response = await client.async_get_server_bans(server_name)

    if response.get("status") == "success":
        bans_list = response.get("bans", [])
        if not bans_list:
            click.secho("The ban list is empty.", fg="green")
        else:
            click.secho(f"\n--- Ban List for '{server_name}' ---", bold=True)
            for entry in bans_list:
                click.echo(
                    f"- {click.style(entry.get('player_name', 'Unknown'), fg='cyan')} (XUID: {entry.get('xuid')}) - Reason: {entry.get('reason', 'N/A')}"
                )
    else:
        click.secho(
            f"Failed to fetch ban list: {response.get('message', 'Unknown Error')}",
            fg="red",
        )


@bans.command("add")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server.",
)
@click.pass_context
async def add_ban(ctx, server_name: str):
    """Adds a player to the server ban list interactively."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    await interactive_ban_workflow(client, server_name)


@bans.command("remove")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server.",
)
@click.pass_context
async def remove_ban(ctx, server_name: str):
    """Removes a player from the server ban list interactively."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    response = await client.async_get_server_bans(server_name)
    if response.get("status") != "success":
        click.secho(
            f"Failed to fetch ban list: {response.get('message', 'Unknown Error')}",
            fg="red",
        )
        return

    bans_list = response.get("bans", [])
    if not bans_list:
        click.secho("The ban list is currently empty.", fg="yellow")
        return

    choices = [
        questionary.Choice(
            title=f"{entry.get('player_name', 'Unknown')} ({entry.get('xuid')})",
            value=entry.get("xuid"),
        )
        for entry in bans_list
    ]

    selected_xuid = await questionary.select(
        "Select a player to remove from the ban list:", choices=choices
    ).ask_async()

    if not selected_xuid:
        return

    confirm = await questionary.confirm(
        f"Are you sure you want to remove XUID '{selected_xuid}' from the ban list?"
    ).ask_async()
    if not confirm:
        click.secho("Operation cancelled.", fg="yellow")
        return

    payload = BanRemoveRequest(xuid=selected_xuid)

    click.echo(
        f"Removing XUID '{selected_xuid}' from the ban list for '{server_name}'..."
    )
    rem_response = await client.async_remove_server_ban(server_name, payload)

    if rem_response.get("status") == "success":
        click.secho("Player successfully removed from the ban list.", fg="green")
    else:
        click.secho(
            f"Failed to remove player from ban list: {rem_response.get('message', 'Unknown Error')}",
            fg="red",
        )


async def interactive_ban_workflow(client, server_name: str):
    """Guides the user through an interactive session to view and add players to the ban list."""
    response = await client.async_get_server_bans(server_name)
    existing_bans = response.get("bans", [])

    click.secho("\n--- Interactive Ban List Configuration ---", bold=True)
    if existing_bans:
        click.echo("Current players in ban list:")
        for b in existing_bans:
            click.echo(
                f"  - {b.get('player_name')} (XUID: {b.get('xuid')}) - Reason: {b.get('reason', 'N/A')}"
            )
    else:
        click.secho("Ban list is currently empty.", fg="yellow")

    click.echo("\nEnter a new player to ban. Leave Gamertag empty to finish.")
    while True:
        player_name = await questionary.text("Player gamertag:").ask_async()
        if not player_name or not player_name.strip():
            break

        xuid = await questionary.text("Player XUID:").ask_async()
        if not xuid or not xuid.strip():
            click.secho("XUID is required to ban a player.", fg="red")
            continue

        reason = await questionary.text("Reason (optional):").ask_async()

        if any(b.get("xuid") == xuid.strip() for b in existing_bans):
            click.secho(
                f"Player with XUID '{xuid}' is already in the list. Skipping.",
                fg="yellow",
            )
            continue

        payload = BanAddRequest(
            player_name=player_name.strip(),
            xuid=xuid.strip(),
            reason=reason.strip() if reason.strip() else None,
        )
        res = await client.async_add_server_ban(server_name, payload)
        if res.get("status") == "success":
            click.secho(f"Successfully banned {player_name}.", fg="green")
            existing_bans.append(
                {
                    "player_name": player_name.strip(),
                    "xuid": xuid.strip(),
                    "reason": reason.strip() if reason.strip() else None,
                }
            )
        else:
            click.secho(
                f"Failed to ban player: {res.get('message', 'Unknown Error')}", fg="red"
            )

    click.secho("Ban list interactive configuration finished.", fg="green")
