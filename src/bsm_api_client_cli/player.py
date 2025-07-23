import click


@click.group()
def player():
    """Manages the central player database."""
    pass


@player.command("scan")
@click.pass_context
async def scan_for_players(ctx):
    """Scans all server logs to discover player gamertags and XUIDs."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        click.echo("Scanning all server logs for player data...")
        response = await client.async_scan_player_db()
        if response.status == "success":
            click.secho("Player database updated successfully.", fg="green")
        else:
            click.secho(f"Failed to scan for players: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred during scan: {e}", fg="red")


@player.command("add")
@click.option(
    "-p",
    "--player",
    "players",
    multiple=True,
    required=True,
    help="Player to add in 'Gamertag:XUID' format. Use multiple times for multiple players.",
)
@click.pass_context
async def add_players(ctx, players):
    """Manually adds or updates player entries in the central player database."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        player_list = list(players)
        click.echo(f"Adding/updating {len(player_list)} player(s) in the database...")
        response = await client.async_add_players_to_db(player_list)
        if response.status == "success":
            click.secho("Players added/updated successfully.", fg="green")
        else:
            click.secho(f"Failed to add players: {response.message}", fg="red")
    except Exception as e:
        click.secho(f"An error occurred while adding players: {e}", fg="red")
