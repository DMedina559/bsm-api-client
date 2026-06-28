# src/bsm_api_client/client/_account_methods.py
"""Mixin class for account-related API methods."""

import logging
from typing import Any, Callable, cast

from ..models import (
    BaseApiResponse,
    ChangePasswordPayload,
    ProfileUpdatePayload,
    ThemeUpdatePayload,
    UserResponse,
)

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.account")


class AccountMethodsMixin:
    """Mixin for account-related endpoints."""

    _request: Callable[..., Any]

    async def async_get_account_details(self) -> UserResponse:
        """Gets the current user's account details.

        :returns: A `UserResponse` object containing the account details.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_account_details()
        """
        _LOGGER.debug("Fetching account details from /account")
        response = await self._request(
            method="GET", path="/account", authenticated=True
        )
        return cast(UserResponse, UserResponse.model_validate(response))

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
        response = await self._request(
            method="POST",
            path="/account/theme",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

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
        response = await self._request(
            method="POST",
            path="/account/profile",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

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
        response = await self._request(
            method="POST",
            path="/account/change-password",
            json_data=payload.model_dump(),
            authenticated=True,
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))
