"""Documentation normalization preserves executable code and Sphinx fields."""

import ast
import importlib.util
from pathlib import Path


def test_generated_docstring_normalization_is_idempotent_and_preserves_code(tmp_path):
    path = Path(__file__).parents[3] / "scripts/sphinx_docstrings.py"
    spec = importlib.util.spec_from_file_location("sphinx_docstrings", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = tmp_path / "sample.py"
    source.write_text('''def request(name: str) -> str:
    """Call an operation.

    Args:
        name (str): Registered name.
            Kept across wrapped lines.

    Raises:
        ValueError: Invalid name.

    Returns:
        The response value.
    """
    # Preserve this comment.
    return name
''')
    before = ast.parse(source.read_text())
    module.normalize_file(source)
    result = source.read_text()
    assert ":param name: Registered name. Kept across wrapped lines." in result
    assert ":raises ValueError: Invalid name." in result
    assert ":returns: The response value." in result
    assert "# Preserve this comment." in result
    after = ast.parse(result)
    before.body[0].body.pop(0)
    after.body[0].body.pop(0)
    assert ast.dump(before) == ast.dump(after)
    module.normalize_file(source)
    assert source.read_text() == result


def test_sdk_docstrings_use_native_fields():
    root = Path(__file__).parents[1] / "src/bsm_api_client"
    sections = {"Args:", "Arguments:", "Returns:", "Yields:", "Raises:", "Attributes:"}
    for path in root.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(
                node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                doc = ast.get_docstring(node) or ""
                assert not sections.intersection(
                    line.strip() for line in doc.splitlines()
                ), path


def test_developer_examples_match_generated_operations():
    """Guide examples parse and use installed operation IDs and signatures."""
    import inspect
    import json
    import re

    from bsm_api_client.generated.rest import RestClient

    root = Path(__file__).parents[3]
    operations = json.loads(
        (
            root
            / "packages/bsm-api-client/src/bsm_api_client/generated/operations.json"
        ).read_text()
    )
    for path in (root / "docs/source").rglob("*.md"):
        for example in re.findall(r"```python\n(.*?)\n```", path.read_text(), re.S):
            for node in ast.walk(ast.parse(example)):
                if not isinstance(node, ast.Call) or not isinstance(
                    node.func, ast.Attribute
                ):
                    continue
                owner = ast.unparse(node.func.value)
                if owner == "client.rest":
                    method = getattr(RestClient, node.func.attr)
                    inspect.signature(method).bind(
                        None,
                        *[None for _ in node.args],
                        **{keyword.arg: None for keyword in node.keywords},
                    )
                elif owner == "client.discovery" and node.func.attr in {
                    "call",
                    "stream",
                }:
                    assert node.args[0].value in operations, path
