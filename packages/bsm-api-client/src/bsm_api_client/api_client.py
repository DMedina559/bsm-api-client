"""BSM SDK: generated REST operations plus domain and live extensions."""

from typing import TYPE_CHECKING

import aiohttp
import httpx

from .client_base import ClientBase
from .dynamic import DynamicOpenAPIMixin
from .services.account import AccountService
from .services.application import ApplicationService
from .services.content import ContentService
from .services.diagnostics import DiagnosticsService
from .services.discovery import DiscoveryService
from .services.events import EventService
from .services.players import PlayersService
from .services.plugins import PluginsService
from .services.servers import ServersService
from .services.tasks import TasksService
from .services.users import UsersService

if TYPE_CHECKING:
    from .generated.rest import RestClient


class BedrockServerManagerApi(DynamicOpenAPIMixin, ClientBase):
    """Own authentication and transports; services own domain workflows.

    Generated endpoints are available through ``async_call_generated`` and
    ``async_get_generated_client``. Use ``rest`` for typed operation-ID methods
    and the service attributes for domain workflows. ``discovery`` exposes
    operations advertised by the live backend and its plugins.
    """

    rest: "RestClient"
    diagnostics: DiagnosticsService
    events: EventService
    discovery: DiscoveryService
    application: ApplicationService
    servers: ServersService
    players: PlayersService
    tasks: TasksService
    content: ContentService
    account: AccountService
    users: UsersService
    plugins: PluginsService

    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
        jwt_token: str | None = None,
        session: aiohttp.ClientSession | None = None,
        base_path: str = "/api",
        request_timeout: float = 90,
        verify_ssl: bool = True,
        http_client: httpx.AsyncClient | None = None,
        remember_me: bool = False,
    ) -> None:
        """Create the SDK and its domain services without opening a WebSocket.

        Provide a JWT token or both username and password. base_url may include
        a reverse-proxy mount; base_path selects the REST API prefix.
        request_timeout applies to REST requests in seconds. verify_ssl controls
        owned transports. Optional http_client and session transports remain
        caller-owned; session is used only for WebSockets. remember_me requests
        the backend-configured longer token lifetime for credential login and
        reauthentication. It defaults to False and cannot extend a supplied JWT.
        """
        super().__init__(
            base_url=base_url,
            username=username,
            password=password,
            jwt_token=jwt_token,
            session=session,
            base_path=base_path,
            request_timeout=request_timeout,
            verify_ssl=verify_ssl,
            http_client=http_client,
            remember_me=remember_me,
        )
        from .generated.rest import RestClient

        self.rest = RestClient(self)
        self.discovery = DiscoveryService(self)
        self.diagnostics = DiagnosticsService(self)
        self.events = EventService(self)
        self.application = ApplicationService(self)
        self.servers = ServersService(self)
        self.players = PlayersService(self)
        self.tasks = TasksService(self)
        self.content = ContentService(self)
        self.plugins = PluginsService(self)
        self.account = AccountService(self)
        self.users = UsersService(self)
