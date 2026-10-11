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
parameters fail before invoking an endpoint. Cookie parameters are not currently supported by the generic CLI. Query arrays and objects honor form `explode`, deepObject, spaceDelimited and pipeDelimited serialization.

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

For Python client examples and OpenAPI discovery, see the
[API usage guide](../../docs/API_DOCS.md).


## Content and task behavior

`world install --file`, `addon install --file`, and `backup restore --file` select
files already present on the backend. They do not upload a local file. Examples:

```bash
bsm-cli world install --server survival --file MyWorld.mcworld --yes
bsm-cli addon install --server survival --file Example.mcaddon
bsm-cli backup restore --server survival --file MyWorld_backup_20261007_120000.mcworld
bsm-cli backup restore --server survival --file custom-backup.zip --type world
```

`content upload LOCAL_FILE` works only when the server advertises an
`upload_content` operation. The current backend does not advertise one.
Place content files in the backend's content directories, then select them by name.

Background commands subscribe to the task's WebSocket topic and check its REST
snapshot after subscribing, covering tasks that finish before monitoring starts.
A silent or disconnected WebSocket falls back to REST polling. Failed and
cancelled tasks exit with a nonzero status.

Registry menus accept a single value or a JSON array for repeated options and
variadic arguments, preserving spaces in player names and paths. Password inputs
are hidden and password confirmations are checked.

## Contract review and streaming downloads

```bash
bsm-cli api operations --method GET --plugin example
bsm-cli --json api diff --against saved-openapi.json --details
bsm-cli api download example_download ./archive.zip --param name=example
```

`api download` streams a discovered GET operation and replaces the destination
only after a complete download. JSON mode returns the output path and byte count.
`api diff --details` includes conservative compatibility classifications alongside
the usual added/removed/changed lists. Invalid saved schemas produce input errors.

Completion validates cached contracts and fingerprints and rejects metadata for a
different backend URL or recorded user. Malformed caches yield no suggestions.
Boolean and enum parameter values have completion suggestions. Interactive command
menus can select live operation IDs and return to the menu after each action.


## Manager dashboard and settings

The home menu opens Overview, Monitor, and Operations directly. Select a server
to see its lifecycle, configuration, backup, and world actions on one screen.
Menus with a list display it automatically before offering actions. Operations
can be selected directly to inspect their outcomes.

These views are also available without entering the menu:

```bash
bsm-cli auth setup --base-url http://localhost:11325
bsm-cli overview
bsm-cli health
bsm-cli monitor
bsm-cli monitor --once --unit GB
bsm-cli operations list
bsm-cli operations show TASK_ID
bsm-cli audit
bsm-cli logs --topic app_logs
```

Application commands use their direct paths (`overview`, `monitor`, `settings`,
`health`, `logs`, `audit`, and `operations`). Server monitoring and settings live
under `server`; the duplicate `manager` and `system` groups have been removed.
Use `bsm-cli server monitor --server survival` for a single server.

Live views reconnect automatically and reconcile WebSocket updates with HTTP
snapshots. Revision checks prevent older snapshots from replacing newer state.
Application monitoring separates app and system metrics and shows recent CPU
history. Log history returns a cursor for requesting older pages.

```bash
bsm-cli settings
bsm-cli server settings --server survival
bsm-cli plugin settings edit backup_on_start
bsm-cli plugin settings show backup_on_start
bsm-cli plugin settings set backup_on_start settings.json
bsm-cli appearance set --memory-unit GB --density compact
```

The shared settings editor reviews changes before saving. Plugin schemas provide
field descriptions, bounds, enums, and server checklists; plugins without settings
have no Settings action. Credential fields are masked. Application and server
settings infer field types from their current values because those endpoints do
not advertise an editable settings schema. Backend validation remains authoritative.

An editor refuses to save if its settings changed in another session. Global and
server settings are saved one key at a time; the CLI prints each successfully saved
key so partial updates remain visible if a later request fails. Plugins use one
request to replace their settings. `--json` continues to return structured API data
for noninteractive commands; use `plugin settings set` for scripted updates.
