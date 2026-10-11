"""CLI discovery, validation, machine output, and exit code behavior."""

import json
from unittest.mock import AsyncMock

import pytest
from click.testing import CliRunner

from bsm_api_client.dynamic import DynamicOpenAPIMixin
from bsm_api_client.exceptions import (
    AuthError,
    CannotConnectError,
    InvalidInputError,
    NotFoundError,
)
from bsm_cli.__main__ import cli
from bsm_cli.completion import complete_operation, complete_parameter, complete_plugin
from bsm_cli.config import Config
from bsm_cli.output import normalize_error

SCHEMA = {
    "openapi": "3.1.0",
    "info": {"title": "Test", "version": "1"},
    "paths": {
        "/extra/{name}": {
            "parameters": [
                {
                    "in": "path",
                    "name": "name",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "post": {
                "operationId": "demo_action",
                "x-bsm-plugin": "demo",
                "tags": ["Plugin:demo"],
                "parameters": [
                    {"in": "query", "name": "enabled", "schema": {"type": "boolean"}}
                ],
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": {"type": "object"}}},
                },
            },
        },
        "/api/info": {"get": {"operationId": "info", "tags": ["Application"]}},
    },
}


class FakeConfig(Config):
    def __init__(self):
        self._config = {"jwt_token": "token"}
        self._config["openapi_cache"] = {"base_url": self.base_url, "schema": SCHEMA}

    def set(self, key, value):
        self._config[key] = value


class FakeClient(DynamicOpenAPIMixin):
    def __init__(self):
        self._fetch_openapi_schema = AsyncMock(return_value=SCHEMA)
        self.async_call_operation = AsyncMock(return_value={"status": "success"})
        self.close = AsyncMock()
        self.async_get_servers = AsyncMock(return_value={"servers": []})


@pytest.fixture
def client(monkeypatch):
    fake = FakeClient()
    monkeypatch.setattr("bsm_cli.__main__.Config", FakeConfig)
    monkeypatch.setattr(
        "bsm_cli.__main__.BedrockServerManagerApi", lambda **kwargs: fake
    )
    return fake


def run(*args):
    return CliRunner().invoke(cli, list(args))


def test_dynamic_error_response_exits_nonzero(client):
    client.async_call_operation.return_value = {
        "status": "error",
        "message": "Rejected",
    }
    result = run(
        "--json", "api", "call", "demo_action", "--param", "name=test", "--json", "{}"
    )
    assert result.exit_code == 1
    assert not result.stdout
    assert "Rejected" in json.loads(result.stderr)["error"]


def test_root_parse_error_respects_json():
    result = run("--json", "--unknown")
    assert result.exit_code == 2
    assert json.loads(result.stderr)["exit_code"] == 2


@pytest.mark.asyncio
async def test_registry_menu_accepts_optional_body_and_missing_defaults(
    client, monkeypatch
):
    import click

    from bsm_cli.api import api
    from bsm_cli.menu_registry import command_menu

    class Answer:
        def __init__(self, value):
            self.value = value

        async def ask_async(self):
            return self.value

    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.confirm",
        lambda *a, **k: Answer(k.get("default", False)),
    )
    selections = iter(["call", "Back"])
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    monkeypatch.setattr(
        "bsm_cli.menu_registry._resource_choices", AsyncMock(return_value=[])
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select",
        lambda *a, **k: Answer(next(selections)),
    )
    values = iter(["demo_action", "name=test", "{}", "", ""])
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.text", lambda *a, **k: Answer(next(values))
    )
    with click.Context(cli, obj={"client": client, "json_output": True}) as ctx:
        await command_menu(ctx, api)
    assert client.async_call_operation.call_args.kwargs["json_data"] == {}


def test_json_operations_and_plugin_scope(client):
    result = run("--json", "api", "operations", "--tag", "Plugin:demo")
    assert result.exit_code == 0, result.output
    assert [op["operation_id"] for op in json.loads(result.stdout)] == ["demo_action"]
    result = run("--json", "plugin", "operations", "demo")
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)[0]["plugin"] == "demo"
    result = run(
        "--json",
        "plugin",
        "call",
        "wrong",
        "demo_action",
        "--param",
        "name=one",
        "--json",
        "{}",
    )
    assert result.exit_code == 5
    client.async_call_operation.assert_not_awaited()


def test_call_parses_parameters_and_body(client):
    result = run(
        "--json",
        "api",
        "call",
        "demo_action",
        "--param",
        "name=My Server",
        "--param",
        "enabled=true",
        "--json",
        '{"value": 1}',
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) == {"status": "success"}
    client.async_call_operation.assert_awaited_once_with(
        "demo_action",
        path_params={"name": "My Server"},
        query={"enabled": True},
        headers={},
        json_data={"value": 1},
        form_data=None,
        authenticated=False,
    )


@pytest.mark.parametrize(
    "params",
    [
        [],
        ["--param", "name=one", "--param", "enabled=maybe"],
        ["--param", "name=one", "--param", "extra=bad"],
    ],
)
def test_invalid_parameters_do_not_send_requests(client, params):
    result = run("--json", "api", "call", "demo_action", *params, "--json", "{}")
    assert result.exit_code == 2, result.output
    assert json.loads(result.stderr)["exit_code"] == 2
    client.async_call_operation.assert_not_awaited()


def test_export_refresh_and_saved_schema_diff(client, tmp_path):
    output = tmp_path / "schema.json"
    result = run("--json", "api", "export", str(output))
    assert result.exit_code == 0, result.output
    assert json.loads(output.read_text()) == SCHEMA
    result = run("--json", "api", "diff", "--against", str(output))
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["changed"] == []
    result = run("--json", "api", "refresh")
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["diff"]["added"] == []


def test_human_operations_table_and_machine_curated_response(client):
    result = run("api", "operations")
    assert result.exit_code == 0, result.output
    assert "METHOD" in result.stdout and "demo_action" in result.stdout
    result = run("--json", "server", "list")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"servers": []}


def test_curated_command_has_structured_response(client):
    from bsm_api_client.models import ServersListResponse

    client.async_get_servers.return_value = ServersListResponse(
        status="success", servers=[]
    )
    result = run("--json", "server", "list")
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["servers"] == []
    assert "SERVER NAME" not in result.stdout


@pytest.mark.parametrize(
    "error,code",
    [
        (AuthError("auth"), 3),
        (CannotConnectError("offline"), 4),
        (NotFoundError("missing"), 5),
        (InvalidInputError("invalid"), 2),
    ],
)
def test_errors_have_consistent_exit_codes(client, error, code):
    client._fetch_openapi_schema.side_effect = error
    result = run("--json", "api", "info")
    assert result.exit_code == code, result.output
    assert result.stdout == ""
    assert json.loads(result.stderr)["exit_code"] == code
    assert normalize_error(error).exit_code == code


def test_completion_uses_cache_without_discovering(client):
    import click

    ctx = click.Context(cli, obj={"config": FakeConfig()})
    ctx.params["operation_id"] = "demo_action"
    assert [item.value for item in complete_operation(ctx, None, "demo")] == [
        "demo_action"
    ]
    assert complete_plugin(ctx, None, "d") == ["demo"]
    assert complete_parameter(ctx, None, "n") == ["name="]
    client._fetch_openapi_schema.assert_not_awaited()


def test_server_completion_ignores_another_servers_cache(client):
    import click

    from bsm_cli.completion import complete_server

    config = FakeConfig()
    config.set(
        "server_cache", {"base_url": config.base_url, "names": ["alpha", "beta"]}
    )
    ctx = click.Context(cli, obj={"config": config})
    assert complete_server(ctx, None, "a") == ["alpha"]
    config.set("base_url", "http://other:11325")
    assert complete_server(ctx, None, "") == []


def test_curated_failure_returns_nonzero_status(client):
    from bsm_api_client.exceptions import OperationFailedError

    client.async_get_servers.side_effect = OperationFailedError("Failed")
    result = run("--json", "server", "list")
    assert result.exit_code == 1
    assert json.loads(result.stderr)["exit_code"] == 1


@pytest.mark.parametrize(
    "args",
    [("api", "--help"), ("plugin", "call", "--help"), ("--json", "api", "--help")],
)
def test_nested_help_exits_successfully(client, args):
    result = run(*args)
    assert result.exit_code == 0, result.output
    assert "Usage:" in result.stdout


@pytest.mark.parametrize("cache", [None, {}, [], "invalid", {"schema": None}])
def test_refresh_after_login_clears_cache(client, monkeypatch, cache):
    config = FakeConfig()
    config.set("openapi_cache", cache)
    config.set("server_cache", None)
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    result = run("--json", "api", "refresh")
    assert result.exit_code == 0, result.output
    assert config.get("openapi_cache")["schema"] == SCHEMA
    assert json.loads(result.stdout)["diff"]["added"]


@pytest.mark.parametrize("cache", [None, [], "invalid", {"names": None}])
def test_completion_handles_cleared_caches(client, cache):
    import click

    from bsm_cli.completion import complete_server

    config = FakeConfig()
    if isinstance(cache, dict):
        cache = {"base_url": config.base_url, **cache}
    config.set("openapi_cache", cache)
    config.set("server_cache", cache)
    ctx = click.Context(cli, obj={"config": config})
    assert complete_operation(ctx, None, "") == []
    assert complete_plugin(ctx, None, "") == []
    assert complete_parameter(ctx, None, "") == []
    assert complete_server(ctx, None, "") == []
    client._fetch_openapi_schema.assert_not_awaited()


@pytest.mark.parametrize(
    "kind,value,expected",
    [("integer", "3", 3), ("boolean", "false", False), ("number", "1.5", 1.5)],
)
def test_nullable_parameter_types(kind, value, expected):
    from bsm_cli.api import parameter_value

    parameter = {
        "name": "optional",
        "schema": {"anyOf": [{"type": kind}, {"type": "null"}]},
    }
    assert parameter_value({}, parameter, value) == expected


def test_missing_upload_file_is_input_error(client):
    result = run(
        "--json",
        "api",
        "call",
        "demo_action",
        "--param",
        "name=test",
        "--file",
        "file=/missing/file",
    )
    assert result.exit_code == 2, result.output
    assert json.loads(result.stderr)["exit_code"] == 2
    client.async_call_operation.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["diff", "operations"])
async def test_registry_blank_api_options(client, monkeypatch, capsys, name):
    import click

    from bsm_cli.api import api
    from bsm_cli.menu_registry import command_menu

    class Answer:
        def __init__(self, value):
            self.value = value

        async def ask_async(self):
            return self.value

    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.confirm",
        lambda *a, **k: Answer(k.get("default", False)),
    )
    selections = iter([name, "Back"])
    monkeypatch.setattr("click.pause", lambda *a, **k: None)
    monkeypatch.setattr(
        "bsm_cli.menu_registry._resource_choices", AsyncMock(return_value=[])
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.select",
        lambda *a, **k: Answer(next(selections)),
    )
    monkeypatch.setattr(
        "bsm_cli.menu_registry.questionary.text", lambda *a, **k: Answer("")
    )
    with click.Context(cli, obj={"client": client, "json_output": False}) as ctx:
        await command_menu(ctx, api)
    output = capsys.readouterr().out
    assert output
    if name == "operations":
        assert "demo_action" in output
        assert "/api/info" in output


@pytest.mark.parametrize(
    "schema",
    [
        {"paths": []},
        {"paths": {"/bad": None}},
        {"paths": {"/bad": {"get": {"parameters": [None]}}}},
    ],
)
def test_malformed_cached_contract_is_ignored(client, schema):
    import click

    config = FakeConfig()
    config.set("openapi_cache", {"base_url": config.base_url, "schema": schema})
    ctx = click.Context(cli, obj={"config": config})
    assert complete_operation(ctx, None, "") == []
    assert complete_plugin(ctx, None, "") == []
    assert complete_parameter(ctx, None, "") == []
    client._fetch_openapi_schema.assert_not_awaited()


def test_completion_checks_fingerprint_identity_and_suggests_boolean_values(client):
    import click

    config = FakeConfig()
    ctx = click.Context(cli, obj={"config": config})
    ctx.params["operation_id"] = "demo_action"
    assert complete_parameter(ctx, None, "enabled=f") == ["enabled=false"]
    config.set(
        "openapi_cache",
        {"base_url": config.base_url, "schema": SCHEMA, "fingerprint": "invalid"},
    )
    assert complete_operation(ctx, None, "") == []
    config.set(
        "openapi_cache",
        {"base_url": config.base_url, "schema": SCHEMA, "username": "another-user"},
    )
    assert complete_operation(ctx, None, "") == []


def test_operation_filters_and_detailed_compatibility(client, tmp_path):
    result = run("--json", "api", "operations", "--method", "post", "--plugin", "demo")
    assert result.exit_code == 0, result.output
    assert [op["operation_id"] for op in json.loads(result.stdout)] == ["demo_action"]
    output = tmp_path / "before.json"
    output.write_text(json.dumps(SCHEMA))
    result = run("--json", "api", "diff", "--against", str(output), "--details")
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["compatibility"] == {
        "compatible": True,
        "changes": [],
    }
    output.write_text("invalid JSON")
    result = run("--json", "api", "diff", "--against", str(output))
    assert result.exit_code == 2
    assert json.loads(result.stderr)["exit_code"] == 2
