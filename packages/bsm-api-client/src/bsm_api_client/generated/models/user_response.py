from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserResponse")


@_attrs_define
class UserResponse:
    """Pydantic model representing a user.

    Attributes:
        id (int): The user's ID.
        username (str): The user's username.
        identity_type (str): The type of identity (e.g., "local").
        role (str): The user's role.
        is_active (bool): Whether the user is active.
        theme (str): The user's preferred theme. Defaults to "default".

        Attributes:
            id (int):
            is_active (bool):
            role (str):
            username (str):
            identity_type (None | str | Unset):
            theme (str | Unset):  Default: 'default'.
    """

    id: int
    is_active: bool
    role: str
    username: str
    identity_type: None | str | Unset = UNSET
    theme: str | Unset = "default"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        is_active = self.is_active

        role = self.role

        username = self.username

        identity_type: None | str | Unset
        if isinstance(self.identity_type, Unset):
            identity_type = UNSET
        else:
            identity_type = self.identity_type

        theme = self.theme

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "is_active": is_active,
                "role": role,
                "username": username,
            }
        )
        if identity_type is not UNSET:
            field_dict["identity_type"] = identity_type
        if theme is not UNSET:
            field_dict["theme"] = theme

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        is_active = d.pop("is_active")

        role = d.pop("role")

        username = d.pop("username")

        def _parse_identity_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        identity_type = _parse_identity_type(d.pop("identity_type", UNSET))

        theme = d.pop("theme", UNSET)

        user_response = cls(
            id=id,
            is_active=is_active,
            role=role,
            username=username,
            identity_type=identity_type,
            theme=theme,
        )

        user_response.additional_properties = d
        return user_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
