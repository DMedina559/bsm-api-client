"""Portable server archive workflows using the generated operation contracts."""

import asyncio
from pathlib import Path
from typing import Any, BinaryIO, Literal

from ..exceptions import OperationFailedError
from .base import Service


class BackupsService(Service):
    """Create, inspect, plan and restore one portable server backup."""

    async def _call(
        self,
        operation: str,
        server_name: str,
        backup_id: str | None = None,
        body: Any = None,
    ) -> Any:
        parameters = {"server_name": server_name}
        if backup_id is not None:
            parameters["backup_id"] = backup_id
        return await self.async_call_generated(
            operation, parameters=parameters, body=body, authenticated=True
        )

    async def async_list(self, server_name: str) -> Any:
        """List archive summaries without decrypting them.

        :param server_name: Destination server name.
        :returns: The backup listing response.
        """
        return await self._call("list_server_snapshots", server_name)

    async def async_create(
        self,
        server_name: str,
        encrypted: bool | None = None,
        *,
        mode: Literal["world", "selected", "full"] | None = None,
        components: list[str] | None = None,
    ) -> Any:
        """Submit one backup using an optional encryption override.

        :param server_name: Server to capture.
        :param encrypted: Override the configured default, or use None.
        :param mode: world, selected, full, or None for global defaults.
        :param components: Component names for selected mode.
        :returns: The accepted background task.
        """
        return await self._call(
            "create_server_snapshot",
            server_name,
            body={
                "encrypted": encrypted,
                **({"mode": mode} if mode is not None else {}),
                **({"components": components} if components is not None else {}),
            },
        )

    async def async_inspect(
        self, server_name: str, backup_id: str, recovery_key: str | None = None
    ) -> Any:
        """Submit authenticated inspection without persisting the recovery key.

        :param server_name: Destination server name.
        :param backup_id: Archive identifier from the listing.
        :param recovery_key: Optional recovery credential.
        :returns: The accepted inspection task.
        """
        return await self._call(
            "inspect_server_snapshot",
            server_name,
            backup_id,
            {"recovery_key": recovery_key},
        )

    async def async_plan(
        self,
        server_name: str,
        backup_id: str,
        components: list[str],
        recovery_key: str | None = None,
    ) -> Any:
        """Submit a restore review against the current destination state.

        :param server_name: Destination server name.
        :param backup_id: Archive identifier.
        :param components: Complete components to replace.
        :param recovery_key: Optional recovery credential.
        :returns: The accepted planning task.
        """
        return await self._call(
            "plan_snapshot_restore",
            server_name,
            backup_id,
            {"components": components, "recovery_key": recovery_key},
        )

    async def async_restore(
        self,
        server_name: str,
        backup_id: str,
        components: list[str],
        token: str,
        recovery_key: str | None = None,
        restart: bool = True,
    ) -> Any:
        """Submit an explicitly reviewed component selection.

        :param server_name: Destination server name.
        :param backup_id: Archive identifier.
        :param components: Reviewed component selection.
        :param token: Token returned by planning.
        :param recovery_key: Optional recovery credential.
        :param restart: Restart an originally running server after success.
        :returns: The accepted restore task.
        """
        return await self._call(
            "restore_server_snapshot",
            server_name,
            backup_id,
            {
                "components": components,
                "token": token,
                "recovery_key": recovery_key,
                "restart": restart,
                "stop_running": True,
            },
        )

    async def async_wait(self, accepted: Any) -> dict[str, Any]:
        """Wait for a submitted task and return its structured result.

        :param accepted: Accepted response containing a task_id.
        :returns: The completed operation result.
        :raises OperationFailedError: If the task fails or is cancelled.
        """
        task_id = (
            accepted.get("task_id") if isinstance(accepted, dict) else accepted.task_id
        )
        if not isinstance(task_id, str) or not task_id:
            raise OperationFailedError("Backup operation did not return a task ID.")
        while True:
            snapshot = await self._owner.tasks.async_get_task_status(task_id)
            if snapshot.status == "completed":
                if not isinstance(snapshot.result, dict):
                    raise OperationFailedError(
                        "Backup task returned an invalid result."
                    )
                return snapshot.result
            if snapshot.status in ("failed", "cancelled"):
                raise OperationFailedError(
                    snapshot.error.message if snapshot.error else snapshot.message
                )
            await asyncio.sleep(0.5)

    async def async_download(self, server_name: str, backup_id: str) -> bytes:
        """Download the stored archive while preserving encryption.

        :param server_name: Source server name.
        :param backup_id: Archive identifier.
        :returns: Stored archive bytes.
        """
        data = await self._call("download_server_snapshot", server_name, backup_id)
        if not isinstance(data, bytes):
            raise OperationFailedError("Backup download returned invalid content.")
        return data

    async def async_import(
        self,
        server_name: str,
        stream: BinaryIO,
        filename: str,
        recovery_key: str | None = None,
    ) -> Any:
        """Upload and validate a portable archive before publishing it.

        :param server_name: Destination server name.
        :param stream: Binary file-like object containing the archive.
        :param filename: Display filename for multipart upload.
        :param recovery_key: Optional credential used to validate encrypted contents.
        :returns: Updated archive listing.
        """
        from ..generated.models.body_import_server_snapshot import (
            BodyImportServerSnapshot,
        )
        from ..generated.types import UNSET, File

        body = BodyImportServerSnapshot(
            file=File(
                payload=stream, file_name=filename, mime_type="application/octet-stream"
            ),
            recovery_key=recovery_key if recovery_key is not None else UNSET,
        )
        return await self._call("import_server_snapshot", server_name, body=body)

    async def async_download_to(
        self, server_name: str, backup_id: str, destination: str | Path
    ) -> Path:
        """Stream an archive to a new local file with bounded memory use.

        :param server_name: Source server name.
        :param backup_id: Archive identifier.
        :param destination: New local destination path.
        :returns: The completed destination path.
        """
        import os
        import tempfile

        target = Path(destination)
        if target.exists():
            raise ValueError("Download destination already exists.")
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(
            prefix=".bsm-download-", dir=target.parent
        )
        try:
            with os.fdopen(descriptor, "wb") as output:
                async with self._owner.async_stream_operation(
                    "download_server_snapshot",
                    path_params={"server_name": server_name, "backup_id": backup_id},
                ) as response:
                    async for chunk in response.aiter_bytes(65536):
                        output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
        return target

    async def async_health(self, server_name: str) -> Any:
        """Read durable verification, recovery-key, and destination health.

        :param server_name: Server to inspect.
        :returns: Backup health response.
        """
        return await self._call("get_backup_health", server_name)

    async def async_manage(
        self,
        server_name: str,
        backup_id: str,
        action: str,
        *,
        destination: str | None = None,
        recovery_key: str | None = None,
        label: str | None = None,
        notes: str | None = None,
    ) -> Any:
        """Manage archive verification, protection, copies, annotations and drills.

        :param server_name: Archive owner.
        :param backup_id: Local archive identifier.
        :param action: verify, pin, unpin, copy, test_key, annotate, drill or delete.
        :param destination: Configured destination name for copy.
        :param label: Manager-local archive label for annotate.
        :param notes: Manager-local archive notes for annotate.
        :param recovery_key: Optional recovery credential; never persisted.
        :returns: Accepted operation task.
        """
        if action not in {
            "verify",
            "pin",
            "unpin",
            "copy",
            "test_key",
            "annotate",
            "drill",
            "delete",
        }:
            raise ValueError("Unsupported backup action.")
        return await self._call(
            "manage_server_snapshot",
            server_name,
            backup_id,
            {
                "action": action,
                "destination": destination,
                "label": label,
                "notes": notes,
                "recovery_key": recovery_key,
            },
        )

    async def async_prepare_copy(
        self,
        server_name: str,
        backup_id: str,
        target_server: str,
        server_port: int,
        server_portv6: int,
        *,
        target_version: str = "LATEST",
        recovery_key: str | None = None,
    ) -> Any:
        """Prepare a stopped new server and an archive with remapped ports.

        :param server_name: Source archive owner.
        :param backup_id: Source archive identifier.
        :param target_server: New server name.
        :param server_port: Destination IPv4 port.
        :param server_portv6: Destination IPv6 port.
        :param target_version: Bedrock version to install.
        :param recovery_key: Optional source recovery credential.
        :returns: Accepted task; review and restore the returned archive separately.
        """
        return await self._call(
            "prepare_backup_copy",
            server_name,
            backup_id,
            {
                "target_server": target_server,
                "server_port": server_port,
                "server_portv6": server_portv6,
                "target_version": target_version,
                "recovery_key": recovery_key,
            },
        )

    async def async_dry_run(
        self,
        server_name: str,
        backup_id: str,
        components: list[str],
        recovery_key: str | None = None,
    ) -> Any:
        """Validate isolated replacement copies without stopping Minecraft.

        :param server_name: Restore destination.
        :param backup_id: Source archive.
        :param components: Components to exercise.
        :param recovery_key: Optional archive recovery credential.
        :returns: Accepted task containing a readiness and capacity report.
        """
        return await self._call(
            "dry_run_server_restore",
            server_name,
            backup_id,
            {"components": components, "recovery_key": recovery_key},
        )

    async def async_set_schedule(
        self, server_name: str, schedule: dict[str, Any] | None
    ) -> Any:
        """Configure or remove a server schedule using administrator settings.

        :param server_name: Scheduled server.
        :param schedule: Daily local time, IANA timezone, weekdays, catch_up and stagger_minutes; None removes it.
        :returns: Updated settings response.
        """
        response = await self.async_call_generated("get_settings", authenticated=True)
        schedules = dict(response["settings"].get("backups", {}).get("schedules", {}))
        if schedule is None:
            schedules.pop(server_name, None)
        else:
            schedules[server_name] = schedule
        await self.async_call_generated(
            "set_setting",
            body={"key": "backups.schedules", "value": schedules},
            authenticated=True,
        )

        return await self.async_call_generated("get_settings", authenticated=True)

    async def async_cleanup_destination(
        self, server_name: str, destination: str, token: str | None = None
    ) -> Any:
        """Preview external cleanup or apply a reviewed, unchanged plan.

        :param server_name: Server whose external copies are inspected.
        :param destination: Saved destination name.
        :param token: Preview token authorizing deletion; None previews only.
        :returns: Accepted task with a destination cleanup plan.
        """
        return await self.async_call_generated(
            "cleanup_backup_destination",
            parameters={"server_name": server_name, "destination": destination},
            body={"token": token},
            authenticated=True,
        )

    async def async_recovery_report(self, server_name: str) -> Any:
        """Read redacted verification, drill, capacity and restore evidence.

        :param server_name: Server whose recovery evidence is exported.
        :returns: Report response without paths, credentials or configuration values.
        """
        return await self._call("download_backup_recovery_report", server_name)
