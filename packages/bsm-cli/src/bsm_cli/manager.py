"""Manager overview, health, metrics, and background operations."""

import click

from bsm_cli.output import get_client


def memory(mb, unit="auto"):
    if mb is None:
        return "Unavailable"
    if unit == "auto":
        unit = "TB" if mb >= 1024**2 else "GB" if mb >= 1024 else "MB"
    divisor = {"MB": 1, "GB": 1024, "TB": 1024**2}[unit]
    return f"{mb / divisor:.2f} {unit}"


def outcome(value, prefix=""):
    """Render nested task outcomes without exposing an unstyled JSON blob."""
    if isinstance(value, dict):
        for key, item in value.items():
            outcome(item, f"{prefix} / {key}" if prefix else key)
    elif isinstance(value, list):
        for index, item in enumerate(value, 1):
            outcome(item, f"{prefix} {index}")
    elif value is not None:
        click.echo(f"{prefix.replace('_', ' ').capitalize()}: {value}")


@click.group()
def manager():
    """Overview, health checks, monitoring, and background tasks."""


async def overview(client, unit):
    health = await client.async_get_application_health()
    metrics = (await client.async_get_application_metrics()).latest
    fleet = await client.async_get_servers()
    click.secho("Bedrock Server Manager", bold=True)
    click.echo(
        f"Connection: Connected | Health: {health.health} | Lifecycle: {health.lifecycle}"
    )
    click.echo(
        f"App: CPU {metrics.app_cpu_percent}% | Memory {memory(metrics.app_ram_mb, unit)} | Background operations {metrics.background_task_count}"
    )
    click.echo(
        f"System: CPU {metrics.sys_cpu_percent}% | Memory {memory(metrics.sys_ram_mb, unit)} / {memory(metrics.sys_ram_total_mb, unit)}"
    )
    for server in fleet.servers or []:
        click.echo(
            f"{server.name}: {server.status} | Bedrock {server.version} | Players {server.player_count}"
        )


@manager.command("overview")
@click.option("--unit", type=click.Choice(["auto", "MB", "GB", "TB"]), default=None)
@click.pass_context
async def show_overview(ctx, unit):
    """Show fleet status and separate application and system statistics."""
    from bsm_cli.appearance import preferred_unit

    await overview(get_client(ctx), preferred_unit(ctx, unit))


@manager.command("health")
@click.pass_context
async def health(ctx):
    """Show component health checks and their current details."""
    response = await get_client(ctx).async_get_application_health()
    click.echo(f"{response.health} ({response.lifecycle})")
    for name, check in response.checks.items():
        outcome(check.model_dump(exclude_none=True), name)


@manager.command("monitor")
@click.option(
    "--interval", type=click.FloatRange(min=0.1), default=3.0, show_default=True
)
@click.option("--unit", type=click.Choice(["auto", "MB", "GB", "TB"]), default=None)
@click.option("--once", is_flag=True, help="Print a single metrics snapshot.")
@click.pass_context
async def monitor(ctx, interval, unit, once):
    """Monitor application and system metrics, including sample history."""
    if ctx.obj.get("json_output") and not once:
        raise click.UsageError("Use --once with --json.")
    from bsm_cli.appearance import preferred_unit

    unit = preferred_unit(ctx, unit)
    from bsm_api_client.models import MetricsSample
    from bsm_cli.live import watch_resource

    client = get_client(ctx)

    def update(current, data):
        sample = MetricsSample.model_validate(data)
        limit = current.history_limit
        history = [*current.history, sample]
        history = history[-limit:]
        return current.model_copy(
            update={
                "latest": sample,
                "history": history,
                "epoch": sample.epoch,
                "revision": sample.revision,
            }
        )

    if once:
        response = await client.async_get_application_metrics()
        render_metrics(response, unit)
        return
    async for response, live in watch_resource(
        client,
        client.async_get_application_metrics,
        ("application-metrics",),
        interval=interval,
        transform=update,
    ):
        click.clear()
        click.echo(
            f"WebSocket: {'Live' if live else 'Offline'} | Connection: Connected"
        )
        render_metrics(response, unit)


def render_metrics(response, unit):  # noqa: C901
    from bsm_cli.appearance import comfortable

    values = response.latest.model_dump(exclude_none=True)
    groups = {"Application": {}, "System": {}}
    for key, value in values.items():
        if key in ("servers", "epoch", "revision", "timestamp"):
            continue
        group = "System" if key.startswith(("sys_", "disk_", "net_")) else "Application"
        label = key.removeprefix("app_").removeprefix("sys_").replace("_", " ")
        if key.endswith("_mb"):
            value = memory(value, unit)
            label = label.removesuffix(" mb")
        elif key.endswith("_percent"):
            value = f"{value:.1f}%"
            label = label.removesuffix(" percent")
        elif key.endswith("_kib_s"):
            value = f"{value:.2f} KiB/s"
            label = label.removesuffix(" kib s")
        elif key.endswith("_seconds"):
            value = f"{value:.0f}s"
            label = label.removesuffix(" seconds")
        groups[group][label] = value
    for name, rows in groups.items():
        click.secho(name, bold=True)
        for label, value in rows.items():
            click.echo(f"  {label.capitalize()}: {value}")
        if comfortable():
            click.echo()
    for server in response.latest.servers or []:
        click.echo(
            f"{server.name}: CPU {server.cpu_percent}% | Memory {memory(server.memory_mb, unit)}"
        )
    for label, key in (
        ("App CPU", "app_cpu_percent"),
        ("System CPU", "sys_cpu_percent"),
    ):
        samples = [getattr(sample, key) for sample in response.history]
        samples = [sample for sample in samples if sample is not None]
        if samples:
            bars = "▁▂▃▄▅▆▇█"
            click.echo(
                f"{label}: "
                + "".join(
                    bars[min(7, max(0, int(value / 100 * 7)))]
                    for value in samples[-60:]
                )
            )


@manager.group("tasks")
def tasks():
    """List retained tasks and inspect their outcomes."""


@tasks.command("list")
@click.pass_context
async def list_tasks(ctx):
    for task in await get_client(ctx).async_list_tasks():
        click.echo(f"{task.id} | {task.status} | {task.message}")


@tasks.command("show")
@click.argument("task_id")
@click.pass_context
async def show_task(ctx, task_id):
    task = await get_client(ctx).async_get_task_snapshot(task_id)
    click.echo(f"{task.id}: {task.status} — {task.message}")
    outcome(task.result)
    if task.error:
        outcome(task.error.model_dump(exclude_none=True), "Error")


@manager.command("settings")
@click.pass_context
async def settings(ctx):
    """Review and edit typed global application settings."""
    from bsm_api_client.models import SettingItemResponse
    from bsm_cli.settings_editor import edit_settings, fields, infer_schema

    if ctx.obj.get("json_output"):
        return await get_client(ctx).async_get_all_settings()
    client = get_client(ctx)
    original = (await client.async_get_all_settings()).settings or {}
    draft = await edit_settings(original, title="Application settings")
    if draft is None:
        return
    if (await client.async_get_all_settings()).settings != original:
        raise click.ClickException(
            "Settings changed in another session. Reopen the editor."
        )
    schema = infer_schema(draft)
    for path, spec, value in fields(schema, schema, draft):
        previous = original
        for key in path:
            previous = previous.get(key) if isinstance(previous, dict) else None
        if previous != value:
            await client.async_set_setting(
                SettingItemResponse(key=".".join(path), value=value)
            )
            click.echo(f"Saved {'.'.join(path)}")


@manager.command("audit")
@click.pass_context
async def audit(ctx):
    """Show audit records with time, actor, action, and structured details."""
    records = await get_client(ctx).async_call_generated(
        "list_audit_logs", authenticated=True
    )
    for record in records:
        click.echo(
            f"{record['timestamp']} | User {record['user_id']} | {record['action']}"
        )
        if record.get("details"):
            outcome(record["details"])


@manager.command("logs")
@click.option(
    "--topic",
    default="app_logs",
    show_default=True,
    help="Log topic, such as server_log:example.",
)
@click.option(
    "--before",
    type=click.IntRange(min=0),
    help="Byte cursor from the previous page's start.",
)
@click.option(
    "--file-id", help="Log file identity from the previous page, to detect rotation."
)
@click.pass_context
async def logs(ctx, topic, before, file_id):
    """Read a log-history page; use the cursor to request older content."""
    parameters = {"topic": topic}
    if before is not None:
        parameters["before"] = before
    if file_id is not None:
        parameters["file_id"] = file_id
    page = await get_client(ctx).async_call_generated(
        "get_log_history", parameters=parameters, authenticated=True
    )
    click.echo(page["data"], nl=False)
    if page["has_more"]:
        click.echo(
            f"\nOlder logs: --before {page['start']} --file-id {page['file_id']}"
        )
