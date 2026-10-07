from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_properties_response_properties import GetPropertiesResponseProperties


T = TypeVar("T", bound="GetPropertiesResponse")


@_attrs_define
class GetPropertiesResponse:
    """
    Attributes:
        properties (GetPropertiesResponseProperties):
        raw_content (str):
        message (None | str | Unset):
        status (Literal['success'] | Unset):  Default: 'success'.
    """

    properties: GetPropertiesResponseProperties
    raw_content: str
    message: None | str | Unset = UNSET
    status: Literal["success"] | Unset = "success"

    def to_dict(self) -> dict[str, Any]:
        properties = self.properties.to_dict()

        raw_content = self.raw_content

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "properties": properties,
                "raw_content": raw_content,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_properties_response_properties import GetPropertiesResponseProperties  # noqa: PLC0415

        d = dict(src_dict)
        properties = GetPropertiesResponseProperties.from_dict(d.pop("properties"))

        raw_content = d.pop("raw_content")

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

        get_properties_response = cls(
            properties=properties,
            raw_content=raw_content,
            message=message,
            status=status,
        )

        return get_properties_response
