"""Generate public Pydantic contracts from the bundled OpenAPI document."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "packages/bsm-api-client/src/bsm_api_client/generated/openapi.json"
OUTPUT = ROOT / "packages/bsm-api-client/src/bsm_api_client/contracts.py"


def generate(source: Path) -> str:  # noqa: C901
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "models.py"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "datamodel_code_generator",
                "--input",
                str(source),
                "--input-file-type",
                "openapi",
                "--output",
                str(output),
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--enum-field-as-literal",
                "all",
                "--field-constraints",
                "--use-union-operator",
                "--target-python-version",
                "3.11",
                "--disable-timestamp",
                "--use-standard-collections",
                "--collapse-root-models",
                "--base-class",
                "bsm_api_client.contract_base.ContractModel",
            ],
            check=True,
        )
        tree = ast.parse(output.read_text())
        schemas = json.loads(source.read_text())["components"]["schemas"]
        for cls in tree.body:
            if not isinstance(cls, ast.ClassDef) or cls.name not in schemas:
                continue
            for field in cls.body:
                if isinstance(field, ast.AnnAssign) and isinstance(
                    field.target, ast.Name
                ):
                    spec = (
                        schemas[cls.name].get("properties", {}).get(field.target.id, {})
                    )
                    if "#/components/schemas/JsonValue" in json.dumps(spec):

                        class JsonTypes(ast.NodeTransformer):
                            def visit_Name(self, node):
                                return (
                                    ast.copy_location(
                                        ast.Name(id="JsonValue", ctx=node.ctx), node
                                    )
                                    if node.id == "Any"
                                    else node
                                )

                        field.annotation = JsonTypes().visit(field.annotation)
        roots: list[ast.stmt] = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and any(
                isinstance(base, ast.Subscript)
                and isinstance(base.value, ast.Name)
                and base.value.id == "RootModel"
                for base in node.bases
            ):
                root = next(
                    field
                    for field in node.body
                    if isinstance(field, ast.AnnAssign)
                    and isinstance(field.target, ast.Name)
                    and field.target.id == "root"
                )
                annotation = root.annotation
                if isinstance(root.value, ast.Call):
                    metadata = ast.Call(
                        func=ast.Name(id="Field", ctx=ast.Load()),
                        args=[],
                        keywords=[k for k in root.value.keywords if k.arg != "default"],
                    )
                    annotation = ast.Subscript(
                        value=ast.Name(id="Annotated", ctx=ast.Load()),
                        slice=ast.Tuple(elts=[annotation, metadata], ctx=ast.Load()),
                        ctx=ast.Load(),
                    )
                roots.append(
                    ast.Assign(
                        targets=[ast.Name(id=node.name, ctx=ast.Store())],
                        value=annotation,
                    )
                )
            else:
                roots.append(node)
        tree.body = roots
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "pydantic":
                node.names = [item for item in node.names if item.name != "RootModel"]
        tree.body.insert(
            1,
            ast.ImportFrom(
                module="typing", names=[ast.alias(name="Annotated")], level=0
            ),
        )
        tree.body.insert(
            1,
            ast.ImportFrom(
                module="pydantic", names=[ast.alias(name="JsonValue")], level=0
            ),
        )
        return (
            "# Generated from bundled OpenAPI by tools/generate_models.py.\n"
            + ast.unparse(ast.fix_missing_locations(tree))
            + "\n"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = generate(args.source)
    # Use the repository formatter so CI compares exactly what contributors commit.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "contracts.py"
        path.write_text(value)
        subprocess.run(
            [sys.executable, "-m", "isort", "--settings-path", str(ROOT), str(path)],
            check=True,
        )
        subprocess.run(
            [sys.executable, "-m", "black", "--target-version", "py311", str(path)],
            check=True,
        )
        value = path.read_text()
    if args.check:
        if OUTPUT.read_text() != value:
            raise SystemExit(
                "Public contracts drift. Run python tools/generate_models.py"
            )
    else:
        OUTPUT.write_text(value)


if __name__ == "__main__":
    main()
