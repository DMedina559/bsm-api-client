import asyncio
import functools

import click
from bsm_api_client.exceptions import AuthError, OperationFailedError


class AsyncGroup(click.Group):
    def parse_args(self, ctx, args):
        root_args = args[
            : next((i for i, arg in enumerate(args) if arg in self.commands), len(args))
        ]
        json_output = "--json" in root_args
        try:
            return super().parse_args(ctx, args)
        except click.ClickException as error:
            if not json_output:
                raise
            from bsm_cli.output import echo_json

            echo_json(
                {"error": error.format_message(), "exit_code": error.exit_code},
                err=True,
            )
            raise click.exceptions.Exit(error.exit_code) from error

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.async_context_settings = {}

    def context(self, f):
        self.async_context_settings["context"] = f
        return f

    def invoke(self, ctx):
        ctx.obj = ctx.obj or {}
        if self.async_context_settings.get("context"):
            return asyncio.run(self._invoke_context(ctx))
        result = super().invoke(ctx)
        return asyncio.run(result) if asyncio.iscoroutine(result) else result

    async def _invoke_context(self, ctx):
        import contextlib
        import io

        from bsm_cli.output import RecordingClient, echo_json, fail, normalize_error

        json_output = ctx.params.get("json_output", False)
        transcript = io.StringIO()
        output_context = (
            contextlib.redirect_stdout(transcript)
            if json_output
            else contextlib.nullcontext()
        )
        try:
            with output_context:
                async with self.async_context_settings["context"](ctx):
                    recorder = None
                    if ctx.obj.get("client"):
                        recorder = RecordingClient(
                            ctx.obj["client"], record=json_output
                        )
                        ctx.obj["client"] = recorder
                    result = super().invoke(ctx)
                    if asyncio.iscoroutine(result):
                        result = await result
            if json_output:
                echo_json(_structured_result(result, recorder))
            return result
        except click.exceptions.Exit as error:
            if json_output and error.exit_code == 0:
                click.echo(transcript.getvalue(), nl=False)
            raise
        except click.Abort:
            raise
        except Exception as error:
            if json_output:
                normalized = normalize_error(error)
                echo_json(
                    {"error": str(error), "exit_code": normalized.exit_code}, err=True
                )
                raise click.exceptions.Exit(normalized.exit_code) from error
            fail(error)


def _structured_result(result, recorder):
    if result is not None or recorder is None:
        return result
    return recorder.results[0] if len(recorder.results) == 1 else recorder.results


def pass_async_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        return f(ctx, *args, **kwargs)

    return wrapper


async def monitor_task(
    client, task_id: str, success_message: str, failure_message: str
):
    """Watch task updates with WebSockets, then use the shared REST fallback."""
    click.echo("Task started in the background. Monitoring for completion...")
    try:
        if await _watch_with_refresh(client, task_id, success_message, failure_message):
            return
    except OperationFailedError:
        raise
    except Exception as error:
        click.secho(
            f"WebSocket monitoring failed ({error}), falling back to polling...",
            fg="yellow",
        )
    while True:
        data = await client.async_get_task_status(task_id)
        if _task_finished(data, success_message, failure_message):
            return
        await asyncio.sleep(2)


async def _watch_with_refresh(client, task_id, success_message, failure_message):
    try:
        return await _watch_task(client, task_id, success_message, failure_message)
    except AuthError:
        click.secho(
            "WebSocket authentication failed. Attempting to refresh token...",
            fg="yellow",
        )
        await client.authenticate()
        return await _watch_task(client, task_id, success_message, failure_message)


async def _watch_task(client, task_id, success_message, failure_message):
    ws_client = await client.websocket_connect()
    async with ws_client:
        await ws_client.subscribe(f"task:{task_id}")
        # Completion can precede the subscription; always check the snapshot.
        if _task_finished(
            await client.async_get_task_status(task_id),
            success_message,
            failure_message,
        ):
            return True
        messages = ws_client.listen().__aiter__()
        while True:
            try:
                message = await asyncio.wait_for(anext(messages), timeout=5)
            except (TimeoutError, StopAsyncIteration):
                return False
            if (
                message.get("topic") == f"task:{task_id}"
                and message.get("type") == "task_update"
            ):
                if _task_finished(
                    message.get("data", {}), success_message, failure_message
                ):
                    return True
    return False


def _task_finished(data, success_message, failure_message):
    status = data.get("status")
    message = data.get("message", "No message provided.")
    result = data.get("result")
    failed_result = isinstance(result, dict) and result.get("status") in {
        "error",
        "failed",
    }
    if status in {"error", "failed", "cancelled"} or failed_result:
        detail = result.get("message", message) if failed_result else message
        error = data.get("error")
        if isinstance(error, dict):
            detail = error.get("message", detail)
        raise OperationFailedError(f"{failure_message}: {detail}", response_data=data)
    if status in {"success", "completed"}:
        click.secho(f"{success_message}: {message}", fg="green")
        return True
    return False
