# Diagnostics and support reports

Diagnostics endpoints require an administrator and a backend supporting the advertised operations. Missing readings remain unknown or unavailable; they must not be converted into zero or healthy states.

```python
snapshot = await client.diagnostics.async_get_application_diagnostics()
report = await client.diagnostics.async_get_diagnostic_report()
print(snapshot.summary)
print(report.model_dump(mode="json"))
```

Read one subsystem with `async_get_subsystem_diagnostics("events")`. History accepts bounded filters and cursor pagination:

```python
page = await client.diagnostics.async_get_diagnostic_history(limit=50)
while page.next_cursor:
    page = await client.diagnostics.async_get_diagnostic_history(
        limit=50, cursor=page.next_cursor,
    )
```

Keep the same filters across pages. History is a retained best-effort support journal, not a guaranteed audit log. Live counters reset at backend restart. Runs and traces expose retained instance/correlation metadata; missing sources remain explicit.

```python
from bsm_api_client.models import CompareDiagnosticSnapshotsRequest

after = await client.diagnostics.async_get_application_diagnostics()
comparison = await client.diagnostics.async_compare_diagnostic_snapshots(
    CompareDiagnosticSnapshotsRequest(before=snapshot, after=after)
)
```

Counter deltas depend on instance identity and chronological snapshots. A process restart is a reset, not negative activity. Reports omit payloads but can contain installation-identifying names; review them before sharing.


## Global activity across execution chains

```python
activity = await client.diagnostics.async_get_diagnostic_activity(server_name="example")
for operation in activity.operations.recent if activity.operations else []:
    print(operation.name, operation.status, operation.outcome, operation.parent_operation_id)
```

The typed response includes active/recent events, active/recent operations, listener
configuration/statistics, per-source availability (`None`), issues and truncation.
No correlation filter is required. Existing snapshots and reports also carry the
new Events section details, and traces expose `operations_available` separately.
Older trace responses without these fields remain valid. Global activity requires
a backend advertising `get_diagnostic_activity`; it does not emulate unavailable
operation metadata on older servers.

Use `bsm-cli diagnostics activity --server-name example` or
`bsm-cli --json diagnostics activity --sequence-id SEQUENCE_ID`. Add
`--event-name`, `--operation-name`, `--owner`, `--source`, `--operation-id`,
`--correlation-id`, `--phase`, `--status`, or `--limit` as needed. Limits are bounded
by backend diagnostic settings. Event status filters apply only to events; listener
configuration follows event-name/owner filters. This metadata history resets on
restart and excludes payloads, credentials and task arguments.

The existing `client.events.async_get_event_activity()` and
`bsm-cli events activity` also accept server, source, operation name/ID,
sequence ID, and phase filters in addition to their previous filters.


## Backup and verification schedules

`client.scheduler.async_list_schedules(server_name=None)` returns durable task
configuration, handler availability, next occurrence and recent run outcomes.
Create or replace a job with `async_save_schedule(schedule_id, ScheduledTask(...))`
and remove it with `async_delete_schedule(schedule_id)`. Administrator access is
required. The SDK exports `ScheduledTask`, `ScheduleEntry` and `ListSchedulesResponse`.

```python
from bsm_api_client.models import ScheduledTask

await client.scheduler.async_save_schedule("weekly-verify", ScheduledTask(
    task="verify", server_name="MyServer", enabled=True,
    time="04:00", timezone="UTC", weekdays=[6],
    options={"minimum_age_hours": 168},
))
```

CLI equivalents are `bsm-cli scheduler list`,
`bsm-cli scheduler save weekly-verify schedule.json`, and
`bsm-cli scheduler remove weekly-verify` (all support the global `--json` option).
Saving uses a JSON file with the same `ScheduledTask` fields.

Full verification after capture, periodic verification and automatic recovery
drills default to off on new installations. Existing explicitly configured
intervals are retained. A new archive is **unverified** until checked. Restore
integrity validation remains mandatory. Configure `backups.verify_after_create`
through the existing settings service for immediate verification; alternatively
create an independent `verify` job. Backup summaries include per-stage durations
in `stage_durations_ms`. The existing backup manage method also accepts `delete`
for unpinned local archives outside their safety protection window.

Lifecycle endpoints remain synchronous. Choose a `request_timeout` appropriate
for long pre-start backups and check status before retrying an interrupted write.


### Schedule clock metadata

The schedule listing includes supported `timezones`, a
`timezone_database_available` flag, `server_time` in UTC, and the display-only
`host_timezone`. Use `America/Los_Angeles` for Pacific Time, rather than `PDT`.
Schedules keep their regional wall-clock time and derive each occurrence in UTC,
including daylight-saving transitions. A fixed conversion to the host offset
would change the local execution hour after a seasonal clock change.

Storage now observes schedule writes through its ordinary transaction boundary.
Committed definitions appear in AppState, and runtime health checks track the
scheduler heartbeat and timezone data. Scheduler diagnostics use the existing
4.0 metadata shape and include correlated run history. CLI schedule listings show
each job's server, task and regional execution time.


### Application timezone

`general.timezone` defaults to `UTC`. Set it with the existing global-settings
service; no new endpoint is required. Read the display default without admin
settings access using `(await client.application.async_get_info()).info.get(
"timezone", "UTC")`. Older servers may omit the metadata.

Use IANA regions such as `America/Los_Angeles`, not seasonal abbreviations such
as `PDT`. New scheduler configurations that omit `timezone` inherit this setting;
updates that omit it preserve the saved job's timezone. The SDK and CLI preserve
omitted fields on the wire. Explicit `timezone="UTC"` always remains UTC.

API event, diagnostic, and backup timestamps remain UTC instants. Changing the
application timezone never changes archive identifiers or existing recorded
instants. Consumers can convert for display and retain the original value in
details. Numeric metrics and diagnostic timestamps use epoch seconds.
