"""Portable server archive workflows using the generated operation contracts."""

import asyncio
from pathlib import Path
from typing import Any, BinaryIO

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
        self, server_name: str, encrypted: bool | None = None
    ) -> Any:
        """Submit one backup using an optional encryption override.

        :param server_name: Server to capture.
        :param encrypted: Override the configured default, or use None.
        :returns: The accepted background task.
        """
        return await self._call(
            "create_server_snapshot", server_name, body={"encrypted": encrypted}
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
