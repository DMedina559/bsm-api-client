"""Registry prompts preserve values, conceal passwords, and support cancellation."""

from copy import copy
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

    selections = iter(["command", "Back"])
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    monkeypatch.setattr(
        "bsm_cli.menu_registry._resource_choices", AsyncMock(return_value=[])
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select",
        lambda *a, **k: Answer(next(selections)),
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.confirm", lambda *a, **k: Answer(False)
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

    selections = iter(["command", "Back"])
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    monkeypatch.setattr(
        "bsm_cli.menu_registry._resource_choices", AsyncMock(return_value=[])
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select",
        lambda *a, **k: Answer(next(selections)),
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


def optional_commands():
    from bsm_cli.__main__ import cli

    def walk(group, path=()):
        for name, command in group.commands.items():
            if isinstance(command, click.Group):
                yield from walk(command, (*path, name))
            elif any(not param.required for param in command.params):
                yield (*path, name), command

    return list(walk(cli))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path,original", optional_commands(), ids=lambda value: str(value)
)
async def test_blank_menu_options_match_command_line_defaults(
    monkeypatch, path, original
):
    """Cover optional parameters from every registered CLI command."""
    params = [copy(param) for param in original.params if not param.required]
    for param in params:
        if isinstance(param, click.Option):
            param.prompt = None
    received = []
    command = click.Command(
        "command", params=params, callback=lambda **kw: received.append(kw)
    )
    group = click.Group("group", commands={"command": command})
    with command.make_context("command", []) as parsed:
        expected = dict(parsed.params)
    selections = iter(["command", "Back"])
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    monkeypatch.setattr(
        "bsm_cli.menu_registry._resource_choices", AsyncMock(return_value=[])
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select",
        lambda *a, **k: Answer(next(selections)),
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.confirm",
        lambda *a, **k: Answer(k.get("default", False)),
    )
    for prompt in ("text", "password"):
        monkeypatch.setattr(
            f"bsm_cli.menu_registry.questionary.{prompt}", lambda *a, **k: Answer("")
        )
    with click.Context(group) as ctx:
        await command_menu(ctx, group)
    assert received == [expected], path
