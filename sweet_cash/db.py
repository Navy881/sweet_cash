import abc
import sqlalchemy
import aiopg.sa
from typing import Any, Dict, Optional, List
import contextlib
from contextlib import asynccontextmanager

from aiopg.sa import Engine, SAConnection, create_engine
from pydantic import BaseModel, PostgresDsn
from pydantic.types import PositiveInt


from sweet_cash.settings import Settings


def engine(db_url):
    return sqlalchemy.create_engine(db_url, pool_pre_ping=True)

# engine = sqlalchemy.create_engine(Settings.POSTGRESQL_DATABASE_URI, pool_pre_ping=True)


# def pg_engine():
#     pg_engine = aiopg.sa.create_engine(user=Settings.POSTGRESQL_USER,
#                                        database=Settings.POSTGRESQL_DATABASE,
#                                        host=Settings.POSTGRESQL_SERVER,
#                                        password=Settings.POSTGRESQL_PASSWORD)
#     return pg_engine


# class State:
#     """Контейнер стейта приложения"""
#
#     def __init__(self, state: Optional[Dict[str, Any]] = None) -> None:
#         if state is None:
#             state = {}
#         super(State, self).__setattr__("_state", state)
#
#     def __setattr__(self, key: str, value: Any) -> None:
#         self._state[key] = value
#
#     def __getattr__(self, key: str) -> Any:
#         try:
#             return self._state[key]
#         except KeyError:
#             raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
#
#     def __delattr__(self, key: str) -> None:
#         del self._state[key]


# class Lifecycle(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     async def startup(self) -> None:
#         pass
#
#     @abc.abstractmethod
#     async def shutdown(self) -> None:
#         pass


# class BaseComponent(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def _get_settings_model(self) -> Optional[type[BaseModel]]:
#         pass
#
#     @staticmethod
#     def _check_providing_settings(app_settings: type[BaseModel], component_settings: Optional[type[BaseModel]]) -> None:
#         if component_settings is None:
#             return
#
#         component_external_fields = {field.alias for field in component_settings.__fields__.values()}
#         app_fields = {field.name for field in app_settings.__fields__.values()}
#
#         missing_fields = component_external_fields - app_fields
#         if missing_fields:
#             raise AttributeError(
#                 f"Application settings do not provide the "
#                 f"following attributes required for the component: {sorted(missing_fields)}"
#             )
#
#     @abc.abstractmethod
#     async def startup(self, state: State) -> State:
#         self._check_providing_settings(state.settings, self._get_settings_model())
#         return state
#
#     @abc.abstractmethod
#     async def shutdown(self) -> None:
#         pass


# class StateManager(metaclass=abc.ABCMeta):
#     """Манагер стейта."""
#
#     def __init__(self, components: List[Any], settings: Settings) -> None:
#         """
#         Args:
#             components: список компонентов
#             settings: настройки
#         """
#         self.settings = settings
#         self.components = components
#
#         self.state = State()
#         self.state._state_manager = self
#         self.state.settings = settings
#         self.started = False
#
#     async def startup(self) -> None:
#         """Последовательно вызовет startup каждого компонента передавая в него state.
#         В state можно писать, из него можно читать. Изначально в state только settings."""
#         for component in self.components:
#             self.state = await component.startup(self.state)
#
#         self.started = True
#
#     async def shutdown(self) -> None:
#         """Вызовет shutdown каждого компонента в обратном порядке."""
#         if self.started:
#             for component in reversed(self.components):
#                 await component.shutdown()
#
#
# class FastAPIStateManager(StateManager):
#     """Манагер стейта для FastAPI."""
#
#     def set_fastapi_startup_hook(self, app: "FastAPI") -> None:
#         """Проставит startup hook FastAPI приложению,
#         в котором вызовет у себя startup и перезапишет FastAPI.state на свой state"""
#
#         async def hook() -> None:
#             await self.startup()
#
#             # this is dangerous
#             app.state = self.state  # type: ignore
#
#         app.router.add_event_handler("startup", hook)
#
#     def set_fastapi_shutdown_hook(self, app: "FastAPI") -> None:
#         """Проставит shutdown hook FastAPI приложению, в котором вызовет у себя shutdown"""
#
#         async def hook() -> None:
#             await self.shutdown()
#
#         app.router.add_event_handler("shutdown", hook)


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
        """Последовательно вызовет startup каждого компонента передавая в него state.
        В state можно писать, из него можно читать. Изначально в state только settings."""
        for component in self.components:
            self.state = await component.startup(self.state)

        self.started = True

    async def shutdown(self) -> None:
        """Вызовет shutdown каждого компонента в обратном порядке."""
        if self.started:
            for component in reversed(self.components):
                await component.shutdown()

    def set_fastapi_startup_hook(self, app: "FastAPI") -> None:
        """Проставит startup hook FastAPI приложению,
        в котором вызовет у себя startup и перезапишет FastAPI.state на свой state"""

        async def hook() -> None:
            await self.startup()

            # this is dangerous
            app.state = self.state  # type: ignore

        app.router.add_event_handler("startup", hook)

    def set_fastapi_shutdown_hook(self, app: "FastAPI") -> None:
        """Проставит shutdown hook FastAPI приложению, в котором вызовет у себя shutdown"""

        async def hook() -> None:
            await self.shutdown()

        app.router.add_event_handler("shutdown", hook)


class AIOPostgresComponent(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.engine: Optional[Engine] = None
        self._exit_stack = contextlib.AsyncExitStack()

    async def startup(self, state: State) -> State:
        settings = Settings()

        self.engine = await self._create_engine(settings)
        state.db = self.engine
        return state

    # async def healthcheck(self) -> None:
    #     async with self._get_connection() as conn:
    #         await conn.execute("select 1;")
    #
    async def shutdown(self) -> None:
        await self._exit_stack.aclose()
    #
    # @asynccontextmanager
    # async def _get_connection(self) -> SAConnection:
    #     assert self.engine is not None, "Engine is not initialized"
    #     async with self.engine.acquire() as connection:
    #         yield connection

    async def _create_engine(self, settings: Settings) -> Engine:
        return await self._exit_stack.enter_async_context(
            create_engine(
                dsn=settings.POSTGRESQL_DATABASE_URI,
                maxsize=settings.POSTGRESQL_POOL_SIZE,
                timeout=settings.POSTGRESQL_CONNECTION_TIMEOUT
            )
        )