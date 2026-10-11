import asyncio
import time

import click

from bsm_api_client.models import ServerSettingItemPayload
from bsm_cli.completion import complete_server
from bsm_cli.output import get_client


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
    shell_complete=complete_server,
)
@click.pass_context
async def server_settings(ctx, server_name: str):
    """Review and edit all available Bedrock server settings."""
    client = get_client(ctx)

    from bsm_cli.settings_editor import edit_settings, fields, infer_schema

    response = await client.async_get_server_settings(server_name)
    original = response.settings or {}
    draft = await edit_settings(original, title=f"Settings: {server_name}")
    if draft is None:
        return
    latest = await client.async_get_server_settings(server_name)
    if latest.settings != original:
        raise click.ClickException(
            "Settings changed in another session. Reopen the editor."
        )
    for path, spec, value in fields(infer_schema(draft), infer_schema(draft), draft):
        previous = original
        for key in path:
            previous = previous.get(key) if isinstance(previous, dict) else None
        if previous != value:
            await client.async_set_server_setting(
                server_name, ServerSettingItemPayload(key=".".join(path), value=value)
            )
            click.echo(f"Saved {'.'.join(path)}")


@system.command("monitor")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server to monitor.",
    shell_complete=complete_server,
)
@click.pass_context
async def monitor_usage(ctx, server_name: str):
    """Continuously monitors CPU and memory usage of a specific server process."""
    client = get_client(ctx)

    if ctx.obj.get("json_output"):
        return await client.async_get_server_process_info(server_name)

    click.secho(
        f"Starting resource monitoring for server '{server_name}'. Press CTRL+C to exit.",
        fg="cyan",
    )
    await asyncio.sleep(1)

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
                from bsm_cli.appearance import preferred_unit
                from bsm_cli.manager import memory

                mem_str = memory(info.memory_mb, preferred_unit(ctx, None))
                uptime_str = info.get("uptime", "N/A")

                click.echo(f"  {'PID':<15}: {click.style(str(pid_str), fg='cyan')}")
                click.echo(f"  {'CPU Usage':<15}: {click.style(cpu_str, fg='green')}")
                click.echo(
                    f"  {'Memory Usage':<15}: {click.style(mem_str, fg='green')}"
                )
                click.echo(f"  {'Uptime':<15}: {click.style(uptime_str, fg='white')}")

            await asyncio.sleep(2)
    except (KeyboardInterrupt, click.Abort):
        click.secho("\nMonitoring stopped.", fg="green")
