"""Check that wheels and source distributions ship every generated operation."""

from __future__ import annotations

import argparse
import json
import tarfile
import zipfile
from pathlib import Path


def check(path: Path) -> None:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            contents = {
                name: archive.read(name)
                for name in archive.namelist()
                if not name.endswith("/")
            }
        root = "bsm_api_client/generated/"
    else:
        with tarfile.open(path) as archive:
            contents = {}
            for member in archive.getmembers():
                if member.isfile():
                    handle = archive.extractfile(member)
                    if handle is None:
                        raise RuntimeError(f"{path}: cannot read {member.name}")
                    with handle:
                        contents[member.name] = handle.read()
        roots = {
            name.removesuffix("operations.json")
            for name in contents
            if name.endswith("/bsm_api_client/generated/operations.json")
        }
        if len(roots) != 1:
            raise RuntimeError(f"{path}: missing generated operation registry")
        root = roots.pop()
    registry = json.loads(contents[root + "operations.json"])
    schema = json.loads(contents[root + "openapi.json"])
    expected = {
        details["operationId"]
        for item in schema["paths"].values()
        for method, details in item.items()
        if method
        in {"get", "post", "put", "delete", "patch", "head", "options", "trace"}
    }
    if set(registry) != expected:
        raise RuntimeError(f"{path}: generated registry does not cover the schema")
    for module in registry.values():
        name = root + module.replace(".", "/") + ".py"
        if name not in contents:
            raise RuntimeError(f"{path}: missing generated endpoint {name}")
    if root + "client.py" not in contents:
        raise RuntimeError(f"{path}: missing generated HTTP client")
    print(f"{path.name}: {len(registry)} generated operations packaged")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("distributions", nargs="+", type=Path)
    for path in parser.parse_args().distributions:
        check(path)


if __name__ == "__main__":
    main()
