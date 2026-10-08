"""Generated package coverage and failure-safe replacement."""

import importlib.util
import json
from pathlib import Path

import pytest

from bsm_api_client.generated_adapter import operation_module
from bsm_api_client.openapi import generated_schema, index_operations

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "generate_client", ROOT / "tools/generate_client.py"
)
assert SPEC is not None and SPEC.loader is not None
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


def test_every_shipped_operation_is_importable():
    for operation_id in index_operations(generated_schema()):
        assert callable(operation_module(operation_id).asyncio_detailed)


def test_omitted_operations_preserve_existing_package(tmp_path, monkeypatch):
    output = tmp_path / "generated"
    output.mkdir()
    sentinel = output / "previous.txt"
    sentinel.write_text("working client")

    def incomplete_generation(command, **kwargs):
        package = Path(command[command.index("--output-path") + 1]) / "generated"
        package.mkdir(parents=True)

    monkeypatch.setattr(generator.subprocess, "run", incomplete_generation)
    schema = {"paths": {"/missing": {"get": {"operationId": "missing"}}}}
    with pytest.raises(RuntimeError, match="omitted operations"):
        generator.generate(schema, output)
    assert sentinel.read_text() == "working client"
    assert not (output / "operations.json").exists()


def test_failed_publication_restores_existing_package(tmp_path, monkeypatch):
    output = tmp_path / "generated"
    output.mkdir()
    (output / "previous.txt").write_text("working client")
    package = tmp_path / "replacement"
    package.mkdir()
    (package / "operations.json").write_text(json.dumps({}))
    rename = Path.rename

    def fail_replacement(path, target):
        if path.name == "generated" and path.parent.name.startswith(".bsm-generated-"):
            raise OSError("replacement failed")
        return rename(path, target)

    monkeypatch.setattr(Path, "rename", fail_replacement)
    with pytest.raises(OSError, match="replacement failed"):
        generator.publish_package(package, output)
    assert (output / "previous.txt").read_text() == "working client"


@pytest.mark.parametrize("phrase", ["Unprocessable Entity", "Unprocessable Content"])
def test_export_normalizes_python_http_status_descriptions(phrase):
    spec = importlib.util.spec_from_file_location(
        "export_bsm_openapi", ROOT / "tools/export_bsm_openapi.py"
    )
    assert spec is not None and spec.loader is not None
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    schema = {
        "paths": {
            "/test": {
                "parameters": [],
                "get": {
                    "responses": {
                        "422": {"description": phrase},
                        "200": {"description": "OK"},
                    }
                },
                "post": {
                    "responses": {"422": {"description": "Custom validation message"}}
                },
            }
        }
    }
    normalized = exporter.normalize_response_descriptions(schema)
    assert (
        normalized["paths"]["/test"]["get"]["responses"]["422"]["description"]
        == "Unprocessable Entity"
    )
    assert (
        normalized["paths"]["/test"]["get"]["responses"]["200"]["description"] == "OK"
    )
    assert (
        normalized["paths"]["/test"]["post"]["responses"]["422"]["description"]
        == "Custom validation message"
    )


@pytest.mark.asyncio
async def test_generated_adapter_typed_mode_preserves_parsed_model(monkeypatch):
    from types import SimpleNamespace
    from unittest.mock import AsyncMock

    from bsm_api_client import generated_adapter

    parsed = object()
    response = SimpleNamespace(parsed=parsed, content=b'{"status":"ok"}')
    module = SimpleNamespace(asyncio_detailed=AsyncMock(return_value=response))
    monkeypatch.setattr(generated_adapter, "operation_module", lambda _: module)
    import bsm_api_client.generated as generated

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        def set_async_httpx_client(self, transport):
            return self

    monkeypatch.setattr(generated, "Client", FakeClient)
    owner = SimpleNamespace(_server_root_url="http://localhost")
    assert await generated_adapter.call_generated(owner, "test", typed=True) is parsed
    assert await generated_adapter.call_generated(owner, "test") == {"status": "ok"}
    with pytest.raises(generated_adapter.InvalidInputError):
        await generated_adapter.call_generated(owner, "test", typed=True, detailed=True)
