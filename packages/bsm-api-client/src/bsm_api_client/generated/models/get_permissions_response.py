from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.player_permission import PlayerPermission


T = TypeVar("T", bound="GetPermissionsResponse")


@_attrs_define
class GetPermissionsResponse:
    """
    Attributes:
        permissions (list[PlayerPermission]):
        message (None | str | Unset):
        status (Literal['success'] | Unset):  Default: 'success'.
    """

    permissions: list[PlayerPermission]
    message: None | str | Unset = UNSET
    status: Literal["success"] | Unset = "success"

    def to_dict(self) -> dict[str, Any]:
        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = permissions_item_data.to_dict()
            permissions.append(permissions_item)

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "permissions": permissions,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.player_permission import PlayerPermission  # noqa: PLC0415

        d = dict(src_dict)
        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = PlayerPermission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

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

        get_permissions_response = cls(
            permissions=permissions,
            message=message,
            status=status,
        )

        return get_permissions_response
