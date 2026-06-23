"""Mixin class for users-related API methods."""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

from ..models import ActionResponse, BaseApiResponse, UserResponse

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client.users")


class UsersMethodsMixin:
    """Mixin for users-related endpoints."""

    if TYPE_CHECKING:
        # Pydantic models require typing but we don't want to inherit ClientBase
        async def _request(
            self,
            method: str,
            path: str,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            authenticated: bool = True,
            is_retry: bool = False,
        ) -> Any: ...

    async def async_get_users(self) -> List[UserResponse]:
        """Gets a list of all users.

        :returns: A list of `UserResponse` objects.


        .. rubric:: Example:
        .. code-block:: python

            response = await client._request()
        """
        _LOGGER.debug("Fetching users from /users/list")
        response = await self._request(
            method="GET", path="/users/list", authenticated=True
        )
        return [UserResponse.model_validate(user) for user in response]

    async def async_delete_user(self, user_id: int) -> BaseApiResponse:
        """Deletes a user.

        :param user_id: The ID of the user to delete.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_delete_user()
        """
        _LOGGER.info("Deleting user %s", user_id)
        response = await self._request(
            method="POST", path=f"/users/{user_id}/delete", authenticated=True
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

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
        response = await self._request(
            method="POST",
            path=f"/users/{user_id}/role",
            json_data={"role": role},
            authenticated=True,
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

    async def async_disable_user(self, user_id: int) -> BaseApiResponse:
        """Disables a user.

        :param user_id: The ID of the user.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_disable_user()
        """
        _LOGGER.info("Disabling user %s", user_id)
        response = await self._request(
            method="POST", path=f"/users/{user_id}/disable", authenticated=True
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

    async def async_enable_user(self, user_id: int) -> BaseApiResponse:
        """Enables a user.

        :param user_id: The ID of the user.

        :returns: A `BaseApiResponse` object.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_enable_user()
        """
        _LOGGER.info("Enabling user %s", user_id)
        response = await self._request(
            method="POST", path=f"/users/{user_id}/enable", authenticated=True
        )
        return cast(BaseApiResponse, BaseApiResponse.model_validate(response))

    async def async_generate_invite_token(self, role: str) -> ActionResponse:
        """Generates an invite token.

        :param role: The role for the new user.

        :returns: A dict containing the redirect_url.


        .. rubric:: Example:
        .. code-block:: python

            response = await client.async_generate_invite_token()
        """
        _LOGGER.info("Generating invite token for role %s", role)
        response = await self._request(
            method="POST",
            path="/register/generate-token",
            json_data={"role": role},
            authenticated=True,
        )
        return cast(ActionResponse, ActionResponse.model_validate(response))
