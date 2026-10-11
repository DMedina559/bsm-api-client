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

        share_canonical_models(package)
        generate_rest_interface(package, registry, schema)
        (package / "__init__.py").write_text(
            '"""Generated BSM REST client."""\n\n'
            "from .client import AuthenticatedClient, Client\n"
            "from .rest import RestClient\n\n"
            '__all__ = ("AuthenticatedClient", "Client", "RestClient")\n'
        )
        publish_package(package, output)


def share_canonical_models(package: Path) -> None:
    """Use one Pydantic contract across generated endpoints and SDK workflows."""
    contracts = ROOT / "packages/bsm-api-client/src/bsm_api_client/contracts.py"
    canonical = {
        node.name
        for node in ast.parse(contracts.read_text()).body
        if isinstance(node, ast.ClassDef)
    }
    for model_file in (package / "models").glob("*.py"):
        model_tree = ast.parse(model_file.read_text())
        classes = [
            node.name for node in model_tree.body if isinstance(node, ast.ClassDef)
        ]
        if len(classes) == 1 and classes[0] in canonical:
            name = classes[0]
            model_file.write_text(
                f'"""Canonical OpenAPI contract; generated import compatibility."""\n\nfrom ...contracts import {name} as {name}\n'
            )

    prune_model_helpers(package)


def prune_model_helpers(package: Path) -> None:  # noqa: C901
    # Schema helpers formerly used inside attrs models are unnecessary once the
    # parent models share Pydantic contracts. Retain only endpoint dependencies.
    required = set()
    for endpoint in (package / "api").rglob("*.py"):
        for node in ast.parse(endpoint.read_text()).body:
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("models.")
            ):
                required.add(node.module.split(".")[1])
    pending = list(required)
    while pending:
        name = pending.pop()
        for node in ast.parse((package / "models" / f"{name}.py").read_text()).body:
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                dependency = node.module.split(".")[0]
                if (
                    package / "models" / f"{dependency}.py"
                ).is_file() and dependency not in required:
                    required.add(dependency)
                    pending.append(dependency)
    exports = ast.parse((package / "models" / "__init__.py").read_text())
    exports.body = [
        node
        for node in exports.body
        if not isinstance(node, ast.ImportFrom) or node.module in required
    ]
    # The generator's original __all__ includes the removed private helpers.
    exports.body = [node for node in exports.body if not isinstance(node, ast.Assign)]
    names = [
        alias.name
        for node in exports.body
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    ]
    exports.body.append(
        ast.Assign(
            targets=[ast.Name(id="__all__", ctx=ast.Store())],
            value=ast.List(elts=[ast.Constant(name) for name in names], ctx=ast.Load()),
        )
    )
    (package / "models" / "__init__.py").write_text(
        ast.unparse(ast.fix_missing_locations(exports)) + "\n"
    )
    for model_file in (package / "models").glob("*.py"):
        if model_file.stem not in required and model_file.name != "__init__.py":
            model_file.unlink()


def generate_rest_interface(
    package: Path, registry: dict[str, str], schema: dict[str, Any]
) -> None:
    """Generate typed operationId methods from the standard endpoint signatures."""
    imports = {
        "from typing import Any, cast",
        "from .types import Response, UNSET, Unset",
    }
    methods = []
    authentication = {
        operation["operationId"]: bool(
            operation.get("security", schema.get("security", []))
        )
        for item in schema["paths"].values()
        for operation in item.values()
        if isinstance(operation, dict) and "operationId" in operation
    }
    for identifier, module_path in sorted(registry.items()):
        module = ast.parse(
            package.joinpath(*module_path.split(".")).with_suffix(".py").read_text()
        )
        for node in module.body:
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("models."):
                    imports.add(
                        ast.unparse(
                            ast.ImportFrom(
                                module=node.module, names=node.names, level=1
                            )
                        )
                    )
                elif node.level == 0 and node.module in {"typing", "datetime", "http"}:
                    imports.add(ast.unparse(node))
        for detailed in (False, True):
            function = next(
                n
                for n in module.body
                if isinstance(n, ast.AsyncFunctionDef)
                and n.name == ("asyncio_detailed" if detailed else "asyncio")
            )
            arguments = function.args
            arguments.args.insert(0, ast.arg(arg="self"))
            kept = [
                (arg, default)
                for arg, default in zip(arguments.kwonlyargs, arguments.kw_defaults)
                if arg.arg != "client"
            ]
            arguments.kwonlyargs = [arg for arg, _ in kept]
            arguments.kw_defaults = [default for _, default in kept]
            names = [arg.arg for arg in arguments.args[1:] + arguments.kwonlyargs]
            parameters = ast.Dict(
                keys=[ast.Constant(name) for name in names if name != "body"],
                values=[
                    ast.Name(id=name, ctx=ast.Load())
                    for name in names
                    if name != "body"
                ],
            )
            call = ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="self", ctx=ast.Load()),
                        attr="_owner",
                        ctx=ast.Load(),
                    ),
                    attr="async_call_generated",
                    ctx=ast.Load(),
                ),
                args=[ast.Constant(identifier)],
                keywords=[
                    ast.keyword(arg="parameters", value=parameters),
                    ast.keyword(
                        arg="body",
                        value=(
                            ast.Name(id="body", ctx=ast.Load())
                            if "body" in names
                            else ast.Constant(None)
                        ),
                    ),
                    ast.keyword(
                        arg="authenticated",
                        value=ast.Constant(authentication[identifier]),
                    ),
                    ast.keyword(
                        arg="detailed" if detailed else "typed",
                        value=ast.Constant(True),
                    ),
                ],
            )
            assert function.returns is not None
            function.name = identifier + ("_detailed" if detailed else "")
            function.body = [
                ast.Expr(value=ast.Constant(f"Generated {identifier} operation.")),
                ast.Return(
                    value=ast.Call(
                        func=ast.Name(id="cast", ctx=ast.Load()),
                        args=[function.returns, ast.Await(value=call)],
                        keywords=[],
                    )
                ),
            ]
            methods.append(function)
    init = ast.parse("def __init__(self, owner: Any):\n    self._owner = owner").body[0]
    cls = ast.ClassDef(
        name="RestClient",
        bases=[],
        keywords=[],
        body=[init, *methods],
        decorator_list=[],
    )
    text = (
        '"""Typed REST interface generated from the bundled OpenAPI contract."""\n\n'
        + "\n".join(sorted(imports))
        + "\n\n"
        + ast.unparse(ast.fix_missing_locations(cls))
        + "\n"
    )
    (package / "rest.py").write_text(text)


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
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify committed generation without modifying files.",
    )
    args = parser.parse_args()
    schema = load_schema(args.source)
    if not args.check:
        generate(schema, args.output)
        return
    with tempfile.TemporaryDirectory(prefix="bsm-generation-check-") as directory:
        fresh = Path(directory) / "generated"
        generate(schema, fresh)

        def snapshot(path):
            return {
                str(file.relative_to(path)): file.read_bytes()
                for file in path.rglob("*")
                if file.is_file()
                and "__pycache__" not in file.parts
                and file.suffix != ".pyc"
            }

        if snapshot(fresh) != snapshot(args.output):
            raise SystemExit(
                "Generated REST client drift. Regenerate and review the changes."
            )


if __name__ == "__main__":
    main()
