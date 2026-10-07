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
