<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/DMedina559/bsm-frontend/main/frontend/public/image/icon/web-app-manifest-512x512.png" alt="BSM Logo" width="150">
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

Overview, monitoring, and operation lists use structured terminal tables. In an
interactive menu, Ctrl+C stops the active live view and returns to its menu;
standalone live commands still exit normally on Ctrl+C.

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

Use `bsm-cli auth login --remember-me` to request the backend-configured longer
token lifetime. Interactive login also offers this choice, defaulting to off.
The CLI saves the issued token without storing your password; the flag cannot
extend the lifetime of an existing token supplied with `--token`.


## Administrative diagnostics

```bash
bsm-cli diagnostics snapshot
bsm-cli diagnostics snapshot --subsystem runtime
bsm-cli diagnostics history --outcome failed --limit 50
bsm-cli diagnostics history --cursor RETURNED_CURSOR
bsm-cli diagnostics runs
bsm-cli diagnostics trace CORRELATION_ID
bsm-cli --json diagnostics snapshot > before.json
bsm-cli --json diagnostics snapshot > after.json
bsm-cli diagnostics compare before.json after.json
```

History supports subsystem, instance, owner, code, outcome, operation and correlation filters. Trace sources may be independently unavailable. Comparison accepts snapshots or the `snapshot` member of saved support reports; counter deltas are unavailable across instance changes. All commands support the existing `--json` output and administrator error policy. Requests are on demand; no new background polling is added.

### Support reports

On a backend with diagnostic endpoints, an administrator can save a sanitized report:

```console
bsm-cli diagnostics report --output bsm-support-report.json
```

The command discovers the live `get_diagnostic_report` operation and uses your configured authentication. The destination is published only after the response completes. Use `--force` to replace an existing file. Reports contain subsystem metadata and bounded history; inspect them before sharing. Older backends report that the operation is unavailable.

### Portable backups

```console
bsm-cli backup create --server MyServer
bsm-cli backup create --server MyServer --encrypted
bsm-cli backup list --server MyServer
bsm-cli backup inspect --server MyServer --file ARCHIVE.bsmbackup
bsm-cli backup restore --server MyServer --file ARCHIVE.bsmbackup --component world --component server.properties
```

Restore inspects the manifest, offers complete components, prints a destination review, and requests confirmation. Use `--unlock` to prompt privately for an imported backup's recovery key. Use `--no-restart` to leave an originally running server stopped. `--yes` explicitly confirms a noninteractive reviewed restore. Old `--type` backup creation and filename-based restore inference have been replaced by unified archives and component selection.

Offline extraction is provided by the backend package's `bedrock-server-manager backup extract` command and requires no running instance or original database.

Use `backup create --packs` or `--no-packs` to override server-level pack inclusion for one capture. Leaving both unset uses the configured default. Pack directories remain optional components within manifest version 1.

Additional backup commands:

- `backup dry-run --server SERVER --file ID --component world`: stage and verify selected files without stopping Minecraft or replacing live files; report required space per volume.
- `backup annotate --server SERVER --file ID --label "Before update" --notes "Known good"`: edit local catalog metadata without rewriting the archive.
- `backup list --server SERVER --kind scheduled --search "label"`: narrow the archive listing.
- `backup schedule --server SERVER --time 03:00 --timezone America/Los_Angeles`: set a timezone-aware daily schedule. Use `--skip-missed`, `--disable`, or `--remove` to adjust missed-run behavior or pause/remove the schedule.
- `backup health --server SERVER`: verification, key and destination health.
- `backup manage verify --server SERVER --file ID`: isolated recovery validation.
- `backup manage drill --server SERVER --file ID`: stage every included component on the destination filesystem and check copied hashes without stopping Minecraft or changing live files.
- `backup cleanup-destination --server SERVER --destination NAME`: preview independent external retention. Add `--apply` to confirm deletion using the reviewed token. Untracked files, pins, active safety protection, and the newest recorded copy remain protected.
- `backup manage pin` / `unpin`: protect an archive from local retention.
- `backup manage copy --destination NAME`: copy or retry a configured destination.
- `backup manage test_key`: privately prompt for an emergency-kit key and test it.
- `backup prepare-copy --name NEW --port PORT --portv6 PORT`: install a stopped
  destination and prepare a port-remapped archive for a separate reviewed restore.
- `backup upload ARCHIVE`: alias for the native multipart `backup import` command.

Restore review displays file changes and redacted setting differences. A protected
safety backup is created before replacement. Download streams directly to a new
local file, retaining encryption; interrupted transfers remove temporary output.


Backup health includes recovery readiness, active alert reasons, the last isolated
recovery drill, and destination free-space status. Readiness defaults to a maximum
backup age of 48 hours. Periodic isolated drills default to every 168 hours; set
`backups.recovery_drill_interval_hours` to zero to disable them. Archive manifests
remain version 1.

`backup report --server SERVER --output recovery-report.json` writes a redacted
JSON recovery report to a new file and refuses to overwrite an existing file.
Reports contain verification, drill, capacity and restore outcome evidence.
Archive references are hashes; archive filenames, paths, credentials, notes and
configuration values are excluded.

## Interactive API Explorer

Run `bsm-cli api explore`, or select **Advanced API** from the home menu, to browse
live core and plugin operations. Type in the operation/model selectors to search.
Operation views show parameter types and request/response contracts. Build JSON
requests with guided fields (including nested objects, enums, booleans and defaults)
or enter raw JSON. Invalid inputs are rejected before execution; cancelling a
prompt sends no request. Review the redacted preview and choose Execute to send it.

Responses include HTTP status and elapsed time. Switch between structured Body,
Headers and Raw JSON views; filter array items and move through pages of 25 rows.
Nested collections are bounded in the terminal; raw views retain complete results.
The explorer keeps requests and responses in memory for the current action.

Equivalent direct commands are available for scripting and one-off inspection:

```sh
bsm-cli api operations --search backup
bsm-cli api models --search Snapshot
bsm-cli api model SnapshotCreatePayload
bsm-cli api operation create_server_snapshot
bsm-cli api call get_settings --dry-run
bsm-cli api call get_settings --details
bsm-cli api call get_settings --raw
bsm-cli --json api call get_settings
```

`--json` continues to return the complete response body without presentation or
pagination. `--details` opts into an envelope containing `status_code`, `headers`,
`data` and `duration_ms`; it does not change the default result shape.
`--dry-run` validates and previews without executing, concealing credentials and
write-only model fields. `--raw` prints complete JSON instead of terminal tables.
Model/operation inspection also supports `--raw`.

To inspect or execute from an exported contract, place `--schema-file` before the
API subcommand:

```sh
bsm-cli api --schema-file saved-openapi.json explore
bsm-cli api --schema-file saved-openapi.json model SnapshotCreatePayload
```

Imported `servers` URLs never change the configured backend or credentials.
Refresh reloads the selected source. Generic form uploads and streaming downloads
remain available through `api call --form/--file` and `api download`.
