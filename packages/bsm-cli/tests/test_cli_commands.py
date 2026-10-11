"""Command smoke tests through the real facade and generated HTTP serializers."""

import json
import re
from unittest.mock import AsyncMock

import click
import httpx
import pytest
from click.testing import CliRunner

from bsm_api_client import BedrockServerManagerApi
from bsm_api_client.openapi import generated_schema, resolve
from bsm_cli.__main__ import cli
from bsm_cli.config import Config


def response_for(method, path, values):
    document = generated_schema()
    for template, routes in document["paths"].items():
        pattern = re.sub(r"\{[^}]+\}", "[^/]+", template)
        if re.fullmatch(pattern, path) and method.lower() in routes:
            operation = routes[method.lower()]
            response = next(
                value
                for code, value in operation["responses"].items()
                if str(code).startswith("2")
            )
            spec = (
                response.get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )
            return shape(document, spec, values)
    return values


def shape(document, spec, values):
    spec = resolve(document, spec)
    if "anyOf" in spec:
        spec = next(
            (
                resolve(document, option)
                for option in spec["anyOf"]
                if "task_id" in resolve(document, option).get("properties", {})
            ),
            resolve(document, spec["anyOf"][0]),
        )
    if spec.get("type") == "array":
        return [shape(document, spec["items"], values)]
    if spec.get("type") != "object":
        return values
    result = {
        key: value for key, value in values.items() if key in spec.get("properties", {})
    }
    for key, field in spec.get("properties", {}).items():
        field = resolve(document, field)
        if key == "status" and (
            field.get("enum") == ["accepted"] or field.get("const") == "accepted"
        ):
            result[key] = "accepted"
        if key == "task_id":
            result[key] = "test-task"
    if "task_id" in result:
        result["status"] = "accepted"
    if "details" in result:
        result["details"] = None
    if "players" in result:
        result["players"] = [{"name": "Test Player", "xuid": "123"}]
    return result


SUCCESS = {
    "status": "success",
    "message": "Done",
    "server_name": "test",
    "outcome": "started",
    "servers": [
        {"name": "test", "status": "STOPPED", "version": "1", "player_count": 0}
    ],
    "players": [{"name": "Test Player", "xuid": "123", "ignoresPlayerLimit": False}],
    "permissions": [
        {"name": "Test Player", "xuid": "123", "permission_level": "member"}
    ],
    "raw_content": "server-name=Test Server",
    "properties": {"server-name": "Test Server"},
    "settings": {"settings": {"autostart": False, "autoupdate": False}},
    "plugins": {"demo": {"enabled": True, "version": "1"}},
    "bans": [{"player_name": "Test Player", "xuid": "123", "reason": None}],
    "details": {"removed": ["Test Player"], "not_found": []},
    "addons": {"behavior_packs": [], "resource_packs": []},
    "id": 1,
    "username": "admin",
    "identity_type": "local",
    "role": "admin",
    "is_active": True,
    "registration_url": "http://localhost/register?token=test",
    "process_info": None,
}

# Every curated noninteractive command goes through request serialization and
# response validation, rather than mocking its facade method.
CASES = [
    ("server", "list"),
    ("server", "list", "--server-name", "test"),
    ("server", "start", "-s", "test"),
    ("server", "stop", "-s", "test"),
    ("server", "restart", "-s", "test"),
    ("server", "update", "-s", "test"),
    ("server", "delete", "-s", "test", "--yes"),
    ("server", "send-command", "-s", "test", "say", "hello world"),
    ("account", "details"),
    ("account", "update-theme", "--theme", "dark"),
    (
        "account",
        "update-profile",
        "--full-name",
        "Test User",
        "--email",
        "test@example.com",
    ),
    (
        "account",
        "change-password",
        "--current-password",
        "old-password",
        "--new-password",
        "new-password",
    ),
    ("users", "list"),
    ("users", "delete", "1", "--yes"),
    ("users", "set-role", "1", "moderator"),
    ("users", "enable", "1"),
    ("users", "disable", "1"),
    ("users", "invite", "user"),
    ("plugin", "list"),
    ("plugin", "enable", "demo"),
    ("plugin", "disable", "demo"),
    ("plugin", "reload"),
    ("plugin", "trigger-event", "demo", "--payload-json", '{"value":1}'),
    ("player", "scan"),
    ("player", "add", "-p", "Test Player:123"),
    ("allowlist", "list", "-s", "test"),
    ("allowlist", "add", "-s", "test", "-p", "Test Player", "--ignore-limit"),
    ("allowlist", "remove", "-s", "test", "-p", "Test Player"),
    ("bans", "list", "-s", "test"),
    ("permissions", "list", "-s", "test"),
    ("permissions", "set", "-s", "test", "-p", "Test Player", "-l", "operator"),
    ("properties", "get", "-s", "test"),
    ("properties", "get", "-s", "test", "-p", "server-name"),
    ("properties", "set", "-s", "test", "-p", "server-name=Test Server"),
    ("backup", "create", "-s", "test", "-t", "all"),
    ("backup", "create", "-s", "test", "-t", "config", "-f", "server.properties"),
    ("backup", "restore", "-s", "test", "-f", "world_backup.zip"),
    ("backup", "restore", "-s", "test", "-f", "My Level_backup_20261007.mcworld"),
    ("backup", "restore", "-s", "test", "-f", "custom.zip", "--type", "world"),
    ("backup", "prune", "-s", "test"),
    ("world", "install", "-s", "test", "-f", "world.mcworld", "--yes"),
    ("world", "export", "-s", "test"),
    ("world", "reset", "-s", "test", "--yes"),
    ("addon", "install", "-s", "test", "-f", "addon.mcaddon"),
]


@pytest.fixture
def command_client(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "bsm_cli.config.get_config_path", lambda: tmp_path / "config.json"
    )
    config = Config()
    config.update(jwt_token="token")
    clients = []

    def create(**kwargs):
        client = BedrockServerManagerApi(**kwargs)

        async def request(method, path, **kwargs):
            body = dict(SUCCESS)
            if path == "/api/server/install":
                body.update(status="accepted", task_id="test-task")
            if "restart" in path:
                body["outcome"] = "restarted"
            elif "stop" in path:
                body["outcome"] = "stopped"
            if path.startswith("/api/tasks/"):
                body = {
                    "id": "test-task",
                    "status": "completed",
                    "message": "Done",
                    "result": None,
                    "error": None,
                }
            else:
                body = response_for(method, path, body)
            return httpx.Response(200, json=body)

        client._dynamic_request = AsyncMock(side_effect=request)
        clients.append(client)
        return client

    monkeypatch.setattr("bsm_cli.__main__.BedrockServerManagerApi", create)
    return clients


@pytest.mark.parametrize("args", CASES, ids=lambda args: " ".join(args))
@pytest.mark.parametrize("machine", [False, True], ids=["human", "json"])
def test_curated_commands(command_client, args, machine):
    result = CliRunner().invoke(cli, (["--json"] if machine else []) + list(args))
    assert result.exit_code == 0, result.output
    assert command_client[0]._dynamic_request.await_count
    if machine:
        assert json.loads(result.stdout) is not None
        assert not result.stderr


def command_paths(group, prefix=()):
    yield prefix
    if isinstance(group, click.Group):
        for name, command in group.commands.items():
            yield from command_paths(command, (*prefix, name))


@pytest.mark.parametrize("path", list(command_paths(cli)))
def test_every_command_help(path):
    result = CliRunner().invoke(cli, [*path, "--help"])
    assert result.exit_code == 0, result.output
    assert "Usage:" in result.stdout


@pytest.mark.parametrize(
    "args,code",
    [
        (("properties", "set", "-s", "test", "-p", "broken"), 2),
        (("properties", "set", "-s", "test", "-p", "=value"), 2),
        (("properties", "set", "-s", "test", "-p", "x=1", "-p", "x=2"), 2),
        (("properties", "get", "-s", "test", "-p", "missing"), 5),
        (("permissions", "set", "-s", "test", "-p", "missing", "-l", "member"), 5),
        (("backup", "create", "-s", "test", "-t", "config"), 2),
        (("server", "list", "--loop"), 2),
    ],
)
def test_command_input_errors(command_client, args, code):
    result = CliRunner().invoke(cli, ["--json", *args])
    assert result.exit_code == code, result.output
    assert not result.stdout
    assert json.loads(result.stderr)["exit_code"] == code


@pytest.mark.parametrize("args", CASES, ids=lambda args: " ".join(args))
@pytest.mark.parametrize("machine", [False, True], ids=["human", "json"])
def test_curated_api_failures(monkeypatch, tmp_path, args, machine):
    from bsm_api_client.exceptions import AuthError

    monkeypatch.setattr(
        "bsm_cli.config.get_config_path", lambda: tmp_path / "config.json"
    )
    Config().update(jwt_token="token")

    def create(**kwargs):
        client = BedrockServerManagerApi(**kwargs)
        client._dynamic_request = AsyncMock(side_effect=AuthError("Permission denied"))
        return client

    monkeypatch.setattr("bsm_cli.__main__.BedrockServerManagerApi", create)
    result = CliRunner().invoke(cli, (["--json"] if machine else []) + list(args))
    assert result.exit_code == 3, result.output
    if machine:
        assert not result.stdout
        assert json.loads(result.stderr)["exit_code"] == 3


@pytest.mark.parametrize(
    "args,text,select,confirm",
    [
        (("bans", "add", "-s", "test"), ["New Player", "456", "", ""], [], []),
        (("bans", "remove", "-s", "test"), [], ["123"], [True]),
        (("allowlist", "add", "-s", "test"), ["New Player", ""], [], [True]),
        (
            ("permissions", "set", "-s", "test"),
            [],
            ["Test Player (XUID: 123)", "operator"],
            [False],
        ),
        (("addon", "manage", "-s", "test"), [], ["Back"], []),
        (("server", "settings", "-s", "test"), [], ["cancel"], []),
        (("users",), [], ["Back"], []),
    ],
)
def test_interactive_workflows(
    command_client, monkeypatch, args, text, select, confirm
):
    from bsm_cli import menu_registry

    class Answer:
        def __init__(self, value):
            self.value = value

        async def ask_async(self):
            return self.value

    for method, values in (("text", text), ("select", select), ("confirm", confirm)):
        answers = iter(values)
        monkeypatch.setattr(
            menu_registry.questionary,
            method,
            lambda *a, answers=answers, **k: Answer(next(answers)),
        )
    result = CliRunner().invoke(cli, list(args))
    assert result.exit_code == 0, result.output
    assert command_client[0]._dynamic_request.await_count


def test_content_upload_requires_advertised_endpoint(command_client, tmp_path):
    from bsm_api_client.openapi import generated_schema

    file = tmp_path / "world.mcworld"
    file.write_bytes(b"content")
    # The pinned backend has no public upload endpoint. Report that explicitly.
    original = BedrockServerManagerApi._fetch_openapi_schema
    try:
        BedrockServerManagerApi._fetch_openapi_schema = AsyncMock(
            return_value=generated_schema()
        )
        result = CliRunner().invoke(cli, ["--json", "content", "upload", str(file)])
    finally:
        BedrockServerManagerApi._fetch_openapi_schema = original
    assert result.exit_code == 5, result.output
    assert "upload_content" in json.loads(result.stderr)["error"]


def test_server_install_interactive(command_client, monkeypatch):
    from bsm_cli import menu_registry

    class Answer:
        def __init__(self, value):
            self.value = value

        async def ask_async(self):
            return self.value

    values = iter(["new-server", "LATEST"])
    choices = iter([False, False, False, False])
    monkeypatch.setattr(
        menu_registry.questionary, "text", lambda *a, **k: Answer(next(values))
    )
    monkeypatch.setattr(
        menu_registry.questionary, "confirm", lambda *a, **k: Answer(next(choices))
    )
    monkeypatch.setattr("bsm_cli.server.interactive_properties_workflow", AsyncMock())
    monkeypatch.setattr("bsm_cli.server.monitor_task", AsyncMock())
    result = CliRunner().invoke(cli, ["server", "install"])
    assert result.exit_code == 0, result.output
    request = command_client[0]._dynamic_request.call_args.kwargs["raw_request"]
    assert json.loads(request.content)["server_name"] == "new-server"


def test_cancelled_ban_reason_does_not_ban(command_client, monkeypatch):
    from bsm_cli import menu_registry

    class Answer:
        async def ask_async(self):
            return next(answers)

    answers = iter(["New Player", "456", None])
    monkeypatch.setattr(menu_registry.questionary, "text", lambda *a, **k: Answer())
    result = CliRunner().invoke(cli, ["bans", "add", "-s", "test"])
    assert result.exit_code == 0, result.output
    assert command_client[0]._dynamic_request.await_count == 1


def test_cancelled_allowlist_confirmation_does_not_add(command_client, monkeypatch):
    from bsm_cli import menu_registry

    class Answer:
        def __init__(self, value):
            self.value = value

        async def ask_async(self):
            return self.value

    monkeypatch.setattr(
        menu_registry.questionary, "text", lambda *a, **k: Answer("New Player")
    )
    monkeypatch.setattr(
        menu_registry.questionary, "confirm", lambda *a, **k: Answer(None)
    )
    result = CliRunner().invoke(cli, ["allowlist", "add", "-s", "test"])
    assert result.exit_code == 0, result.output
    assert command_client[0]._dynamic_request.await_count == 1


@pytest.mark.asyncio
async def test_registry_blank_property_name(command_client, monkeypatch, capsys):
    from bsm_cli.menu_registry import command_menu

    class Answer:
        def __init__(self, value):
            self.value = value

        async def ask_async(self):
            return self.value

    # Initialize the real facade used by the command smoke tests.
    client = BedrockServerManagerApi(
        base_url="http://localhost", jwt_token="test-token"
    )
    client._dynamic_request = AsyncMock(
        return_value=httpx.Response(
            200,
            json={
                "status": "success",
                "properties": {"server-name": "Test Server"},
                "raw_content": "server-name=Test Server",
            },
        )
    )
    answers = iter(["test", ""])
    selections = iter(["get", "Back"])
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    monkeypatch.setattr(
        "bsm_cli.menu_registry._resource_choices", AsyncMock(return_value=[])
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select",
        lambda *a, **k: Answer(next(selections)),
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.text", lambda *a, **k: Answer(next(answers))
    )
    try:
        with click.Context(cli, obj={"client": client}) as ctx:
            await command_menu(ctx, cli.commands["properties"])
        assert "server-name = Test Server" in capsys.readouterr().out
    finally:
        await client.close()
