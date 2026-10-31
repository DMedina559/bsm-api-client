<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/DMedina559/bsm-frontend/main/frontend/public/image/icon/web-app-manifest-512x512.png" alt="BSM Logo" width="150">
</div>

# bsm-api-client

<p align="center">
  <a href="https://github.com/DMedina559/bsm-api-client/releases">
    <img alt="Stable" src="https://img.shields.io/github/v/release/DMedina559/bsm-api-client?label=Stable&color=blue">
  </a>
  <a href="https://github.com/DMedina559/bsm-api-client/releases">
    <img alt="Pre-Release" src="https://img.shields.io/github/v/release/DMedina559/bsm-api-client?include_prereleases&label=Pre-Release&color=red">
  </a>
  <a href="https://github.com/DMedina559/bsm-api-client/actions">
    <img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/DMedina559/bsm-api-client/build-test.yml?label=Tests&event=push">
  </a>
</p>

## Introduction

This repository is a monorepo containing the following Python packages for interacting with the Bedrock Server Manager API:

*   [`bsm-api-client`](packages/bsm-api-client/README.md): An asynchronous Python client library.
*   [`bsm-cli`](packages/bsm-cli/README.md): A command-line interface tool for managing servers via the API.

## Installation

Install the library using pip:

```bash
pip install bsm-api-client
```

Or if you wish to use the Command Line Interface CLI:

```bash
pip install bsm-cli
```

## OpenAPI contract

In a separate contract-tooling environment, install `bedrock-server-manager` from the target backend checkout. Export with `python scripts/export_bsm_openapi.py --output packages/bsm-api-client/src/bsm_api_client/generated/openapi.json`, then run `python scripts/generate_models.py` and `python scripts/generate_client.py packages/bsm-api-client/src/bsm_api_client/generated/openapi.json`. CI tests against backend `dev`. The separate Lint and Types workflow checks generated clients and models against the bundled document. Review and regenerate the contract when adopting backend API changes.


### Event diagnostics and web runtime

The regenerated contract includes event catalog/activity and web runtime control
from backend `dev`. Administrators can use `client.events.async_list_application_events()`,
`client.events.async_get_event_activity(limit=20)`, and
`client.application.async_get_web_runtime()`. All four operations also have typed
`client.rest` operation-ID methods. `async_shutdown_web_runtime()` submits `{}` and
returns an HTTP 202 receipt; it confirms acceptance, not completed cleanup.

CLI equivalents are `events catalog`, `events activity`,
`runtime`, and `shutdown --yes`. Shutdown uses administrator
credentials, not the private local-host control token. Event payloads remain
separate from metadata-only diagnostics. Custom event emission must follow the
backend's declared-event and ownership rules.

## Operation access metadata

Discovered operations preserve standard OpenAPI `security` alternatives and
versioned BSM access metadata in `ApiOperation.access`. Metadata absent from older
servers is labeled `unknown`. `accessible_with(permissions)` returns a static
boolean for simple permission policies and `None` for contextual or unknown
policies. The backend remains authoritative for ownership, custom rules, and 403
responses.

`bsm-cli api operations` includes access metadata. Add `--accessible` to list
operations statically permitted by the current account's discovered permissions;
contextual and unknown policies are omitted from that filter. Without the filter,
unavailable operations remain inspectable. Account permissions are resolved from
current roles; endpoint scopes do not narrow an individual JWT. CLI and integration
credentials remain bearer tokens.


## Named credentials and server assignments

New backends expose credential operations through the generated operation API:
`create_integration_token`, `list_integration_tokens`, and
`revoke_integration_token`. A created secret is returned once; lists contain
metadata only. Use the secret as the client's existing bearer `token`. Expired or
revoked integration credentials raise authentication errors without silently
falling back to a configured username/password. Logging out clears the local
credential; revoke it explicitly to disable it elsewhere.

```sh
bsm-cli access servers
bsm-cli auth tokens create --name "Home Assistant" --expires-days 30
bsm-cli auth tokens list
bsm-cli auth tokens revoke TOKEN_ID
bsm-cli access show USER_ID
bsm-cli access set USER_ID --mode assigned --grant SERVER_ID=servers:read,servers:control
```

The create command prints the one-time secret and never saves it as your login
credential. Repeat `--permission` and `--server-id` to narrow a credential.
Assignments replace the account's grant set and require an administrator.
Server identifiers are immutable; account roles remain the upper capability
limit. `ApiOperation.accessible_with()` returns unknown for resource-scoped
operations because capability membership alone cannot establish resource access.

## Sessions and MFA

Interactive logins are tracked sessions. `auth logout` revokes the current session
on the server and clears local credentials even when that request fails. Revoked
sessions require explicit login; saved passwords are not silently retried. Bearer
login does not create cookies. Older untracked JWTs require a new login after
upgrading the backend.

```sh
bsm-cli auth login --mfa
bsm-cli auth sessions list
bsm-cli auth sessions revoke SESSION_ID
bsm-cli auth sessions revoke-all
bsm-cli auth verify --mfa
bsm-cli auth activity
bsm-cli auth mfa status
bsm-cli auth mfa enroll
bsm-cli auth mfa confirm
bsm-cli auth tokens rotate TOKEN_ID
bsm-cli access sessions USER_ID
bsm-cli access signout USER_ID --all
```

Use an authenticator or one-use recovery code when prompted. MFA enrollment and
recovery commands print secrets once; save them securely. The SDK accepts a
one-use `otp=` argument for password authentication. Sensitive operations require
recent password/factor verification; refresh does not extend that verification.
Integration credentials remain independent from login-session revocation.

Use `bsm-cli auth tokens create --name "Home Assistant" --never-expire` for an
integration credential without a deadline. The API represents this as
`expires_in_days: null`, with `expires_at: null` in metadata. Omitting the option
retains the 30-day default. Rotation preserves the original expiry choice, and
revocation/account access checks still apply. Login-session expiry is unchanged.
