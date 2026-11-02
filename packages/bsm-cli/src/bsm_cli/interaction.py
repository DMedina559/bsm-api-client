"""Keep terminal interrupts scoped to the action opened by a menu."""

import asyncio
import signal

import click


async def menu_action(awaitable):
    loop = asyncio.get_running_loop()
    task = asyncio.ensure_future(awaitable)
    interrupted = False

    def interrupt(signum, frame):
        nonlocal interrupted
        interrupted = True
        task.cancel()
        loop.call_soon_threadsafe(task.cancel)

    previous = signal.signal(signal.SIGINT, interrupt)
    try:
        return await task
    except asyncio.CancelledError:
        if not interrupted:
            raise
        raise click.Abort() from None
    finally:
        signal.signal(signal.SIGINT, previous)


def pause_or_exit(message: str = "Press any key to continue...") -> bool:
    """Pause in an interactive menu; return False on Ctrl+C so the caller exits cleanly."""
    try:
        click.pause(message)
        return True
    except (click.Abort, KeyboardInterrupt, EOFError):
        return False
