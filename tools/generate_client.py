"""Generate the typed BSM client from a live or saved OpenAPI schema."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "packages" / "bsm-api-client" / "src" / "bsm_api_client" / "generated"
)


def load_schema(source: str) -> dict[str, Any]:
    """Load OpenAPI JSON from a URL or local file."""
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source) as response:  # noqa: S310
            return cast(dict[str, Any], json.load(response))
    with Path(source).open(encoding="utf-8") as handle:
        return cast(dict[str, Any], json.load(handle))


def generate(schema: dict[str, Any], output: Path) -> None:
    """Run openapi-python-client into the package's generated namespace."""
    with tempfile.TemporaryDirectory(prefix="bsm-openapi-") as tmp:
        tmp_path = Path(tmp)
        schema_path = tmp_path / "openapi.json"
        config_path = tmp_path / "config.json"
        generated_root = tmp_path / "client"
        schema_path.write_text(
            json.dumps(schema, indent=2, sort_keys=True), encoding="utf-8"
        )
        config_path.write_text(
            json.dumps(
                {
                    "package_name_override": "generated",
                    "project_name_override": "bsm-api-client-generated",
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(
            [
                sys.executable,
                "-m",
                "openapi_python_client",
                "generate",
                "--path",
                str(schema_path),
                "--config",
                str(config_path),
                "--output-path",
                str(generated_root),
                "--overwrite",
            ],
            check=True,
        )
        package = generated_root / "generated"
        if not package.is_dir():
            raise RuntimeError(
                "openapi-python-client did not create the expected package"
            )
        import shutil

        shutil.copyfile(schema_path, package / "openapi.json")
        registry = {}
        for module in package.glob("api/*/*.py"):
            if module.name == "__init__.py":
                continue
            tree = ast.parse(module.read_text(encoding="utf-8"))
            builder = next(
                (
                    node
                    for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "_get_kwargs"
                ),
                None,
            )
            if builder is None:
                raise RuntimeError(f"Generated module lacks _get_kwargs: {module}")
            for node in ast.walk(builder):
                if not isinstance(node, ast.Dict):
                    continue
                entries = {
                    key.value: value
                    for key, value in zip(node.keys, node.values)
                    if isinstance(key, ast.Constant)
                }
                if "method" not in entries or "url" not in entries:
                    continue
                method = ast.literal_eval(entries["method"])
                url = entries["url"]
                path = ast.literal_eval(
                    url.func.value
                    if isinstance(url, ast.Call) and isinstance(url.func, ast.Attribute)
                    else url
                )
                operation_id = schema["paths"][path][method]["operationId"]
                if operation_id in registry:
                    raise RuntimeError(
                        f"Duplicate generated operationId {operation_id!r}: {module}"
                    )
                registry[operation_id] = ".".join(
                    module.relative_to(package).with_suffix("").parts
                )
        expected = {
            details["operationId"]
            for item in schema["paths"].values()
            for method, details in item.items()
            if method
            in {"get", "post", "put", "delete", "patch", "head", "options", "trace"}
            and "operationId" in details
        }
        if expected != registry.keys():
            raise RuntimeError(
                "Generator operation mismatch: "
                f"missing={sorted(expected - registry.keys())}, "
                f"unexpected={sorted(registry.keys() - expected)}"
            )
        (package / "operations.json").write_text(
            json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        publish_package(package, output)


def publish_package(package: Path, output: Path) -> None:
    """Replace a validated package, restoring the old package on failure."""
    import shutil

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".bsm-generated-", dir=output.parent
    ) as staging:
        replacement = Path(staging) / "generated"
        backup = Path(staging) / "previous"
        shutil.copytree(package, replacement)
        if output.exists():
            output.rename(backup)
        try:
            replacement.rename(output)
        except BaseException:
            if backup.exists():
                backup.rename(output)
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        help="OpenAPI JSON file or URL (normally http://HOST:PORT/api/openapi.json)",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    generate(load_schema(args.source), args.output)


if __name__ == "__main__":
    main()
