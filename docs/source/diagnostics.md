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
