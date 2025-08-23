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
    click.echo("Task started in the background. Polling for completion...")
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
            elif status == "pending":
                # Still waiting, continue loop
                pass
            else:
                # Handle unexpected status
                click.secho(f"Unknown task status received: {status}", fg="yellow")

            time.sleep(2)
        except Exception as e:
            click.secho(f"An error occurred while monitoring task: {e}", fg="red")
            break
