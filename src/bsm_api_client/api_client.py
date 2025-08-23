# src/bsm_api_client/client.py
"""Main API client class for Bedrock Server Manager.

This module provides the main API client class, `BedrockServerManagerApi`,
which integrates connection handling, authentication, and various API
endpoint methods organized into mixins.
"""
import logging
from .client_base import ClientBase
from .client._manager_methods import ManagerMethodsMixin
from .client._server_info_methods import ServerInfoMethodsMixin
from .client._server_action_methods import ServerActionMethodsMixin
from .client._content_methods import ContentMethodsMixin
from .client._plugin_methods import PluginMethodsMixin
from .client._account_methods import AccountMethodsMixin

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client")


class BedrockServerManagerApi(
    ClientBase,
    ManagerMethodsMixin,
    ServerInfoMethodsMixin,
    ServerActionMethodsMixin,
    ContentMethodsMixin,
    PluginMethodsMixin,
    AccountMethodsMixin,
):
    """API Client for the Bedrock Server Manager.

    This class combines the base connection and authentication logic from
    `ClientBase` with methods for interacting with various API endpoints,
    which are organized into mixin classes.

    Example:
        >>> from bsm_api_client import BedrockServerManagerApi
        >>> client = BedrockServerManagerApi("http://localhost:8080", "admin", "password")
        >>> await client.async_get_info()
    """

    # __init__ is inherited from ClientBase.
    # All async API methods are inherited from mixins.

    @property
    def servers(self):
        """Provides access to server-related methods.

        This is a convenience property that returns the client instance itself,
        allowing for a more intuitive call structure (e.g., `client.servers.async_get_list()`).

        Returns:
            The client instance.
        """
        return self
