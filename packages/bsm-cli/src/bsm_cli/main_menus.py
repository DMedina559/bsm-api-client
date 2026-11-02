"""Task-oriented terminal navigation with direct server and manager actions."""

import inspect

import click
import questionary
from questionary import Choice, Separator

from bsm_api_client.exceptions import CannotConnectError
from bsm_cli.interaction import menu_action, pause_or_exit
from bsm_cli.menu_registry import command_menu, plugin_api_menu
from bsm_cli.output import CliConnectionError, get_client
from bsm_cli.plugins import interactive_plugin_workflow
from bsm_cli.presentation import load_header, screen_header
from bsm_cli.server import _print_server_table, list_servers


async def _invoke(ctx, command, **kwargs):
    result = ctx.invoke(command, **kwargs)
    return await menu_action(result) if inspect.isawaitable(result) else result


def _command(ctx, group, name):
    root = ctx.obj["cli"]
    return root.commands[group].commands[name] if group else root.commands[name]


async def operations_menu(ctx):  # noqa: C901
    """Choose a retained operation directly to inspect its outcome."""
    from bsm_cli.manager import show_task

    while True:
        try:
            screen_header("Operations")
            tasks = await get_client(ctx).tasks.async_list_tasks()
            choices = [
                Choice(
                    f"{task.status.capitalize()} · {task.message} ({task.id})",
                    value=task.id,
                )
                for task in tasks
            ]
            if not tasks:
                click.echo("No operations recorded.")
            choices.extend(
                [Choice("Refresh", value="refresh"), Choice("Back", value="back")]
            )
            task_id = await questionary.select(
                "Operations", choices=choices
            ).ask_async()
        except (click.Abort, KeyboardInterrupt):
            return
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
            if not pause_or_exit("Press any key to return..."):
                return
            return
        if task_id in (None, "back"):
            return
        if task_id != "refresh":
            try:
                await _invoke(ctx, show_task, task_id=task_id)
            except (click.Abort, KeyboardInterrupt):
                click.echo("Action cancelled.")
            except Exception as error:
                click.secho(f"Action failed: {error}", fg="red")
            if not pause_or_exit("Press any key to return to operations..."):
                return


async def logs_menu(ctx):
    actions = {
        "Application logs": (None, "logs"),
        "Audit log": (None, "audit"),
    }
    await _action_menu(ctx, "Logs", actions)


async def _action_menu(ctx, title, actions, **kwargs):
    while True:
        try:
            screen_header(title)
            choice = await questionary.select(
                title, choices=[*actions, "Back"]
            ).ask_async()
        except (click.Abort, KeyboardInterrupt):
            return
        if choice is None or choice == "Back":
            return
        group, name = actions[choice]
        try:
            await _invoke(ctx, _command(ctx, group, name), **kwargs)
        except (click.Abort, KeyboardInterrupt):
            click.echo("Action cancelled.")
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
        if not pause_or_exit("Press any key to return..."):
            return


async def main_menu(ctx):  # noqa: C901
    client = ctx.obj.get("client")
    if not client:
        click.echo(
            "Sign in with bsm-cli auth login, or configure a new installation with bsm-cli auth setup."
        )
        return
    routes = {
        "Overview": (None, "overview"),
        "Monitor": (None, "monitor"),
        "App settings": (None, "settings"),
        "Health checks": (None, "health"),
    }
    groups = {
        "Players": "player",
        "Content": "content",
        "Appearance": "appearance",
        "Advanced API": "api",
        "Diagnostics": "diagnostics",
    }
    while True:
        try:
            await load_header(ctx, client)
            screen_header()
            fleet = await _load_home_fleet(ctx, client)
            if fleet is None:
                return
            click.echo()
            _print_server_table(fleet.servers or [])
            click.echo()
            choices = [
                Separator("── Monitoring ──"),
                "Overview",
                "Monitor",
                "Operations",
                "Logs",
                Separator("── Servers ──"),
            ]
            choices.extend(
                Choice(server.name, value=("server", server.name))
                for server in fleet.servers or []
            )
            choices.extend(
                [
                    "Install server",
                    Separator("── Application ──"),
                    "Plugins",
                    "App settings",
                    "Appearance",
                    "Health checks",
                    Separator("── Content ──"),
                    "Players",
                    "Content",
                    Separator("── Developer ──"),
                    "Advanced API",
                    "Plugin API",
                    Separator(),
                    "Exit",
                ]
            )
            choice = await questionary.select(
                "Choose a destination", choices=choices, use_shortcuts=False
            ).ask_async()
        except (click.Abort, KeyboardInterrupt):
            return
        if choice is None or choice == "Exit":
            return
        try:
            await _open_destination(ctx, choice, routes, groups)
        except (click.Abort, KeyboardInterrupt):
            click.echo("Returned home.")
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
            if not pause_or_exit("Press any key to return home..."):
                return


async def _load_home_fleet(ctx, client):  # noqa: C901
    while True:
        try:
            return await client.servers.async_get_servers()
        except (click.Abort, KeyboardInterrupt):
            return None
        except (CannotConnectError, CliConnectionError):
            config = ctx.obj.get("config")
            endpoint = config.base_url if config else "the configured backend"
            click.secho(f"Connection: Unavailable — {endpoint}", fg="yellow")
            click.echo(
                "Check that the backend is running and reachable at this address."
            )
            try:
                choice = await questionary.select(
                    "Connection unavailable", choices=["Retry", "Exit"]
                ).ask_async()
            except (click.Abort, KeyboardInterrupt):
                return None
            if choice != "Retry":
                return None
        except Exception as error:
            click.secho(f"Unable to load servers: {error}", fg="red")
            try:
                choice = await questionary.select(
                    "Home screen unavailable", choices=["Retry", "Exit"]
                ).ask_async()
            except (click.Abort, KeyboardInterrupt):
                return None
            if choice != "Retry":
                return None


async def _open_destination(ctx, choice, routes, groups):  # noqa: C901
    if isinstance(choice, tuple):
        await manage_server_menu(ctx, choice[1])
    elif choice in routes:
        await _invoke(ctx, _command(ctx, *routes[choice]))
        if not pause_or_exit("Press any key to return home..."):
            return
    elif choice == "Advanced API":
        from bsm_cli.api_explorer import explore

        await explore(ctx)
    elif choice in groups:
        await command_menu(ctx, ctx.obj["cli"].commands[groups[choice]])
    elif choice == "Plugins":
        await interactive_plugin_workflow(get_client(ctx))
    elif choice == "Operations":
        await operations_menu(ctx)
    elif choice == "Logs":
        await logs_menu(ctx)
    elif choice == "Plugin API":
        await plugin_api_menu(ctx)
    elif choice == "Install server":
        await _invoke(ctx, _command(ctx, "server", "install"))
        if not pause_or_exit("Press any key to return home..."):
            return


async def manage_server_menu(ctx, server_name):  # noqa: C901
    """Keep monitoring, lifecycle, and content actions on one server screen."""
    actions = {
        "Monitor": ("server", "monitor"),
        "Start": ("server", "start"),
        "Stop": ("server", "stop"),
        "Restart": ("server", "restart"),
        "Send command": ("server", "send-command"),
        "Settings": ("server", "settings"),
        "Properties": ("properties", "set"),
        "View raw properties": ("properties", "raw"),
        "Create backup": ("backup", "create"),
        "Restore backup": ("backup", "restore"),
        "Prune backups": ("backup", "prune"),
        "Install world": ("world", "install"),
        "Export world": ("world", "export"),
        "Reset world": ("world", "reset"),
        "Install addon": ("addon", "install"),
        "Manage addons": ("addon", "manage"),
        "Update": ("server", "update"),
        "Delete": ("server", "delete"),
    }
    access = {"Allowlist": "allowlist", "Permissions": "permissions", "Bans": "bans"}
    choices = [
        Separator("── Monitoring ──"),
        "Monitor",
        Separator("── Lifecycle ──"),
        "Start",
        "Stop",
        "Restart",
        "Send command",
        Separator("── Configuration ──"),
        "Settings",
        "Properties",
        "View raw properties",
        Separator("── Access control ──"),
        *access,
        Separator("── Backups ──"),
        "Create backup",
        "Restore backup",
        "Prune backups",
        Separator("── World and addons ──"),
        "Install world",
        "Export world",
        "Reset world",
        "Install addon",
        "Manage addons",
        Separator("── Maintenance ──"),
        "Update",
        "Delete",
        "Back",
    ]
    while True:
        try:
            screen_header(f"Manage server · {server_name}")
            await _invoke(ctx, list_servers, server_name=server_name)
            choice = await questionary.select(server_name, choices=choices).ask_async()
        except (click.Abort, KeyboardInterrupt):
            return
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
            if not pause_or_exit("Press any key to return..."):
                return
            return
        if choice is None or choice == "Back":
            return
        try:
            if choice in access:
                await command_menu(
                    ctx,
                    ctx.obj["cli"].commands[access[choice]],
                    values={"server_name": server_name},
                )
                continue
            kwargs = {"server_name": server_name}
            if choice == "Send command":
                value = await questionary.text("Server command").ask_async()
                if not value:
                    continue
                kwargs["command_parts"] = (value,)
            await _invoke(ctx, _command(ctx, *actions[choice]), **kwargs)
            if not pause_or_exit("Press any key to return to the server..."):
                return
            if await _deleted_server(ctx, choice, server_name):
                return
        except (click.Abort, KeyboardInterrupt):
            click.echo("Returned to server.")
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
            if not pause_or_exit("Press any key to return to the server..."):
                return


async def _deleted_server(ctx, choice, server_name):
    if choice != "Delete":
        return False
    # A cancelled delete leaves the server registered.
    fleet = await get_client(ctx).servers.async_get_servers()
    return not any(item.name == server_name for item in fleet.servers or [])
