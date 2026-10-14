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
