# src/pybedrock_server_manager/client.py
"""Main API client class for Bedrock Server Manager.
Combines the base client logic with specific endpoint method mixins.
"""
import logging
from .client_base import ClientBase
from .client._manager_methods import ManagerMethodsMixin
from .client._server_info_methods import ServerInfoMethodsMixin
from .client._server_action_methods import ServerActionMethodsMixin
from .client._content_methods import ContentMethodsMixin
from .client._scheduler_methods import SchedulerMethodsMixin

_LOGGER = logging.getLogger(__name__.split(".")[0] + ".client")


class BedrockServerManagerApi(
    ClientBase,
    ManagerMethodsMixin,
    ServerInfoMethodsMixin,
    ServerActionMethodsMixin,
    ContentMethodsMixin,
    SchedulerMethodsMixin,
):
    """
    API Client for the Bedrock Server Manager.

    This class combines the base connection/authentication logic with
    methods for interacting with various API endpoints, organized via mixins.
    """

    # __init__ is inherited from ClientBase.
    # All async API methods are inherited from mixins.
    pass
