from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.servers_list_response_status import ServersListResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.server_summary import ServerSummary


T = TypeVar("T", bound="ServersListResponse")


@_attrs_define
class ServersListResponse:
    """Response model for lists of server data.

    Attributes:
        status (ServersListResponseStatus):
        message (None | str | Unset):
        servers (list[ServerSummary] | None | Unset):
    """

    status: ServersListResponseStatus
    message: None | str | Unset = UNSET
    servers: list[ServerSummary] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        servers: list[dict[str, Any]] | None | Unset
        if isinstance(self.servers, Unset):
            servers = UNSET
        elif isinstance(self.servers, list):
            servers = []
            for servers_type_0_item_data in self.servers:
                servers_type_0_item = servers_type_0_item_data.to_dict()
                servers.append(servers_type_0_item)

        else:
            servers = self.servers

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if servers is not UNSET:
            field_dict["servers"] = servers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.server_summary import ServerSummary  # noqa: PLC0415

        d = dict(src_dict)
        status = ServersListResponseStatus(d.pop("status"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_servers(data: object) -> list[ServerSummary] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                servers_type_0 = []
                _servers_type_0 = data
                for servers_type_0_item_data in _servers_type_0:
                    servers_type_0_item = ServerSummary.from_dict(servers_type_0_item_data)

                    servers_type_0.append(servers_type_0_item)

                return servers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ServerSummary] | None | Unset, data)

        servers = _parse_servers(d.pop("servers", UNSET))

        servers_list_response = cls(
            status=status,
            message=message,
            servers=servers,
        )

        return servers_list_response
