"""Registry prompts preserve values, conceal passwords, and support cancellation."""

from unittest.mock import AsyncMock

import click
import pytest

from bsm_cli.menu_registry import command_menu


class Answer:
    def __init__(self, value):
        self.value = value

    async def ask_async(self):
        return self.value


@pytest.mark.asyncio
async def test_registry_preserves_spaces_and_multiple_values(monkeypatch):
    received = []

    @click.group()
    def group():
        pass

    @group.command()
    @click.option("--values", multiple=True)
    @click.option("--enabled", is_flag=True)
    async def command(values, enabled):
        received.append((values, enabled))

    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select", lambda *a, **k: Answer("command")
    )
    answers = iter(['["player=Test Player", "server=My Server"]', "false"])
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.text", lambda *a, **k: Answer(next(answers))
    )
    with click.Context(group) as ctx:
        await command_menu(ctx, group)
    assert received == [(("player=Test Player", "server=My Server"), False)]


@pytest.mark.asyncio
@pytest.mark.parametrize("confirmation", ["secret", "different", None])
async def test_registry_password_confirmation(monkeypatch, confirmation):
    called = AsyncMock()

    @click.group()
    def group():
        pass

    @group.command()
    @click.option("--password", hide_input=True, confirmation_prompt=True)
    async def command(password):
        await called(password)

    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select", lambda *a, **k: Answer("command")
    )
    answers = iter(["secret", confirmation])
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.password",
        lambda *a, **k: Answer(next(answers)),
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.text",
        lambda *a, **k: pytest.fail("Password displayed"),
    )
    with click.Context(group) as ctx:
        if confirmation == "different":
            with pytest.raises(click.BadParameter, match="Confirmation"):
                await command_menu(ctx, group)
        else:
            await command_menu(ctx, group)
    if confirmation == "secret":
        called.assert_awaited_once_with("secret")
    else:
        called.assert_not_awaited()
