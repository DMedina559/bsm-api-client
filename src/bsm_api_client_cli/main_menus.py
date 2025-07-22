import click
import questionary
from questionary import Separator
from .decorators import pass_async_context
from .server import list_servers


async def _world_management_menu(ctx: click.Context, server_name: str):
    """Displays a sub-menu for world management actions."""
    world_group = ctx.obj["cli"].get_command(ctx, "world")
    if not world_group:
        click.secho("Error: World command group not found.", fg="red")
        return

    menu_map = {
        "Install/Replace World": world_group.get_command(ctx, "install"),
        "Export Current World": world_group.get_command(ctx, "export"),
        "Reset Current World": world_group.get_command(ctx, "reset"),
        "Back": None,
    }

    while True:
        choice = await questionary.select(
            f"World Management for '{server_name}':",
            choices=list(menu_map.keys()),
            use_indicator=True,
        ).ask_async()

        if choice is None or choice == "Back":
            return
        command = menu_map.get(choice)
        if command:
            await ctx.invoke(command, server_name=server_name)
            break


async def _backup_restore_menu(ctx: click.Context, server_name: str):
    """Displays a sub-menu for backup and restore actions."""
    backup_group = ctx.obj["cli"].get_command(ctx, "backup")
    if not backup_group:
        click.secho("Error: Backup command group not found.", fg="red")
        return

    menu_map = {
        "Create Backup": backup_group.get_command(ctx, "create"),
        "Restore from Backup": backup_group.get_command(ctx, "restore"),
        "Prune Old Backups": backup_group.get_command(ctx, "prune"),
        "Back": None,
    }

    while True:
        choice = await questionary.select(
            f"Backup/Restore for '{server_name}':",
            choices=list(menu_map.keys()),
            use_indicator=True,
        ).ask_async()

        if choice is None or choice == "Back":
            return
        command = menu_map.get(choice)
        if command:
            await ctx.invoke(command, server_name=server_name)
            break


async def main_menu(ctx: click.Context):
    """Displays the main application menu and drives interactive mode."""
    client = ctx.obj.get("client")
    if not client:
        click.secho(
            "You are not logged in. Please run `bsm-cli auth login` first.", fg="red"
        )
        return

    cli = ctx.obj["cli"]

    while True:
        try:
            click.clear()
            click.secho("BSM API Client - Main Menu", fg="magenta", bold=True)

            await ctx.invoke(list_servers)

            # --- Dynamically build menu choices ---
            response = await client.async_get_servers_details()
            server_names = (
                [s["name"] for s in response.servers] if response.servers else []
            )

            menu_choices = ["Install New Server"]
            if server_names:
                menu_choices.append("Manage Existing Server")

            menu_choices.append("Manage Plugins")
            menu_choices.append(Separator("--- Application ---"))
            menu_choices.append("Exit")

            choice = await questionary.select(
                "\nChoose an action:",
                choices=menu_choices,
                use_indicator=True,
            ).ask_async()

            if choice is None or choice == "Exit":
                return

            if choice == "Install New Server":
                server_group = cli.get_command(ctx, "server")
                install_cmd = server_group.get_command(ctx, "install")
                await ctx.invoke(install_cmd)
                await questionary.press_any_key_to_continue(
                    "Press any key to return to the main menu..."
                ).ask_async()

            elif choice == "Manage Existing Server":
                server_name = await questionary.select(
                    "Select a server:", choices=server_names
                ).ask_async()
                if server_name:
                    await manage_server_menu(ctx, server_name)

            elif choice == "Manage Plugins":
                plugin_group = cli.get_command(ctx, "plugin")
                await ctx.invoke(plugin_group)
                await questionary.press_any_key_to_continue(
                    "Press any key to return to the main menu..."
                ).ask_async()

        except (click.Abort, KeyboardInterrupt):
            click.echo("\nAction cancelled. Returning to the main menu.")
            click.pause()
        except Exception as e:
            click.secho(f"\nAn unexpected error occurred: {e}", fg="red")
            click.pause("Press any key to return to the main menu...")


async def manage_server_menu(ctx: click.Context, server_name: str):
    """Displays the menu for managing a specific, existing server."""
    cli = ctx.obj["cli"]

    def get_cmd(group_name, cmd_name):
        """Helper to safely retrieve a command object from the CLI."""
        group = cli.get_command(ctx, group_name)
        return group.get_command(ctx, cmd_name) if group else None

    # ---- Define static menu sections ----
    control_map = {
        "Start Server": (get_cmd("server", "start"), {}),
        "Stop Server": (get_cmd("server", "stop"), {}),
        "Restart Server": (get_cmd("server", "restart"), {}),
        "Send Command to Server": (get_cmd("server", "send-command"), {}),
    }
    management_map = {
        "Backup or Restore": _backup_restore_menu,
        "Manage World": _world_management_menu,
        "Install Addon": (get_cmd("addon", "install"), {}),
    }
    config_map = {
        "Configure Properties": (get_cmd("properties", "set"), {}),
        "Configure Allowlist": (get_cmd("allowlist", "add"), {}),
        "Configure Permissions": (get_cmd("permissions", "set"), {}),
    }
    maintenance_map = {
        "Update Server": (get_cmd("server", "update"), {}),
        "Delete Server": (get_cmd("server", "delete"), {}),
    }
    system_map = {}
    system_map["Monitor Resource Usage"] = (get_cmd("system", "monitor"), {})

    # ---- Combine all maps for easy lookup ----
    full_menu_map = {
        **control_map,
        **management_map,
        **config_map,
        **system_map,
        **maintenance_map,
        "Back to Main Menu": "back",
    }

    # ---- Build the final choices list for questionary ----
    menu_choices = [
        Separator("--- Server Control ---"),
        *control_map.keys(),
        Separator("--- Management ---"),
        *management_map.keys(),
        Separator("--- Configuration ---"),
        *config_map.keys(),
    ]

    if system_map:
        menu_choices.extend(
            [Separator("--- System & Monitoring ---"), *system_map.keys()]
        )

    menu_choices.extend(
        [
            Separator("--- Maintenance ---"),
            *maintenance_map.keys(),
            Separator("--------------------"),
            "Back to Main Menu",
        ]
    )

    while True:
        click.clear()
        click.secho(f"--- Managing Server: {server_name} ---", fg="magenta", bold=True)
        await ctx.invoke(list_servers, server_name=server_name)

        choice = await questionary.select(
            f"\nSelect an action for '{server_name}':",
            choices=menu_choices,
            use_indicator=True,
        ).ask_async()

        if choice is None or choice == "Back to Main Menu":
            return

        action = full_menu_map.get(choice)
        if not action:
            continue

        try:
            if callable(action) and not hasattr(action, "commands"):
                await action(ctx, server_name)
            elif isinstance(action, tuple):
                command_obj, kwargs = action
                if not command_obj:
                    continue
                if command_obj.name == "send-command":
                    cmd_str = await questionary.text(
                        "Enter command to send:"
                    ).ask_async()
                    if cmd_str:
                        kwargs["command_parts"] = cmd_str.split()
                    else:
                        continue
                kwargs["server_name"] = server_name
                await ctx.invoke(command_obj, **kwargs)
                if command_obj.name == "delete":
                    click.echo("\nServer has been deleted. Returning to main menu.")
                    click.pause()
                    return
            elif hasattr(action, "commands"):
                ctx.invoke(action, server_name=server_name)

            click.pause("\nPress any key to return to the server menu...")

        except Exception as e:
            click.secho(f"An error occurred while executing '{choice}': {e}", fg="red")
            click.pause()
