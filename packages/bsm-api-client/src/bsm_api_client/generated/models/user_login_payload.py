from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserLoginPayload")


@_attrs_define
class UserLoginPayload:
    """Request model for user login credentials.

    Attributes:
        password (str):
        username (str):
        remember_me (bool | Unset):  Default: False.
    """

    password: str
    username: str
    remember_me: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        password = self.password

        username = self.username

        remember_me = self.remember_me

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "password": password,
                "username": username,
            }
        )
        if remember_me is not UNSET:
            field_dict["remember_me"] = remember_me

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        password = d.pop("password")

        username = d.pop("username")

        remember_me = d.pop("remember_me", UNSET)

        user_login_payload = cls(
            password=password,
            username=username,
            remember_me=remember_me,
        )

        user_login_payload.additional_properties = d
        return user_login_payload

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
