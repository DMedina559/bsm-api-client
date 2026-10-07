from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllowlistAddPayload")


@_attrs_define
class AllowlistAddPayload:
    """Request model for adding players to the allowlist.

    Attributes:
        players (list[str]): List of player gamertags to add.
        ignores_player_limit (bool | Unset): Set 'ignoresPlayerLimit' for these players. Default: False.
    """

    players: list[str]
    ignores_player_limit: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        players = self.players

        ignores_player_limit = self.ignores_player_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "players": players,
            }
        )
        if ignores_player_limit is not UNSET:
            field_dict["ignoresPlayerLimit"] = ignores_player_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        players = cast(list[str], d.pop("players"))

        ignores_player_limit = d.pop("ignoresPlayerLimit", UNSET)

        allowlist_add_payload = cls(
            players=players,
            ignores_player_limit=ignores_player_limit,
        )

        allowlist_add_payload.additional_properties = d
        return allowlist_add_payload

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
