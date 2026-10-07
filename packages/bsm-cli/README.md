<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/DMedina559/bsm-frontend/main/frontend/public/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# bsm-cli

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

`bsm-cli` is a command-line interface tool for managing Minecraft Bedrock Dedicated Servers via the Bedrock Server Manager API.

## Features

*   Full CLI interface using `click` and `questionary`.
*   Interactive menus for server management.
*   Realtime server state updates via WebSocket.
*   Seamlessly manages configuration for server and backups.

## Installation

Install the library using pip:

```bash
pip install bsm-cli
```

## Quick Start

You can invoke the CLI using:

```bash
bsm-cli
```

Which will trigger the interactive menu allowing you to manage and configure your Bedrock Dedicated Servers.

## OpenAPI commands

The CLI targets BSM's typed-contract branch and stable operation IDs. Curated commands remain available;
new server/plugin HTTP endpoints can be inspected and called immediately:

```bash
bsm-cli api info
bsm-cli api schema
bsm-cli api operations --tag 'Server Management'
bsm-cli api operation start_server
bsm-cli api call start_server --param server_name=survival
bsm-cli api diff --against-generated
bsm-cli api diff --against saved-openapi.json
bsm-cli api refresh
bsm-cli api export saved-openapi.json
bsm-cli plugin operations discord
bsm-cli plugin call discord discord_status
```

`--param NAME=VALUE` uses declared path/query/header parameter types. Boolean values
use `true`/`false`; arrays and objects use JSON. Missing, duplicate, and unknown
parameters fail before invoking an endpoint. Cookie parameters and non-form query serialization styles are not currently
supported by the generic CLI. Query arrays and objects honor the form `explode` setting.

Request-body options:

```bash
bsm-cli api call send_command --param server_name=survival --json '{"command":"list"}'
bsm-cli api call login --form username=admin --form password=example
bsm-cli api call plugin_upload --file file=./addon.mcaddon
```

The global `--json` flag precedes the command; the call-specific `--json` option
is a request body and follows the operation:

```bash
bsm-cli --json api call send_command --param server_name=survival --json '{"command":"list"}'
bsm-cli --json server list
```

JSON output contains structured API responses, without human progress/table text.
Commands making multiple calls return an ordered array of responses unless they
provide their own result. Errors are JSON objects on stderr. Resource monitoring
returns one snapshot in JSON mode; `server list --loop` requires human output.
Interactive commands may still prompt; supply their options for scripting.

| Exit status | Meaning |
| --- | --- |
| 0 | Success |
| 1 | API/server or unexpected failure |
| 2 | Usage or input validation |
| 3 | Authentication/authorization |
| 4 | Connection failure |
| 5 | Missing resource/operation |

Human discovery output uses tables. Interactive menus browse Click's registered
command groups and add a Plugin API menu only when the live schema has plugin
operations. `api refresh` caches operation/plugin/parameter completion; on servers
advertising `list_servers`, it also caches server-name completion. Completion does
not make network requests and ignores caches belonging to another configured URL.

Enable Click shell completion, for example in Bash:

```bash
eval "$(_BSM_CLI_COMPLETE=bash_source bsm-cli)"
```

See [generation](../../docs/OPENAPI_GENERATION.md) and
[the API contract](../../docs/OPENAPI_CONTRACT.md).
