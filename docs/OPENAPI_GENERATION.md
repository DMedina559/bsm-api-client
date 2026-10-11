# Building the generated client

Install the development extras for both packages from the repository root:

```bash
python -m pip install -e './packages/bsm-api-client[dev]' -e './packages/bsm-cli[dev]'
python tools/export_bsm_openapi.py --output openapi.json
python tools/generate_client.py openapi.json
python -m pytest
```

The backend `dev` branch is the source contract. Export and review its schema,
then regenerate both public contracts and REST operations:

```bash
python tools/generate_models.py
python tools/generate_client.py packages/bsm-api-client/src/bsm_api_client/generated/openapi.json
python tools/generate_models.py --check
python tools/generate_client.py packages/bsm-api-client/src/bsm_api_client/generated/openapi.json --check
```

Generated code is committed and reviewed alongside the schema. Installation and
packaging never run a generator or mutate source files. Wheels and source archives
contain the same generated endpoints, Pydantic model imports, typed `RestClient`,
and operation registry. The pinned `openapi-python-client` release generates the
endpoint serialization; the shared Pydantic contracts supply request validation
and response parsing. Python 3.11–3.14 are supported; CI verifies regeneration
and builds on the range's Python 3.11 and 3.14 endpoints.
Generation validates complete operation coverage before replacing an existing
package and restores the previous package if replacement fails.

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
