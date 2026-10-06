"""Generate the typed BSM client from a live or saved OpenAPI schema."""

from __future__ import annotations

import argparse
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

        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(package, output)


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
