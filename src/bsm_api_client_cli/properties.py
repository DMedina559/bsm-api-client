import click
import questionary
from bsm_api_client.models import PropertiesPayload

@click.group()
def properties():
    """Manages a server's server.properties file."""
    pass

@properties.command("get")
@click.option("-s", "--server", "server_name", required=True, help="The name of the target server.")
@click.option("-p", "--prop", "property_name", help="Display a single property value.")
@click.pass_context
async def get_props(ctx, server_name: str, property_name: str):
    """Displays server properties from a server's server.properties file."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    response = await client.async_get_server_properties(server_name)

    if response.status == "success":
        properties = response.data["properties"]
        if property_name:
            value = properties.get(property_name)
            if value is not None:
                click.echo(value)
            else:
                click.secho(f"Error: Property '{property_name}' not found.", fg="red")
        else:
            click.secho(f"\nProperties for '{server_name}':", bold=True)
            max_key_len = max(len(k) for k in properties.keys()) if properties else 0
            for key, value in sorted(properties.items()):
                click.echo(f"  {key:<{max_key_len}} = {value}")
    else:
        click.secho(f"Failed to get properties: {response.message}", fg="red")


@properties.command("set")
@click.option("-s", "--server", "server_name", required=True, help="The name of the target server.")
@click.option(
    "-p",
    "--prop",
    "properties",
    multiple=True,
    help="A 'key=value' pair to set. Use multiple times for multiple properties.",
)
@click.pass_context
async def set_props(ctx, server_name: str, properties: tuple[str]):
    """Sets one or more properties in a server's server.properties file."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    try:
        if not properties:
            click.secho(
                f"No properties specified; starting interactive editor for '{server_name}'...",
                fg="yellow",
            )
            await interactive_properties_workflow(client, server_name)
            return

        props_to_update = {}
        for p in properties:
            if "=" not in p:
                click.secho(f"Error: Invalid format '{p}'. Use 'key=value'.", fg="red")
                raise click.Abort()
            key, value = p.split("=", 1)
            props_to_update[key.strip()] = value.strip()

        click.echo(f"Updating {len(props_to_update)} propert(y/ies) for '{server_name}'...")
        
        payload = PropertiesPayload(properties=props_to_update)
        response = await client.async_update_server_properties(server_name, payload)

        if response.status == "success":
            click.secho("Properties updated successfully.", fg="green")
        else:
            click.secho(f"Failed to set properties: {response.message}", fg="red")

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red")


async def interactive_properties_workflow(client, server_name: str):
    """Guides a user through an interactive session to edit `server.properties`."""
    click.secho("\n--- Interactive Server Properties Configuration ---", bold=True)
    click.echo("Loading current server properties...")

    properties_response = await client.async_get_server_properties(server_name)
    if properties_response.status == "error":
        click.secho(f"Error: {properties_response.message}", fg="red")
        raise click.Abort()

    current_properties = properties_response.data["properties"]
    changes = {}

    async def _prompt(prop: str, message: str, prompter, **kwargs):
        """A nested helper to abstract the prompting and change-tracking logic."""
        original_value = current_properties.get(prop)

        if prompter == questionary.confirm:
            default_bool = str(original_value).lower() == "true"
            new_val = await prompter(message, default=default_bool, **kwargs).ask_async()
            if new_val is None:
                return
            if new_val != default_bool:
                changes[prop] = str(new_val).lower()
        else:
            new_val = await prompter(message, default=str(original_value), **kwargs).ask_async()
            if new_val is None:
                return
            if new_val != original_value:
                changes[prop] = new_val

    await _prompt("server-name", "Server name (visible in LAN list):", questionary.text)
    await _prompt("level-name", "World folder name:", questionary.text)
    await _prompt("gamemode", "Default gamemode:", questionary.select, choices=["survival", "creative", "adventure"])
    await _prompt("difficulty", "Game difficulty:", questionary.select, choices=["peaceful", "easy", "normal", "hard"])
    await _prompt("allow-cheats", "Allow cheats:", questionary.confirm)
    await _prompt("max-players", "Maximum players:", questionary.text)
    await _prompt("online-mode", "Require Xbox Live authentication:", questionary.confirm)
    await _prompt("allow-list", "Enable allowlist:", questionary.confirm)
    await _prompt("default-player-permission-level", "Default permission for new players:", questionary.select, choices=["visitor", "member", "operator"])
    await _prompt("view-distance", "View distance (chunks):", questionary.text)
    await _prompt("tick-distance", "Tick simulation distance (chunks):", questionary.text)
    await _prompt("level-seed", "Level seed (leave blank for random):", questionary.text)
    await _prompt("texturepack-required", "Require texture packs:", questionary.confirm)

    if not changes:
        click.secho("\nNo properties were changed.", fg="cyan")
        return

    click.secho("\nApplying the following changes:", bold=True)
    for key, value in changes.items():
        original = current_properties.get(key, "not set")
        click.echo(f"  - {key}: {click.style(original, fg='red')} -> {click.style(value, fg='green')}")

    if not await questionary.confirm("Save these changes?", default=True).ask_async():
        raise click.Abort()

    payload = PropertiesPayload(properties=changes)
    update_response = await client.async_update_server_properties(server_name, payload)
    
    if update_response.status == "success":
        click.secho("Server properties updated successfully.", fg="green")
    else:
        click.secho(f"Failed to update properties: {update_response.message}", fg="red")
