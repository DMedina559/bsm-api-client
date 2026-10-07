from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ProcessInfo")


@_attrs_define
class ProcessInfo:
    """
    Attributes:
        cpu_percent (float):
        memory_mb (float):
        pid (int):
        uptime (str):
    """

    cpu_percent: float
    memory_mb: float
    pid: int
    uptime: str

    def to_dict(self) -> dict[str, Any]:
        cpu_percent = self.cpu_percent

        memory_mb = self.memory_mb

        pid = self.pid

        uptime = self.uptime

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb,
                "pid": pid,
                "uptime": uptime,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_percent = d.pop("cpu_percent")

        memory_mb = d.pop("memory_mb")

        pid = d.pop("pid")

        uptime = d.pop("uptime")

        process_info = cls(
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
            pid=pid,
            uptime=uptime,
        )

        return process_info
