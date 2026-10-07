# API client and CLI audit

This change targets `bedrock-server-manager` branch
`refactor!/move-api-to-pydantic` at
`833eb28fde7b5a43140933405aa5fb0f4700eddd`.

## Findings and fixes

- **Fresh installs cannot log in.** Standard facade methods require generated
  endpoint modules, but Git excluded them. The checkout now contains all 77
  generated operations, their models, operation registry, and schema. Users do
  not need the backend or generator installed to use either package.
- **Generation can destroy a working client.** Validation now happens in the
  temporary generated package. Publication stages the replacement beside its
  destination and restores the previous package if replacement fails.
- **Backend pins have drifted.** Both development extras, release generation,
  and the documented contract now target the requested branch's current commit.
- **Failed login can pair a new server with an old token.** The CLI now saves the
  destination, SSL choice, and token together after successful authentication.
  Successful login clears old username/password and completion caches. Both
  interactive login paths share one implementation, including password-only
  input, which now prompts for the missing username.
- **Logout can automatically authenticate again.** Logout now clears stored
  username/password as well as the JWT.
- **IPv6 WebSocket URLs lose their brackets.** WebSocket construction now keeps
  the parsed URL authority. Unsupported URL schemes fail before a session is
  created.
- **Redundant discovery helpers and unused backup constants.** Removed private
  duplicates of operation-ID/plugin parsing and unused validation constants.
- **Pruning integration test assumes downloaded assets.** The test now creates
  its empty cache directory explicitly rather than depending on another test.

## Contract and packaging verification

All facade-generated operation calls were compared to the actual generated
endpoint signatures: operation IDs, required parameters, and bodies match.
Compatibility models retain the backend's response fields; the shared action
model intentionally retains extra legacy fields. Runtime discovery, error
mapping, auth refresh, binary responses, DELETE bodies, multipart requests,
WebSocket behavior, and CLI JSON output are covered by the unit suite.

CI now tests the shipped client before regenerating it, checks built wheel and
source-distribution registries/endpoints, and rejects regeneration drift.
Generated files are excluded from handwritten-code formatting/type hooks.
Release builds also check generated package contents before publishing.

Validation in this environment:

- 129 unit tests passed; one existing optional test skipped.
- 11 live backend tests passed for login, invalid credentials, account, manager
  settings/info, players, pruning, and plugin management.
- The reported interactive CLI login passed against the real backend.
- Both packages built as wheels and source distributions. API archives contain
  all 77 operations; separately installed wheels import every operation outside
  the source checkout. Regeneration produces no changes.
- Flake8 and mypy passed for the handwritten packages and changed tooling/tests.

## Remaining verification and backend constraints

Bedrock installation/lifecycle/world/addon integration tests require external
assets. The attempted installation failed because the backend connectivity
probe at `http://clients3.google.com/generate_204` could not resolve in this
restricted environment. Those operations have unit/contract coverage but their
live lifecycle behavior was not verified here. Run the complete `python -m
pytest` suite in an environment with those downloads available.

The backend advertises no core content-upload operation. The existing client
reports `NotFoundError` when it is absent; implementing core uploads requires a
backend route. Existing plugin upload routes remain callable through discovery.
The backend also uses the `Server Mannagement` tag for some routes; generated
module paths preserve that spelling to remain faithful to its schema.

## Install from this checkout (PowerShell)

```powershell
python -m pip install -e .\packages\bsm-api-client -e .\packages\bsm-cli
bsm-cli auth login
```

Run these commands from the repository root in the intended environment.
There is no generation prerequisite for login.
