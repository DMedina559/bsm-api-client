import click
import questionary
from bsm_api_client.models import PermissionsSetPayload


@click.group()
def permissions():
    """Manages player permission levels on a server."""
    pass


@permissions.command("set")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="The name of the target server.",
)
@click.option(
    "-p",
    "--player",
    "player_name",
    help="The gamertag of the player. Skips interactive mode.",
)
@click.option(
    "-l",
    "--level",
    type=click.Choice(["visitor", "member", "operator"], case_sensitive=False),
    help="The permission level to grant. Skips interactive mode.",
)
@click.pass_context
async def set_perm(ctx, server_name: str, player_name: str, level: str):
    """Sets a permission level for a player on a specific server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        if not player_name or not level:
            click.secho(
                f"Player or level not specified; starting interactive editor for '{server_name}'...",
                fg="yellow",
            )
            await interactive_permissions_workflow(client, server_name)
            return

        click.echo(f"Finding player '{player_name}' in global database...")
        all_players_resp = await client.async_get_players()
        player_data = next(
            (
                p
                for p in all_players_resp.get("players", [])
                if p.get("name", "").lower() == player_name.lower()
            ),
            None,
        )

        if not player_data or not player_data.get("xuid"):
            click.secho(
                f"Error: Player '{player_name}' not found in the global player database.",
                fg="red",
            )
            return

        xuid = player_data["xuid"]
        click.echo(
            f"Setting permission for {player_name} (XUID: {xuid}) to '{level}'..."
        )

        payload = PermissionsSetPayload(
            permissions=[{"xuid": xuid, "permission_level": level}]
        )
        response = await client.async_set_server_permissions(server_name, payload)

        if response.status == "success":
            click.secho("Permission updated successfully.", fg="green")
        else:
            click.secho(f"Failed to set permission: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


@permissions.command("list")
@click.option(
    "-s", "--server", "server_name", required=True, help="The name of the server."
)
@click.pass_context
async def list_perms(ctx, server_name: str):
    """Lists all configured player permissions for a specific server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    response = await client.async_get_server_permissions_data(server_name)

    if response.status == "success":
        permissions = response.data.get("permissions", [])
        if not permissions:
            click.secho(
                f"The permissions file for server '{server_name}' is empty.",
                fg="yellow",
            )
            return

        click.secho(f"\nPermissions for '{server_name}':", bold=True)
        for p in permissions:
            level = p.get("permission", "unknown").lower()
            level_color = {"operator": "red", "member": "green", "visitor": "blue"}.get(
                level, "white"
            )
            level_styled = click.style(level.capitalize(), fg=level_color, bold=True)

            name = p.get("name", "Unknown Player")
            xuid = p.get("xuid", "N/A")
            click.echo(f"  - {name:<20} (XUID: {xuid:<18}) {level_styled}")
    else:
        click.secho(f"Failed to list permissions: {response.message}", fg="red")


async def interactive_permissions_workflow(client, server_name: str):
    """Guides the user through an interactive workflow to set a player's permission level."""
    click.secho("\n--- Interactive Permission Configuration ---", bold=True)
    player_response = await client.async_get_players()
    all_players = player_response.get("players", [])

    if not all_players:
        click.secho(
            "No players found in the global player database (players.json).",
            fg="yellow",
        )
        return

    player_map = {f"{p['name']} (XUID: {p['xuid']})": p for p in all_players}
    choices = sorted(list(player_map.keys())) + ["Cancel"]

    player_choice_str = await questionary.select(
        "Select a player to configure permissions for:", choices=choices
    ).ask_async()

    if not player_choice_str or player_choice_str == "Cancel":
        raise click.Abort()

    selected_player = player_map[player_choice_str]
    permission = await questionary.select(
        f"Select permission level for {selected_player['name']}:",
        choices=["member", "operator", "visitor"],
        default="member",
    ).ask_async()

    if permission is None:
        raise click.Abort()

    payload = PermissionsSetPayload(
        permissions=[{"xuid": selected_player["xuid"], "permission_level": permission}]
    )
    perm_response = await client.async_set_server_permissions(server_name, payload)

    if perm_response.status == "success":
        click.secho(
            f"Permission for {selected_player['name']} set to '{permission}'.",
            fg="green",
        )
    else:
        click.secho(f"Failed to set permission: {perm_response.message}", fg="red")
