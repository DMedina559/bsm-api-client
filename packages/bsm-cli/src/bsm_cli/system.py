import time

import click
import questionary

from bsm_api_client.models import ServerSettingItemPayload


@click.group()
def system():
    """Manages server OS-level resource monitoring and settings."""
    pass


@system.command("settings")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server to configure.",
)
@click.pass_context
async def server_settings(ctx, server_name: str):
    """Configures autostart and autoupdate settings for a Bedrock server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.secho(
        f"Starting interactive settings configuration for '{server_name}'...",
        fg="yellow",
    )

    settings_response = await client.async_get_server_settings(server_name)
    if settings_response.status != "success" or not settings_response.settings:
        click.secho(
            f"Failed to fetch server settings: {settings_response.message}", fg="red"
        )
        return

    settings = settings_response.settings

    current_autoupdate = settings.get("settings", {}).get("autoupdate", False)
    current_autostart = settings.get("settings", {}).get("autostart", False)

    click.secho(
        f"\n--- Interactive Settings Configuration for '{server_name}' ---", bold=True
    )

    autoupdate_choice = await questionary.confirm(
        "Enable check for updates when the server starts?", default=current_autoupdate
    ).ask_async()

    if autoupdate_choice is not None and autoupdate_choice != current_autoupdate:
        payload = ServerSettingItemPayload(
            key="settings.autoupdate", value=autoupdate_choice
        )
        response = await client.async_set_server_setting(server_name, payload)
        if response.status == "success":
            click.secho(
                f"Autoupdate setting configured to '{autoupdate_choice}'.", fg="green"
            )
        else:
            click.secho(f"Failed to set autoupdate: {response.message}", fg="red")

    autostart_choice = await questionary.confirm(
        "Enable the server to start automatically when the manager starts?",
        default=current_autostart,
    ).ask_async()

    if autostart_choice is not None and autostart_choice != current_autostart:
        payload = ServerSettingItemPayload(
            key="settings.autostart", value=autostart_choice
        )
        response = await client.async_set_server_setting(server_name, payload)
        if response.status == "success":
            click.secho(
                f"Autostart setting configured to '{autostart_choice}'.", fg="green"
            )
        else:
            click.secho(f"Failed to set autostart: {response.message}", fg="red")

    click.secho("\nSettings configuration complete.", fg="green", bold=True)


@system.command("monitor")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server to monitor.",
)
@click.pass_context
async def monitor_usage(ctx, server_name: str):
    """Continuously monitors CPU and memory usage of a specific server process."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.secho(
        f"Starting resource monitoring for server '{server_name}'. Press CTRL+C to exit.",
        fg="cyan",
    )
    time.sleep(1)

    try:
        while True:
            response = await client.async_get_server_process_info(server_name)

            click.clear()
            click.secho(
                f"--- Monitoring Server: {server_name} ---", fg="magenta", bold=True
            )
            click.echo(
                f"(Last updated: {time.strftime('%H:%M:%S')}, Press CTRL+C to exit)\n"
            )

            if response.status == "error":
                click.secho(f"Error: {response.message}", fg="red")
            elif response.process_info is None:
                click.secho("Server process not found (is it running?).", fg="yellow")
            else:
                info = response.process_info
                pid_str = info.get("pid", "N/A")
                cpu_str = f"{info.get('cpu_percent', 0.0):.1f}%"
                mem_str = f"{info.get('memory_mb', 0.0):.1f} MB"
                uptime_str = info.get("uptime", "N/A")

                click.echo(f"  {'PID':<15}: {click.style(str(pid_str), fg='cyan')}")
                click.echo(f"  {'CPU Usage':<15}: {click.style(cpu_str, fg='green')}")
                click.echo(
                    f"  {'Memory Usage':<15}: {click.style(mem_str, fg='green')}"
                )
                click.echo(f"  {'Uptime':<15}: {click.style(uptime_str, fg='white')}")

            time.sleep(2)
    except (KeyboardInterrupt, click.Abort):
        click.secho("\nMonitoring stopped.", fg="green")
