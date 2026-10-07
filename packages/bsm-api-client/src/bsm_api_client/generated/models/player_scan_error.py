from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PlayerScanError")


@_attrs_define
class PlayerScanError:
    """
    Attributes:
        error (str):
        server (str):
    """

    error: str
    server: str

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        server = self.server

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "server": server,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        server = d.pop("server")

        player_scan_error = cls(
            error=error,
            server=server,
        )

        return player_scan_error
