from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ban_info import BanInfo


T = TypeVar("T", bound="GetServerBansResponse")


@_attrs_define
class GetServerBansResponse:
    """
    Attributes:
        bans (list[BanInfo]):
        message (None | str | Unset):
        status (Literal['success'] | Unset):  Default: 'success'.
    """

    bans: list[BanInfo]
    message: None | str | Unset = UNSET
    status: Literal["success"] | Unset = "success"

    def to_dict(self) -> dict[str, Any]:
        bans = []
        for bans_item_data in self.bans:
            bans_item = bans_item_data.to_dict()
            bans.append(bans_item)

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "bans": bans,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ban_info import BanInfo  # noqa: PLC0415

        d = dict(src_dict)
        bans = []
        _bans = d.pop("bans")
        for bans_item_data in _bans:
            bans_item = BanInfo.from_dict(bans_item_data)

            bans.append(bans_item)

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        status = cast(Literal["success"] | Unset, d.pop("status", UNSET))
        if status != "success" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'success', got '{status}'")

        get_server_bans_response = cls(
            bans=bans,
            message=message,
            status=status,
        )

        return get_server_bans_response
