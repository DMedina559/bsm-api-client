# src/bsm_api_client/client/_account_methods.py
"""Mixin class for account-related API methods."""

import logging
from typing import cast

from ..generated_adapter import GeneratedOperationMethods
from ..models import (
    BaseApiResponse,
    ChangePasswordPayload,
    ProfileUpdatePayload,
    ThemeUpdatePayload,
    UserResponse,
)
from ..validation import parse_response

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.account")


class AccountMethodsMixin(GeneratedOperationMethods):
    """Mixin for account-related endpoints."""

    async def async_get_account_details(self) -> UserResponse:
        """Gets the current user's account details.

        :returns: A `UserResponse` object containing the account details.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_account_details()
        """
        _LOGGER.debug("Fetching account details from /account")
        response = await self.async_call_generated("get_account", authenticated=True)
        return cast(UserResponse, parse_response(UserResponse, response))

    async def async_update_theme(self, payload: ThemeUpdatePayload) -> BaseApiResponse:
        """Updates the current user's theme.

        :param payload: A `ThemeUpdatePayload` object containing the new theme.

        :returns: A `BaseApiResponse` object indicating the result of the operation.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_update_theme(payload)
        """
        _LOGGER.info("Updating theme to %s", payload.theme)
        response = await self.async_call_generated(
            "update_account_theme", body=payload.model_dump(), authenticated=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_update_profile(
        self, payload: ProfileUpdatePayload
    ) -> BaseApiResponse:
        """Updates the current user's profile.

        :param payload: A `ProfileUpdatePayload` object containing the new profile data.

        :returns: A `BaseApiResponse` object indicating the result of the operation.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_update_profile(payload)
        """
        _LOGGER.info("Updating profile")
        response = await self.async_call_generated(
            "update_account_profile", body=payload.model_dump(), authenticated=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_change_password(
        self, payload: ChangePasswordPayload
    ) -> BaseApiResponse:
        """Changes the current user's password.

        :param payload: A `ChangePasswordPayload` object.

        :returns: A `BaseApiResponse` object indicating the result of the operation.


        .. rubric:: Example:
        .. code-block:: python

            payload = ...
            response = await client.async_change_password(payload)
        """
        _LOGGER.info("Changing password")
        response = await self.async_call_generated(
            "change_password", body=payload.model_dump(), authenticated=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))
