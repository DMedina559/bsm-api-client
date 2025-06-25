# src/bsm_api_client/client/_content_methods.py
"""Mixin class containing content management methods (worlds, addons)."""
import logging
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from urllib.parse import quote  # For URL encoding path parameters

if TYPE_CHECKING:
    from ..client_base import ClientBase
    from ..exceptions import APIError  # For type hinting

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.content")


class ContentMethodsMixin:
    """Mixin for content management endpoints (worlds, addons)."""

    _request: callable
    if TYPE_CHECKING:

        async def _request(
            self: "ClientBase",
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
        ) -> Any: ...

    async def async_get_content_worlds(self) -> List[str]:
        """
        Lists available world template files (.mcworld) from the manager's content directory.

        Corresponds to `GET /api/content/worlds`.
        Requires authentication.

        Returns:
            A list of world filenames (basenames).

        Raises:
            APIError: For API communication or processing errors.
        """
        _LOGGER.debug("Fetching available world files from /content/worlds")
        try:
            response_data = await self._request(
                "GET", "/content/worlds", authenticated=True
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("files"), list)
            ):
                return [str(f) for f in response_data["files"] if isinstance(f, str)]

            _LOGGER.error(
                "Received non-success or unexpected structure for content worlds: %s",
                response_data,
            )
            # Ensure APIError is available
            from ..exceptions import APIError as ClientAPIError  # Use an alias

            raise ClientAPIError(
                f"Failed to get content worlds, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:  # type: ignore
            _LOGGER.error("API error fetching content worlds: %s", e)
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing content worlds response: %s", e
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(f"Unexpected error processing content worlds: {e}")

    async def async_get_content_addons(self) -> List[str]:
        """
        Lists available addon files (.mcpack, .mcaddon) from the manager's content directory.

        Corresponds to `GET /api/content/addons`.
        Requires authentication.

        Returns:
            A list of addon filenames (basenames).

        Raises:
            APIError: For API communication or processing errors.
        """
        _LOGGER.debug("Fetching available addon files from /content/addons")
        try:
            response_data = await self._request(
                "GET", "/content/addons", authenticated=True
            )
            if (
                isinstance(response_data, dict)
                and response_data.get("status") == "success"
                and isinstance(response_data.get("files"), list)
            ):
                return [str(f) for f in response_data["files"] if isinstance(f, str)]

            _LOGGER.error(
                "Received non-success or unexpected structure for content addons: %s",
                response_data,
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(
                f"Failed to get content addons, API response: {response_data.get('status') if isinstance(response_data, dict) else 'N/A'}",
                response_data=(
                    response_data
                    if isinstance(response_data, dict)
                    else {"raw": response_data}
                ),
            )
        except APIError as e:  # type: ignore
            _LOGGER.error("API error fetching content addons: %s", e)
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error processing content addons response: %s", e
            )
            from ..exceptions import APIError as ClientAPIError

            raise ClientAPIError(f"Unexpected error processing content addons: {e}")

    async def async_export_server_world(self, server_name: str) -> Dict[str, Any]:
        """
        Exports the current world of a server to a .mcworld file in the content directory.
        Response includes `{"export_file": "/full/path/..."}`.

        Corresponds to `POST /api/server/{server_name}/world/export`.
        Requires authentication.

        Args:
            server_name: The name of the server whose world to export.
        Returns:
            API response dictionary.
        """
        _LOGGER.info("Triggering world export for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/world/export",
            json_data=None,  # No body for this POST
            authenticated=True,
        )

    async def async_reset_server_world(self, server_name: str) -> Dict[str, Any]:
        """
        Resets the current world of a server.

        Corresponds to `DELETE /api/server/{server_name}/world/reset`.
        Requires authentication.

        Args:
            server_name: The name of the server whose world to reset.
        Returns:
            API response dictionary.
        """
        _LOGGER.warning("Triggering world reset for server '%s'", server_name)
        encoded_server_name = quote(server_name)
        return await self._request(
            "DELETE",
            f"/server/{encoded_server_name}/world/reset",
            json_data=None,  # No body for this DELETE
            authenticated=True,
        )

    async def async_install_server_world(
        self, server_name: str, filename: str
    ) -> Dict[str, Any]:
        """
        Installs a world from a .mcworld file (from content directory) to a server.

        Corresponds to `POST /api/server/{server_name}/world/install`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            filename: The name of the .mcworld file (relative to content/worlds dir).
        Returns:
            API response dictionary.
        """
        _LOGGER.info(
            "Requesting world install for server '%s' from file '%s'",
            server_name,
            filename,
        )
        if not filename or not isinstance(filename, str):
            from ..exceptions import InvalidInputError  # Local import

            raise InvalidInputError("Filename must be a non-empty string.")

        payload = {"filename": filename}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/world/install",
            json_data=payload,
            authenticated=True,
        )

    async def async_install_server_addon(
        self, server_name: str, filename: str
    ) -> Dict[str, Any]:
        """
        Installs an addon (.mcaddon or .mcpack file from content directory) to a server.

        Corresponds to `POST /api/server/{server_name}/addon/install`.
        Requires authentication.

        Args:
            server_name: The name of the server.
            filename: The name of the addon file (relative to content/addons dir).
        Returns:
            API response dictionary.
        """
        _LOGGER.info(
            "Requesting addon install for server '%s' from file '%s'",
            server_name,
            filename,
        )
        if not filename or not isinstance(filename, str):
            from ..exceptions import InvalidInputError  # Local import

            raise InvalidInputError("Filename must be a non-empty string.")

        payload = {"filename": filename}
        encoded_server_name = quote(server_name)
        return await self._request(
            "POST",
            f"/server/{encoded_server_name}/addon/install",
            json_data=payload,
            authenticated=True,
        )
