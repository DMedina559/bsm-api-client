"""Keep terminal interrupts scoped to the action opened by a menu."""

import asyncio
import signal

import click


async def menu_action(awaitable):
    task = asyncio.ensure_future(awaitable)
    interrupted = False

    def interrupt(signum, frame):
        nonlocal interrupted
        interrupted = True
        task.cancel()

    previous = signal.signal(signal.SIGINT, interrupt)
    try:
        return await task
    except asyncio.CancelledError:
        if not interrupted:
            raise
        raise click.Abort() from None
    finally:
        signal.signal(signal.SIGINT, previous)
