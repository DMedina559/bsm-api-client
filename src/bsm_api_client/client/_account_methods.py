# src/bsm_api_client/client/_account_methods.py
"""Mixin class for account-related API methods."""
import logging
from typing import Any, Dict, Optional, TYPE_CHECKING

from ..models import (
    User,
    ThemeUpdate,
    ProfileUpdate,
    ChangePasswordRequest,
    BaseApiResponse,
)

if TYPE_CHECKING:
    from ..client_base import ClientBase

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.account")


class AccountMethodsMixin:
    """Mixin for account-related endpoints."""

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

    async def async_get_account_details(self) -> User:
        """Gets the current user's account details.

        Returns:
            A `User` object containing the account details.
        """
        _LOGGER.debug("Fetching account details from /account")
        response = await self._request(method="GET", path="/account", authenticated=True)
        return User.model_validate(response)

    async def async_update_theme(self, payload: ThemeUpdate) -> BaseApiResponse:
        """Updates the current user's theme.

        Args:
            payload: A `ThemeUpdate` object containing the new theme.

        Returns:
            A `BaseApiResponse` object indicating the result of the operation.
        """
        _LOGGER.info("Updating theme to %s", payload.theme)
        response = await self._request(
            method="POST",
            path="/account/theme",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return BaseApiResponse.model_validate(response)

    async def async_update_profile(self, payload: ProfileUpdate) -> BaseApiResponse:
        """Updates the current user's profile.

        Args:
            payload: A `ProfileUpdate` object containing the new profile data.

        Returns:
            A `BaseApiResponse` object indicating the result of the operation.
        """
        _LOGGER.info("Updating profile")
        response = await self._request(
            method="POST",
            path="/account/profile",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return BaseApiResponse.model_validate(response)

    async def async_change_password(
        self, payload: ChangePasswordRequest
    ) -> BaseApiResponse:
        """Changes the current user's password.

        Args:
            payload: A `ChangePasswordRequest` object.

        Returns:
            A `BaseApiResponse` object indicating the result of the operation.
        """
        _LOGGER.info("Changing password")
        response = await self._request(
            method="POST",
            path="/account/change-password",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return BaseApiResponse.model_validate(response)
