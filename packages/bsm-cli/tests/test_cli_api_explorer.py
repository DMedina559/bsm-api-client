"""API explorer flows preserve machine output and validate before execution."""

import json
from unittest.mock import AsyncMock

import httpx
import pytest
from click.testing import CliRunner

from bsm_api_client import BedrockServerManagerApi
from bsm_cli.__main__ import cli
from bsm_cli.config import Config

SCHEMA = {
    "openapi": "3.1.0",
    "info": {"title": "Explorer", "version": "1"},
    "servers": [{"url": "https://unrelated.invalid"}],
    "paths": {
        "/api/fixture/{name}": {
            "post": {
                "operationId": "fixture_action",
                "tags": ["Fixture"],
                "summary": "Run fixture",
                "parameters": [
                    {
                        "name": "name",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string", "minLength": 1},
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Fixture"}
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Fixture"}
                            }
                        },
                    }
                },
            }
        },
        "/api/rows": {
            "get": {
                "operationId": "rows",
                "responses": {"200": {"description": "Rows"}},
            }
        },
    },
    "components": {
        "schemas": {
            "Fixture": {
                "type": "object",
                "required": ["enabled"],
                "additionalProperties": False,
                "properties": {
                    "enabled": {"type": "boolean"},
                    "password": {"type": "string", "writeOnly": True},
                },
            }
        }
    },
}


@pytest.fixture
def transport(monkeypatch):
    requests = []

    class FakeConfig(Config):
        def __init__(self):
            self._config = {"jwt_token": "token", "base_url": "http://backend"}

    def handler(request):
        requests.append(request)
        if request.url.path == "/api/rows":
            return httpx.Response(
                200,
                json=[{"name": f"row-{i}", "enabled": i % 2 == 0} for i in range(60)],
            )
        return httpx.Response(
            201, json={"enabled": False}, headers={"x-test": "metadata"}
        )

    def create(**kwargs):
        client = BedrockServerManagerApi(
            "http://backend",
            jwt_token="token",
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )
        client._fetch_openapi_schema = AsyncMock(return_value=SCHEMA)
        return client

    monkeypatch.setattr("bsm_cli.__main__.Config", FakeConfig)
    monkeypatch.setattr("bsm_cli.__main__.BedrockServerManagerApi", create)
    return requests


def run(*args):
    return CliRunner().invoke(cli, list(args))


def test_model_and_operation_inspection_preserve_raw_json(transport):
    result = run("api", "models", "--search", "fixture")
    assert result.exit_code == 0, result.output
    assert "Fixture" in result.output
    result = run("api", "model", "Fixture")
    assert result.exit_code == 0, result.output
    assert "enabled" in result.output and "required" in result.output
    result = run("--json", "api", "model", "Fixture")
    assert json.loads(result.stdout) == SCHEMA["components"]["schemas"]["Fixture"]
    result = run("api", "operation", "fixture_action")
    assert result.exit_code == 0, result.output
    assert "POST" in result.output and "Parameters" in result.output
    result = run("--json", "api", "operations", "--search", "run fixture")
    assert [item["operation_id"] for item in json.loads(result.stdout)] == [
        "fixture_action"
    ]


def test_preview_redacts_and_never_calls_backend(transport):
    result = run(
        "--json",
        "api",
        "call",
        "fixture_action",
        "--param",
        "name=test",
        "--json",
        '{"enabled":false,"password":"secret-value"}',
        "--dry-run",
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["body"] == {
        "enabled": False,
        "password": "[redacted]",
    }
    assert not transport
    invalid = run(
        "--json",
        "api",
        "call",
        "fixture_action",
        "--param",
        "name=test",
        "--json",
        '{"enabled":"false"}',
        "--dry-run",
    )
    assert invalid.exit_code == 2, invalid.output
    assert not transport


def test_detailed_responses_and_saved_contract_use_configured_backend(
    transport, tmp_path
):
    path = tmp_path / "contract.json"
    path.write_text(json.dumps(SCHEMA))
    result = run(
        "--json",
        "api",
        "--schema-file",
        str(path),
        "call",
        "fixture_action",
        "--param",
        "name=hello world",
        "--json",
        '{"enabled":false}',
        "--details",
    )
    assert result.exit_code == 0, result.output
    data = json.loads(result.stdout)
    assert data["status_code"] == 201 and data["headers"]["x-test"] == "metadata"
    assert data["data"] == {"enabled": False} and data["duration_ms"] >= 0
    assert str(transport[0].url) == "http://backend/api/fixture/hello%20world"


def test_human_responses_are_bounded_but_machine_output_is_complete(transport):
    result = run("api", "call", "rows")
    assert result.exit_code == 0, result.output
    assert "page 1/3" in result.output and "row-59" not in result.output
    result = run("--json", "api", "call", "rows")
    assert len(json.loads(result.stdout)) == 60
    result = run("api", "call", "rows", "--raw")
    assert len(json.loads(result.stdout)) == 60


class Answer:
    def __init__(self, value):
        self.value = value

    async def ask_async(self):
        return self.value


@pytest.mark.asyncio
async def test_typed_prompts_preserve_false_and_reprompt_invalid_input(monkeypatch):
    from bsm_cli.api_explorer import prompt_value

    text = iter(["bad", "0", "3"])
    monkeypatch.setattr(
        "bsm_cli.api_explorer.questionary.text", lambda *a, **k: Answer(next(text))
    )
    assert await prompt_value(SCHEMA, {"type": "integer", "minimum": 1}, "count") == 3
    monkeypatch.setattr(
        "bsm_cli.api_explorer.questionary.select", lambda *a, **k: Answer(1)
    )
    assert await prompt_value(SCHEMA, {"type": "boolean"}, "enabled") is False


@pytest.mark.asyncio
async def test_cancelled_prompt_never_sends_request(monkeypatch, transport):
    from bsm_api_client.openapi import index_operations
    from bsm_cli.api_explorer import build_request

    monkeypatch.setattr(
        "bsm_cli.api_explorer.questionary.text", lambda *a, **k: Answer(None)
    )
    import click

    with pytest.raises(click.Abort):
        await build_request(SCHEMA, index_operations(SCHEMA)["fixture_action"])
    assert not transport


def test_interactive_request_and_response_workflow(transport, monkeypatch):
    selections = iter(
        [
            "Operations",
            "fixture_action",
            "Build request",
            "Guided fields",
            1,
            "Execute",
            "Headers",
            "Raw JSON",
            "Back",
            "Back",
            "Back",
        ]
    )
    monkeypatch.setattr(
        "bsm_cli.api_explorer.questionary.select",
        lambda *a, **k: Answer(next(selections)),
    )
    monkeypatch.setattr(
        "bsm_cli.api_explorer.questionary.confirm", lambda *a, **k: Answer(False)
    )
    monkeypatch.setattr(
        "bsm_cli.api_explorer.questionary.text", lambda *a, **k: Answer("test")
    )
    result = run("api", "explore")
    assert result.exit_code == 0, result.output
    assert len(transport) == 1
    assert json.loads(transport[0].content) == {"enabled": False}
    assert "HTTP 201" in result.output and "metadata" in result.output


@pytest.mark.asyncio
async def test_detailed_response_retains_cli_failure_policy():
    from types import SimpleNamespace

    from bsm_api_client.exceptions import OperationFailedError
    from bsm_cli.output import RecordingClient

    client = SimpleNamespace(
        async_call_operation=AsyncMock(
            return_value={
                "status_code": 200,
                "headers": {},
                "data": {"status": "error", "message": "Rejected"},
            }
        )
    )
    with pytest.raises(OperationFailedError, match="Rejected"):
        await RecordingClient(client).async_call_operation("operation", detailed=True)


@pytest.mark.parametrize("destination", ["Operations", "Models"])
def test_searchable_pickers_accept_j_and_k(destination, transport, monkeypatch):
    """Construct the real Questionary prompt and exercise its search bindings."""
    from copy import deepcopy

    import questionary
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput

    from bsm_cli import api_explorer

    document = deepcopy(SCHEMA)
    document["paths"]["/api/fixture/{name}"]["post"]["operationId"] = "jk_action"
    document["components"]["schemas"]["JkModel"] = {"type": "object"}
    monkeypatch.setitem(globals(), "SCHEMA", document)
    menu = iter([destination, "Back"])
    real_select = questionary.select
    searched = []
    shown = []
    operation_menu = AsyncMock()
    monkeypatch.setattr(api_explorer, "operation_menu", operation_menu)
    monkeypatch.setattr(
        api_explorer, "show_model", lambda doc, name, spec: shown.append(name)
    )

    with create_pipe_input() as pipe:

        def select(message, **kwargs):
            if kwargs.get("use_search_filter"):
                if searched:
                    return Answer("Back")
                searched.append(message)
                prompt = real_select(
                    message, **kwargs, input=pipe, output=DummyOutput()
                )
                pipe.send_text("jk\r")
                return prompt
            return Answer(next(menu) if message == "API Explorer" else "Back")

        monkeypatch.setattr(api_explorer.questionary, "select", select)
        result = run("api", "explore")

    assert result.exit_code == 0, result.output
    assert "Action failed" not in result.output
    if destination == "Operations":
        operation_menu.assert_awaited_once()
        assert operation_menu.await_args.args[2].operation_id == "jk_action"
    else:
        assert shown == ["JkModel"]
    assert not transport
