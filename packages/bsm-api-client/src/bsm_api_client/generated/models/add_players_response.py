from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.add_players_response_status import AddPlayersResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player_scan_details import PlayerScanDetails


T = TypeVar("T", bound="AddPlayersResponse")


@_attrs_define
class AddPlayersResponse:
    """Response model for adding players, typically returns just inherited fields or single item data.

    Attributes:
        status (AddPlayersResponseStatus):
        count (int | None | Unset):
        details (None | PlayerScanDetails | Unset):
        message (None | str | Unset):
    """

    status: AddPlayersResponseStatus
    count: int | None | Unset = UNSET
    details: None | PlayerScanDetails | Unset = UNSET
    message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.player_scan_details import PlayerScanDetails  # noqa: PLC0415

        status = self.status.value

        count: int | None | Unset
        if isinstance(self.count, Unset):
            count = UNSET
        else:
            count = self.count

        details: dict[str, Any] | None | Unset
        if isinstance(self.details, Unset):
            details = UNSET
        elif isinstance(self.details, PlayerScanDetails):
            details = self.details.to_dict()
        else:
            details = self.details

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if details is not UNSET:
            field_dict["details"] = details
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player_scan_details import PlayerScanDetails  # noqa: PLC0415

        d = dict(src_dict)
        status = AddPlayersResponseStatus(d.pop("status"))

        def _parse_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        count = _parse_count(d.pop("count", UNSET))

        def _parse_details(data: object) -> None | PlayerScanDetails | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                details_type_0 = PlayerScanDetails.from_dict(data)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PlayerScanDetails | Unset, data)

        details = _parse_details(d.pop("details", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        add_players_response = cls(
            status=status,
            count=count,
            details=details,
            message=message,
        )

        return add_players_response
