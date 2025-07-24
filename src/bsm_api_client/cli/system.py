import click
import time
import questionary


@click.group()
def system():
    """Manages OS-level integrations and server resource monitoring."""
    pass


@system.command("configure-service")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server to configure.",
)
@click.pass_context
async def configure_service(ctx, server_name: str):
    """Configures OS-specific service settings for a Bedrock server."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.secho(
        f"Starting interactive service configuration for '{server_name}'...",
        fg="yellow",
    )
    await interactive_service_workflow(client, server_name)


@system.command("enable-service")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server service to enable.",
)
@click.pass_context
async def enable_service(ctx, server_name: str):
    """Enables a server's system service for automatic startup."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.echo(f"Attempting to enable system service for '{server_name}'...")
    response = await client.async_enable_server_service(server_name)
    if response.status == "success":
        click.secho("Service enabled successfully.", fg="green")
    else:
        click.secho(f"Failed to enable service: {response.message}", fg="red")


@system.command("disable-service")
@click.option(
    "-s",
    "--server",
    "server_name",
    required=True,
    help="Name of the server service to disable.",
)
@click.pass_context
async def disable_service(ctx, server_name: str):
    """Disables a server's system service from starting automatically."""
    client = ctx.obj.get("client")
    if not client:
        click.secho("You are not logged in.", fg="red")
        return

    click.echo(f"Attempting to disable system service for '{server_name}'...")
    response = await client.async_disable_server_service(server_name)
    if response.status == "success":
        click.secho("Service disabled successfully.", fg="green")
    else:
        click.secho(f"Failed to disable service: {response.message}", fg="red")


async def interactive_service_workflow(client, server_name: str):
    """Guides the user through an interactive workflow to configure server services."""
    click.secho(
        f"\n--- Interactive Service Configuration for '{server_name}' ---", bold=True
    )

    autoupdate_choice = await questionary.confirm(
        "Enable check for updates when the server starts?", default=False
    ).ask_async()

    if autoupdate_choice is not None:
        response = await client.async_set_server_autoupdate(
            server_name, autoupdate_choice
        )
        if response.status == "success":
            click.secho(
                f"Autoupdate setting configured to '{autoupdate_choice}'.", fg="green"
            )
        else:
            click.secho(f"Failed to set autoupdate: {response.message}", fg="red")

    setup_service_choice = await questionary.confirm(
        "Create or update the system service for this server?",
        default=True,
    ).ask_async()

    if setup_service_choice:
        enable_autostart_choice = await questionary.confirm(
            "Enable the service to start automatically when you log in?",
            default=False,
        ).ask_async()

        response = await client.async_create_server_service(
            server_name, enable_autostart_choice
        )
        if response.status == "success":
            click.secho("System service configured successfully.", fg="green")
        else:
            click.secho(
                f"Failed to configure system service: {response.message}", fg="red"
            )

    click.secho("\nService configuration complete.", fg="green", bold=True)


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
            elif response.data.get("process_info") is None:
                click.secho("Server process not found (is it running?).", fg="yellow")
            else:
                info = response.data["process_info"]
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
