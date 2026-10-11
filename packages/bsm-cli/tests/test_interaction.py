"""Interrupting a live menu action preserves its caller and cleans up the view."""

import asyncio
import signal

import click
import pytest

from bsm_cli.interaction import menu_action


@pytest.mark.asyncio
async def test_interrupt_closes_view_and_returns_control_to_menu():
    previous = signal.getsignal(signal.SIGINT)
    cleaned = []

    async def view():
        try:
            signal.raise_signal(signal.SIGINT)
            await asyncio.sleep(0)
        finally:
            cleaned.append(True)

    with pytest.raises(click.Abort):
        await menu_action(view())
    assert cleaned == [True]
    assert signal.getsignal(signal.SIGINT) == previous
    assert await menu_action(asyncio.sleep(0, result="next action")) == "next action"


@pytest.mark.asyncio
async def test_external_cancellation_is_not_treated_as_user_interrupt():
    async def view():
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        await menu_action(view())
