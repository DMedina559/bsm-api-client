# Building the generated client

Install the development extras for both packages from the repository root:

```bash
python -m pip install -e './packages/bsm-api-client[dev]' -e './packages/bsm-cli[dev]'
python tools/export_bsm_openapi.py --output openapi.json
python tools/generate_client.py openapi.json
python -m pytest
```

The backend revision is pinned in both development extras and the publication
workflow. When upgrading it, export and review the bundled schema together with
facade models and integration coverage. CI compares the export to the pinned
contract and tests Python 3.11, 3.12, 3.13 and 3.14.

Generated endpoint/model modules are disposable and untracked. The source
archive carries the schema and generator; build isolation installs the pinned
minor generator series. Wheels contain all generated modules and the operation
registry, while consumers need neither the generator nor the backend package.
Generation validates complete operation coverage before replacing an existing
package and restores the previous package if publication fails.

```bash
python -m build packages/bsm-api-client
python -m build packages/bsm-cli
python tools/check_distributions.py packages/bsm-api-client/dist/*
python -m pip wheel --no-deps --wheel-dir /tmp/bsm-wheels packages/bsm-api-client/dist/*.tar.gz
```

The integration suite starts an isolated BSM process with a temporary database,
uses `bsm-test-utils` archives and binaries, and exercises real HTTP/task/lifecycle
operations without downloading Minecraft. Each server test gets a fresh instance.
World backup/export coverage uses stopped servers because the dummy binary does
not implement the native live save-query protocol.
