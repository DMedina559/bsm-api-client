import asyncio
import functools
import time
import click


class AsyncGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.async_context_settings = {}

    def context(self, f):
        self.async_context_settings["context"] = f
        return f

    def invoke(self, ctx):
        ctx.obj = ctx.obj or {}
        if self.async_context_settings.get("context"):

            async def runner():
                async with self.async_context_settings["context"](ctx):
                    result = super(AsyncGroup, self).invoke(ctx)
                    if asyncio.iscoroutine(result):
                        await result

            return asyncio.run(runner())

        result = super().invoke(ctx)
        if asyncio.iscoroutine(result):
            return asyncio.run(result)
        return result


def pass_async_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        return f(ctx, *args, **kwargs)

    return wrapper


async def monitor_task(
    client, task_id: str, success_message: str, failure_message: str
):
    """Polls the status of a background task until it completes."""
    click.echo("Task started in the background. Monitoring for completion...")

    # Try WebSocket first
    try:
        ws_client = await client.websocket_connect()
        async with ws_client:
            # No subscription needed for task updates as per documentation
            async for msg in ws_client.listen():
                # Expected format: {"type": "task_update", "topic": "task:{task_id}", "data": {...}}
                if (
                    msg.get("topic") == f"task:{task_id}"
                    and msg.get("type") == "task_update"
                ):
                    data = msg.get("data", {})
                    status = data.get("status")
                    message = data.get("message", "No message provided.")

                    if status == "success":
                        click.secho(f"{success_message}: {message}", fg="green")
                        return
                    elif status == "error":
                        click.secho(f"{failure_message}: {message}", fg="red")
                        return
                    elif status == "in_progress":
                        # Maybe print progress if available, or just wait
                        pass
    except Exception as e:
        click.secho(
            f"WebSocket monitoring failed ({e}), falling back to polling...",
            fg="yellow",
        )

    # Fallback to polling
    while True:
        try:
            status_response = await client.async_get_task_status(task_id)
            status = status_response.get("status")
            message = status_response.get("message", "No message provided.")

            if status == "success":
                click.secho(f"{success_message}: {message}", fg="green")
                break
            elif status == "error":
                click.secho(
                    f"{failure_message}: {message}",
                    fg="red",
                )
                break
            elif status == "pending" or status == "in_progress":
                # Still waiting, continue loop
                pass
            else:
                # Handle unexpected status
                click.secho(f"Unknown task status received: {status}", fg="yellow")

            await asyncio.sleep(2)
        except Exception as e:
            click.secho(f"An error occurred while monitoring task: {e}", fg="red")
            break
