import logging
from typing import cast

from ..models import (
    BaseApiResponse,
    ChangePasswordPayload,
    ProfileUpdatePayload,
    ThemeUpdatePayload,
    UserResponse,
)
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.account")


class AccountService(Service):
    """Service for account-related endpoints."""

    async def async_get_account_details(self) -> UserResponse:
        """Gets the current user's account details.

        :returns: `UserResponse`.

        .. code-block:: python

            response = await client.account.async_get_account_details()
        """
        _LOGGER.debug("Fetching account details from /account")
        response = await self.async_call_generated(
            "get_account", authenticated=True, typed=True
        )
        return cast(UserResponse, parse_response(UserResponse, response))

    async def async_update_theme(self, payload: ThemeUpdatePayload) -> BaseApiResponse:
        """Updates the current user's theme.

        :param payload: A `ThemeUpdatePayload` object containing the new theme.

        :returns: `BaseApiResponse`.

        .. code-block:: python

            response = await client.account.async_update_theme(payload)
        """
        _LOGGER.info("Updating theme to %s", payload.theme)
        response = await self.async_call_generated(
            "update_account_theme",
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_update_profile(
        self, payload: ProfileUpdatePayload
    ) -> BaseApiResponse:
        """Updates the current user's profile.

        :param payload: A `ProfileUpdatePayload` object containing the new profile data.

        :returns: `BaseApiResponse`.

        .. code-block:: python

            response = await client.account.async_update_profile(payload)
        """
        _LOGGER.info("Updating profile")
        response = await self.async_call_generated(
            "update_account_profile",
            body=payload.model_dump(),
            authenticated=True,
            typed=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_change_password(
        self, payload: ChangePasswordPayload
    ) -> BaseApiResponse:
        """Changes the current user's password.

        :param payload: A `ChangePasswordPayload` object.

        :returns: `BaseApiResponse`.

        .. code-block:: python

            response = await client.account.async_change_password(payload)
        """
        _LOGGER.info("Changing password")
        response = await self.async_call_generated(
            "change_password", body=payload.to_dict(), authenticated=True, typed=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))
