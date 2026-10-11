"""Task-oriented terminal navigation with direct server and manager actions."""

import inspect

import click
import questionary
from questionary import Choice, Separator

from bsm_cli.menu_registry import command_menu, plugin_api_menu
from bsm_cli.output import get_client
from bsm_cli.plugins import interactive_plugin_workflow
from bsm_cli.server import list_servers


async def _invoke(ctx, command, **kwargs):
    result = ctx.invoke(command, **kwargs)
    return await result if inspect.isawaitable(result) else result


def _command(ctx, group, name):
    return ctx.obj["cli"].commands[group].commands[name]


async def operations_menu(ctx):
    """Choose a retained operation directly to inspect its outcome."""
    from bsm_cli.manager import show_task

    while True:
        tasks = await get_client(ctx).async_list_tasks()
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
        task_id = await questionary.select("Operations", choices=choices).ask_async()
        if task_id in (None, "back"):
            return
        if task_id != "refresh":
            await _invoke(ctx, show_task, task_id=task_id)
            click.pause("Press any key to return to operations...")


async def logs_menu(ctx):
    actions = {
        "Application logs": ("manager", "logs"),
        "Audit log": ("manager", "audit"),
    }
    await _action_menu(ctx, "Logs", actions)


async def _action_menu(ctx, title, actions, **kwargs):
    while True:
        choice = await questionary.select(title, choices=[*actions, "Back"]).ask_async()
        if choice is None or choice == "Back":
            return
        group, name = actions[choice]
        await _invoke(ctx, _command(ctx, group, name), **kwargs)
        click.pause("Press any key to return...")


async def main_menu(ctx):
    client = ctx.obj.get("client")
    if not client:
        click.echo(
            "Sign in with bsm-cli auth login, or configure a new installation with bsm-cli auth setup."
        )
        return
    routes = {
        "Overview": ("manager", "overview"),
        "Monitor": ("manager", "monitor"),
        "App settings": ("manager", "settings"),
        "Health checks": ("manager", "health"),
    }
    groups = {
        "Account": "account",
        "Users": "users",
        "Players": "player",
        "Content": "content",
        "Appearance": "appearance",
        "Advanced API": "api",
    }
    while True:
        try:
            click.clear()
            click.secho("Bedrock Server Manager", bold=True, fg="magenta")
            fleet = await client.async_get_servers()
            choices = [
                "Overview",
                "Monitor",
                "Operations",
                "Plugins",
                "Logs",
                Separator("Servers"),
            ]
            choices.extend(
                Choice(
                    f"{server.name} · {server.status}", value=("server", server.name)
                )
                for server in fleet.servers or []
            )
            choices.extend(
                [
                    "Install server",
                    Separator("Administration"),
                    "App settings",
                    "Appearance",
                    "Health checks",
                    "Account",
                    "Users",
                    "Players",
                    "Content",
                    Separator("Developer"),
                    "Advanced API",
                    "Plugin API",
                    "Exit",
                ]
            )
            choice = await questionary.select(
                "Choose a destination", choices=choices
            ).ask_async()
            if choice is None or choice == "Exit":
                return
            await _open_destination(ctx, choice, routes, groups)
        except (click.Abort, KeyboardInterrupt):
            click.echo("Returned home.")
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
            click.pause("Press any key to return home...")


async def _open_destination(ctx, choice, routes, groups):
    if isinstance(choice, tuple):
        await manage_server_menu(ctx, choice[1])
    elif choice in routes:
        await _invoke(ctx, _command(ctx, *routes[choice]))
        click.pause("Press any key to return home...")
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
        click.pause("Press any key to return home...")


async def manage_server_menu(ctx, server_name):
    """Keep monitoring, lifecycle, and content actions on one server screen."""
    actions = {
        "Monitor": ("system", "monitor"),
        "Start": ("server", "start"),
        "Stop": ("server", "stop"),
        "Restart": ("server", "restart"),
        "Send command": ("server", "send-command"),
        "Settings": ("system", "settings"),
        "Properties": ("properties", "set"),
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
        "Monitor",
        Separator("Lifecycle"),
        "Start",
        "Stop",
        "Restart",
        "Send command",
        Separator("Configuration"),
        "Settings",
        "Properties",
        *access,
        Separator("Backups"),
        "Create backup",
        "Restore backup",
        "Prune backups",
        Separator("World and addons"),
        "Install world",
        "Export world",
        "Reset world",
        "Install addon",
        "Manage addons",
        Separator("Maintenance"),
        "Update",
        "Delete",
        "Back",
    ]
    while True:
        click.clear()
        await _invoke(ctx, list_servers, server_name=server_name)
        choice = await questionary.select(server_name, choices=choices).ask_async()
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
            click.pause("Press any key to return to the server...")
            if await _deleted_server(ctx, choice, server_name):
                return
        except (click.Abort, KeyboardInterrupt):
            click.echo("Returned to server.")
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
            click.pause("Press any key to return to the server...")


async def _deleted_server(ctx, choice, server_name):
    if choice != "Delete":
        return False
    # A cancelled delete leaves the server registered.
    fleet = await get_client(ctx).async_get_servers()
    return not any(item.name == server_name for item in fleet.servers or [])
