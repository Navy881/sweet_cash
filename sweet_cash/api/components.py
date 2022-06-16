import abc
import aiohttp
import contextlib
from typing import Any, Optional, List
from aiopg.sa import Engine, create_engine
from socket import AF_INET

from sweet_cash.settings import Settings


class State:

    def __init__(self) -> None:
        super(State, self).__setattr__("_state", {})

    def __setattr__(self, key: str, value: Any) -> None:
        self._state[key] = value

    def __getattr__(self, key: str) -> Any:
        try:
            return self._state[key]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __delattr__(self, key: str) -> None:
        del self._state[key]


class FastAPIStateManager(metaclass=abc.ABCMeta):

    def __init__(self, components: List[Any], settings: Settings) -> None:
        self.settings = settings
        self.components = components

        self.state = State()
        # self.state._state_manager = self
        self.state.settings = settings
        self.started = False

    async def startup(self) -> None:
        """Последовательный вызов startup для каждого компонента с передачей в него state.
        Изначально в state только settings."""
        for component in self.components:
            self.state = await component.startup(self.state)

        self.started = True

    async def shutdown(self) -> None:
        """Вызовет shutdown каждого компонента в обратном порядке."""
        if self.started:
            for component in reversed(self.components):
                await component.shutdown()

    def set_fastapi_startup_hook(self, app: "FastAPI") -> None:
        """Выставление startup hook приложению при вызове у себя startup
        и перезапись state на свой"""

        async def hook() -> None:
            await self.startup()

            # this is dangerous
            app.state = self.state  # type: ignore

        app.router.add_event_handler("startup", hook)

    def set_fastapi_shutdown_hook(self, app: "FastAPI") -> None:
        """Выставление shutdown hook приложению при вызове у себя shutdown"""

        async def hook() -> None:
            await self.shutdown()

        app.router.add_event_handler("shutdown", hook)


class AIOPostgresComponent(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.engine: Optional[Engine] = None
        self._exit_stack = contextlib.AsyncExitStack()

    async def startup(self, state: State) -> State:
        settings = state.settings

        self.engine = await self._create_engine(settings)
        state.db = self.engine
        return state

    async def shutdown(self) -> None:
        await self._exit_stack.aclose()

    async def _create_engine(self, settings: Settings) -> Engine:
        return await self._exit_stack.enter_async_context(
            create_engine(
                dsn=settings.POSTGRESQL_DATABASE_URI,
                maxsize=settings.POSTGRESQL_POOL_SIZE,
                timeout=settings.POSTGRESQL_CONNECTION_TIMEOUT
            )
        )


class AIOHTTPSessionComponent(metaclass=abc.ABCMeta):
    session: Optional[aiohttp.ClientSession]

    async def startup(self, state: State) -> State:
        settings = state.settings

        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=2),
            connector=aiohttp.TCPConnector(family=AF_INET, limit_per_host=settings.SIZE_POOL_AIOHTTP)
        )
        state.session = self.session
        return state

    async def shutdown(self) -> None:
        if self.session:
            await self.session.close()
