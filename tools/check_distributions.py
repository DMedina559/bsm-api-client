"""Verify generated wheels and clean, self-contained source distributions."""

from __future__ import annotations

import argparse
import json
import tarfile
import zipfile
from pathlib import Path

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options", "trace"}


def archive_contents(path: Path) -> dict[str, bytes]:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            return {
                name: archive.read(name)
                for name in archive.namelist()
                if not name.endswith("/")
            }
    with tarfile.open(path) as archive:
        result = {}
        for member in archive.getmembers():
            if member.isfile():
                handle = archive.extractfile(member)
                if handle is None:
                    raise RuntimeError(f"{path}: cannot read {member.name}")
                with handle:
                    result[member.name] = handle.read()
        return result


def check_sdist(path: Path, contents: dict[str, bytes]) -> None:
    roots = {
        name.removesuffix("openapi.json")
        for name in contents
        if name.endswith("/bsm_api_client/generated/openapi.json")
    }
    if len(roots) != 1:
        raise RuntimeError(f"{path}: missing bundled OpenAPI schema")
    root = roots.pop()
    if not any(name.endswith("/generate_client.py") for name in contents):
        raise RuntimeError(f"{path}: missing build-time generator")
    unexpected = [
        name
        for name in contents
        if name.startswith(root)
        and name != root + "__init__.py"
        and name != root + "openapi.json"
    ]
    if unexpected:
        raise RuntimeError(
            f"{path}: generated artifacts leaked into source archive: {unexpected}"
        )
    print(f"{path.name}: source schema and build generator packaged")


def check_wheel(path: Path, contents: dict[str, bytes]) -> None:
    root = "bsm_api_client/generated/"
    registry = json.loads(contents[root + "operations.json"])
    schema = json.loads(contents[root + "openapi.json"])
    expected = {
        details["operationId"]
        for item in schema["paths"].values()
        for method, details in item.items()
        if method in HTTP_METHODS
    }
    if set(registry) != expected:
        raise RuntimeError(f"{path}: generated registry does not cover the schema")
    for module in registry.values():
        name = root + module.replace(".", "/") + ".py"
        if name not in contents:
            raise RuntimeError(f"{path}: missing generated endpoint {name}")
    if root + "client.py" not in contents:
        raise RuntimeError(f"{path}: missing generated HTTP client")
    if not any(
        name.startswith(root + "models/") and name.endswith(".py")
        for name in contents
    ):
        raise RuntimeError(f"{path}: missing generated models")
    print(f"{path.name}: {len(registry)} generated operations packaged")


def check(path: Path) -> None:
    contents = archive_contents(path)
    if path.suffix == ".whl":
        check_wheel(path, contents)
    else:
        check_sdist(path, contents)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("distributions", nargs="+", type=Path)
    for path in parser.parse_args().distributions:
        check(path)


if __name__ == "__main__":
    main()
