import click

from bsm_cli.output import fail, get_client


@click.group()
def player():
    """Manages the central player database."""
    pass


@player.command("scan")
@click.pass_context
async def scan_for_players(ctx):
    """Scans all server logs to discover player gamertags and XUIDs."""
    client = get_client(ctx)

    try:
        click.echo("Scanning all server logs for player data...")
        response = await client.players.async_scan_players()
        if response.status == "success":
            click.secho("Player database updated successfully.", fg="green")
        else:
            click.secho(f"Failed to scan for players: {response.message}", fg="red")
    except Exception as e:
        fail(e)


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
    client = get_client(ctx)

    try:
        from bsm_api_client.models import AddPlayersPayload

        player_list = list(players)
        click.echo(f"Adding/updating {len(player_list)} player(s) in the database...")
        payload = AddPlayersPayload(players=player_list)
        response = await client.players.async_add_players(payload)
        if response.status == "success":
            click.secho("Players added/updated successfully.", fg="green")
        else:
            click.secho(f"Failed to add players: {response.message}", fg="red")
    except Exception as e:
        fail(e)
