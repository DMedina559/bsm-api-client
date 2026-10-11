"""Registry prompts preserve values, conceal passwords, and support cancellation."""

from copy import copy
from unittest.mock import AsyncMock, Mock

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


@pytest.mark.asyncio
async def test_menu_lists_before_actions_and_refreshes_after_changes(monkeypatch):
    events = []

    @click.group()
    def group():
        pass

    @group.command("list")
    @click.option("--server-name", required=True)
    async def listing(server_name):
        events.append(("list", server_name))

    @group.command("change")
    @click.option("--server-name", required=True)
    async def change(server_name):
        events.append(("change", server_name))

    monkeypatch.setattr(
        "bsm_cli.menu_registry._prompt_parameter", AsyncMock(return_value="alpha")
    )
    selections = iter(["change", "Back"])

    def select(*args, **kwargs):
        events.append(("menu",))
        return Answer(next(selections))

    monkeypatch.setattr("questionary.select", select)
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    with click.Context(group) as ctx:
        await command_menu(ctx, group)
    assert events == [
        ("list", "alpha"),
        ("menu",),
        ("change", "alpha"),
        ("list", "alpha"),
        ("menu",),
    ]
    from bsm_cli import menu_registry

    assert menu_registry._prompt_parameter.await_count == 1


@pytest.mark.asyncio
async def test_home_opens_server_directly_and_has_no_duplicate_command_groups(
    monkeypatch,
):
    from bsm_api_client.models import ServersListResponse, ServerSummary
    from bsm_cli.__main__ import cli
    from bsm_cli.main_menus import main_menu

    client = AsyncMock()
    client.async_get_servers.return_value = ServersListResponse(
        status="success",
        servers=[
            ServerSummary(name="alpha", status="STOPPED", version="1", player_count=0)
        ],
    )
    opened = AsyncMock()
    table = Mock()
    monkeypatch.setattr("bsm_cli.main_menus._print_server_table", table)
    monkeypatch.setattr("bsm_cli.main_menus.manage_server_menu", opened)
    monkeypatch.setattr("click.clear", lambda: None)
    answers = iter([("server", "alpha"), "Exit"])
    observed = []

    def select(*args, **kwargs):
        observed.extend(kwargs["choices"])
        return Answer(next(answers))

    monkeypatch.setattr("questionary.select", select)
    with click.Context(cli, obj={"client": client, "cli": cli}) as ctx:
        await main_menu(ctx)
    opened.assert_awaited_once()
    assert opened.await_args.args[1] == "alpha"
    assert table.call_count == 2
    table.assert_called_with(client.async_get_servers.return_value.servers)
    assert "Monitor" in observed
    assert not any(isinstance(value, str) and "Commands" in value for value in observed)


def test_workflows_have_one_canonical_command_path():
    from bsm_cli.__main__ import cli

    assert "manager" not in cli.commands
    assert "system" not in cli.commands
    for name in (
        "overview",
        "monitor",
        "settings",
        "health",
        "audit",
        "logs",
        "operations",
    ):
        assert name in cli.commands
    assert "monitor" in cli.commands["server"].commands
    assert "settings" in cli.commands["server"].commands


@pytest.mark.asyncio
async def test_operations_selects_task_without_another_menu(monkeypatch):
    from types import SimpleNamespace

    from bsm_cli.__main__ import cli
    from bsm_cli.main_menus import operations_menu
    from bsm_cli.manager import show_task

    client = AsyncMock()
    client.async_list_tasks.return_value = [
        SimpleNamespace(id="task-123", status="completed", message="Backup finished")
    ]
    invoked = AsyncMock()
    monkeypatch.setattr("bsm_cli.main_menus._invoke", invoked)
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    answers = iter(["task-123", "back"])
    monkeypatch.setattr("questionary.select", lambda *a, **k: Answer(next(answers)))
    with click.Context(cli, obj={"client": client, "cli": cli}) as ctx:
        await operations_menu(ctx)
        invoked.assert_awaited_once_with(ctx, show_task, task_id="task-123")
    assert client.async_list_tasks.await_count == 2


@pytest.mark.asyncio
async def test_home_connection_failure_can_exit_without_retry_loop(monkeypatch, capsys):
    from bsm_api_client.exceptions import CannotConnectError
    from bsm_cli.__main__ import cli
    from bsm_cli.main_menus import main_menu

    client = AsyncMock()
    client.async_get_servers.side_effect = CannotConnectError("ClientOSError")
    monkeypatch.setattr("click.clear", lambda: None)
    monkeypatch.setattr("questionary.select", lambda *a, **k: Answer("Exit"))
    with click.Context(cli, obj={"client": client, "cli": cli}) as ctx:
        await main_menu(ctx)
    assert client.async_get_servers.await_count == 1
    assert "Connection: Unavailable" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_home_connection_retry_recovers(monkeypatch):
    from bsm_api_client.exceptions import CannotConnectError
    from bsm_api_client.models import ServersListResponse
    from bsm_cli.__main__ import cli
    from bsm_cli.main_menus import main_menu

    client = AsyncMock()
    client.async_get_servers.side_effect = [
        CannotConnectError("ClientOSError"),
        ServersListResponse(status="success", servers=[]),
    ]
    answers = iter(["Retry", "Exit"])
    monkeypatch.setattr("click.clear", lambda: None)
    monkeypatch.setattr("questionary.select", lambda *a, **k: Answer(next(answers)))
    with click.Context(cli, obj={"client": client, "cli": cli}) as ctx:
        await main_menu(ctx)
    assert client.async_get_servers.await_count == 2


def test_shared_header_uses_backend_version_and_splash(monkeypatch, capsys):
    from bsm_cli.presentation import screen_header

    monkeypatch.setattr("click.clear", lambda: None)
    with click.Context(
        click.Command("menu"),
        obj={
            "app_info": {
                "app_version": "4.0.0b2",
                "splash_text": "Your worlds. Your infrastructure.",
            }
        },
    ):
        screen_header("Manage server · alpha")
    output = capsys.readouterr().out
    assert "Bedrock Server Manager · 4.0.0b2" in output
    assert "Your worlds. Your infrastructure." in output
    assert "Manage server · alpha" in output


def test_command_menu_separates_inspection_and_management():
    from bsm_cli.menu_registry import _command_choices

    group = click.Group(
        "example",
        commands={
            "list": click.Command("list"),
            "show": click.Command("show"),
            "set": click.Command("set"),
        },
    )
    choices = _command_choices(group)
    titles = [
        choice.title if hasattr(choice, "title") else choice for choice in choices
    ]
    assert "── View and inspect ──" in titles
    assert "── Manage ──" in titles
    assert "List" not in titles
