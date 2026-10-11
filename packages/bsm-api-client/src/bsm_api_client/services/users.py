import logging
from typing import List, cast

from ..models import BaseApiResponse, RegistrationResponse, UserResponse
from ..validation import parse_response
from .base import Service

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.users")


class UsersService(Service):
    """Service for users-related endpoints."""

    async def async_get_users(self) -> List[UserResponse]:
        """Gets a list of all users.

        :returns: A list of `UserResponse` objects.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_get_users()
        """
        _LOGGER.debug("Fetching users from /users/list")
        response = await self.async_call_generated("list_users", authenticated=True)
        return [parse_response(UserResponse, user) for user in response]

    async def async_delete_user(self, user_id: int) -> BaseApiResponse:
        """Deletes a user.

        :param user_id: The ID of the user to delete.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_delete_user()
        """
        _LOGGER.info("Deleting user %s", user_id)
        response = await self.async_call_generated(
            "delete_user", parameters={"user_id": user_id}, authenticated=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_update_user_role(self, user_id: int, role: str) -> BaseApiResponse:
        """Updates a user's role.

        :param user_id: The ID of the user.
        :param role: The new role.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_update_user_role()
        """
        _LOGGER.info("Updating role for user %s to %s", user_id, role)
        response = await self.async_call_generated(
            "update_user_role",
            parameters={"user_id": user_id},
            body={"role": role},
            authenticated=True,
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_disable_user(self, user_id: int) -> BaseApiResponse:
        """Disables a user.

        :param user_id: The ID of the user.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_disable_user()
        """
        _LOGGER.info("Disabling user %s", user_id)
        response = await self.async_call_generated(
            "disable_user", parameters={"user_id": user_id}, authenticated=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_enable_user(self, user_id: int) -> BaseApiResponse:
        """Enables a user.

        :param user_id: The ID of the user.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_enable_user()
        """
        _LOGGER.info("Enabling user %s", user_id)
        response = await self.async_call_generated(
            "enable_user", parameters={"user_id": user_id}, authenticated=True
        )
        return cast(BaseApiResponse, parse_response(BaseApiResponse, response))

    async def async_generate_invite_token(self, role: str) -> RegistrationResponse:
        """Generates an invite token.

        :param role: The role for the new user.

        :returns: A dict containing the redirect_url.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_generate_invite_token()
        """
        _LOGGER.info("Generating invite token for role %s", role)
        response = await self.async_call_generated(
            "generate_registration_token", body={"role": role}, authenticated=True
        )
        return cast(
            RegistrationResponse, parse_response(RegistrationResponse, response)
        )
