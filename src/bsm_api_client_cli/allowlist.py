import click
import questionary
from bsm_api_client.models import AllowlistAddPayload, AllowlistRemovePayload


@click.group()
def allowlist():
    """Manages a server's player allowlist."""
    pass


@allowlist.command("add")
@click.option(
    "-s", "--server", "server_name", required=True, help="The name of the server."
)
@click.option(
    "-p",
    "--player",
    "players",
    multiple=True,
    help="Gamertag of the player to add. Use multiple times for multiple players.",
)
@click.option(
    "--ignore-limit",
    is_flag=True,
    help="Allow player(s) to join even if the server is full.",
)
@click.pass_context
async def add(ctx, server_name: str, players: tuple[str], ignore_limit: bool):
    """Adds one or more players to a server's allowlist."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        if not players:
            click.secho(
                f"No player specified; starting interactive editor for '{server_name}'...",
                fg="yellow",
            )
            await interactive_allowlist_workflow(client, server_name)
            return

        payload = AllowlistAddPayload(
            players=list(players), ignoresPlayerLimit=ignore_limit
        )
        response = await client.async_add_server_allowlist(server_name, payload)

        message = response.message
        click.secho(
            message,
            fg="green",
        )

    except Exception as e:
        click.secho(f"\nAn error occurred: {e}", fg="red")


@allowlist.command("remove")
@click.option(
    "-s", "--server", "server_name", required=True, help="The name of the server."
)
@click.option(
    "-p",
    "--player",
    "players",
    multiple=True,
    required=True,
    help="Gamertag of the player to remove. Use multiple times for multiple players.",
)
@click.pass_context
async def remove(ctx, server_name: str, players: tuple[str]):
    """Removes one or more players from a server's allowlist."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    player_list = list(players)
    click.echo(
        f"Removing {len(player_list)} player(s) from '{server_name}' allowlist..."
    )

    payload = AllowlistRemovePayload(players=player_list)
    response = await client.async_remove_server_allowlist_players(server_name, payload)

    if response.status == "success":
        details = response.details or {}
        removed_players = details["removed"] or []
        not_found_players = details["not_found"] or []

        message = response.message
        click.secho(message, fg="cyan" if not removed_players else "green")

        if removed_players:
            click.secho(
                f"\nSuccessfully removed {len(removed_players)} player(s):", fg="green"
            )
            for p_name in removed_players:
                click.echo(f"  - {p_name}")
        if not_found_players:
            click.secho(
                f"\n{len(not_found_players)} player(s) were not found in the allowlist:",
                fg="yellow",
            )
            for p_name in not_found_players:
                click.echo(f"  - {p_name}")
    else:
        click.secho(
            f"Failed to remove players from allowlist: {response.message}", fg="red"
        )


@allowlist.command("list")
@click.option(
    "-s", "--server", "server_name", required=True, help="The name of the server."
)
@click.pass_context
async def list_players(ctx, server_name: str):
    """Lists all players currently on a server's allowlist."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    response = await client.async_get_server_allowlist(server_name)

    if response.status == "success":
        players = response.data.get("existing_players", [])
        if not players:
            click.secho(
                f"The allowlist for server '{server_name}' is empty.", fg="yellow"
            )
            return

        click.secho(f"\nAllowlist for '{server_name}':", bold=True)
        for p in players:
            limit_str = (
                click.style(" (Ignores Player Limit)", fg="yellow")
                if p.get("ignoresPlayerLimit")
                else ""
            )
            click.echo(f"  - {p.get('name')}{limit_str}")
    else:
        click.secho(f"Failed to list allowlist: {response.message}", fg="red")


async def interactive_allowlist_workflow(client, server_name: str):
    """Guides the user through an interactive session to view and add players to the allowlist."""
    response = await client.async_get_server_allowlist(server_name)
    existing_players = response.players or []

    click.secho("\n--- Interactive Allowlist Configuration ---", bold=True)
    if existing_players:
        click.echo("Current players in allowlist:")
        for p in existing_players:
            limit_str = (
                click.style(" (Ignores Limit)", fg="yellow")
                if p.get("ignoresPlayerLimit")
                else ""
            )
            click.echo(f"  - {p.get('name')}{limit_str}")
    else:
        click.secho("Allowlist is currently empty.", fg="yellow")

    new_players_to_add = []
    click.echo("\nEnter new players to add. Press Enter on an empty line to finish.")
    while True:
        player_name = await questionary.text("Player gamertag:").ask_async()
        if not player_name or not player_name.strip():
            break

        if any(
            p["name"].lower() == player_name.lower()
            for p in existing_players + new_players_to_add
        ):
            click.secho(
                f"Player '{player_name}' is already in the list. Skipping.", fg="yellow"
            )
            continue

        ignore_limit = await questionary.confirm(
            f"Should '{player_name}' ignore the player limit?", default=False
        ).ask_async()
        new_players_to_add.append({"name": player_name.strip(), "ignoresPlayerLimit": ignore_limit})

    if new_players_to_add:
        # The interactive mode will add all players with their specified ignore limit.
        # We need to group them by the ignore limit flag and make separate API calls.
        players_ignore_limit = [p["name"] for p in new_players_to_add if p["ignoresPlayerLimit"]]
        players_no_ignore_limit = [p["name"] for p in new_players_to_add if not p["ignoresPlayerLimit"]]

        if players_ignore_limit:
            click.echo("Adding players with ignore limit...")
            payload = AllowlistAddPayload(players=players_ignore_limit, ignoresPlayerLimit=True)
            response = await client.async_add_server_allowlist(server_name, payload)
            if response.status != "success":
                click.secho(f"Failed to add players with ignore limit: {response.message}", fg="red")
        
        if players_no_ignore_limit:
            click.echo("Adding players without ignore limit...")
            payload = AllowlistAddPayload(players=players_no_ignore_limit, ignoresPlayerLimit=False)
            response = await client.async_add_server_allowlist(server_name, payload)
            if response.status != "success":
                click.secho(f"Failed to add players without ignore limit: {response.message}", fg="red")

        click.secho("Allowlist updated.", fg="green")
    else:
        click.secho("No new players were added.", fg="cyan")
