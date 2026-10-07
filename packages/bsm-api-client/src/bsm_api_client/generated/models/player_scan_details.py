from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.player_scan_error import PlayerScanError


T = TypeVar("T", bound="PlayerScanDetails")


@_attrs_define
class PlayerScanDetails:
    """
    Attributes:
        actually_saved_or_updated_in_db (int):
        scan_errors (list[PlayerScanError]):
        total_entries_in_logs (int):
        unique_players_submitted_for_saving (int):
    """

    actually_saved_or_updated_in_db: int
    scan_errors: list[PlayerScanError]
    total_entries_in_logs: int
    unique_players_submitted_for_saving: int

    def to_dict(self) -> dict[str, Any]:
        actually_saved_or_updated_in_db = self.actually_saved_or_updated_in_db

        scan_errors = []
        for scan_errors_item_data in self.scan_errors:
            scan_errors_item = scan_errors_item_data.to_dict()
            scan_errors.append(scan_errors_item)

        total_entries_in_logs = self.total_entries_in_logs

        unique_players_submitted_for_saving = self.unique_players_submitted_for_saving

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "actually_saved_or_updated_in_db": actually_saved_or_updated_in_db,
                "scan_errors": scan_errors,
                "total_entries_in_logs": total_entries_in_logs,
                "unique_players_submitted_for_saving": unique_players_submitted_for_saving,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player_scan_error import PlayerScanError  # noqa: PLC0415

        d = dict(src_dict)
        actually_saved_or_updated_in_db = d.pop("actually_saved_or_updated_in_db")

        scan_errors = []
        _scan_errors = d.pop("scan_errors")
        for scan_errors_item_data in _scan_errors:
            scan_errors_item = PlayerScanError.from_dict(scan_errors_item_data)

            scan_errors.append(scan_errors_item)

        total_entries_in_logs = d.pop("total_entries_in_logs")

        unique_players_submitted_for_saving = d.pop("unique_players_submitted_for_saving")

        player_scan_details = cls(
            actually_saved_or_updated_in_db=actually_saved_or_updated_in_db,
            scan_errors=scan_errors,
            total_entries_in_logs=total_entries_in_logs,
            unique_players_submitted_for_saving=unique_players_submitted_for_saving,
        )

        return player_scan_details
