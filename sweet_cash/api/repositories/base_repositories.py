from contextlib import asynccontextmanager
from typing import AsyncGenerator, Union

from aiopg.sa import Engine, SAConnection, create_engine
from sqlalchemy import Table
from sqlalchemy.sql import ClauseElement
from settings import Settings

QUEY_TYPE = Union[ClauseElement, str]


class BaseRepository:
    engine: Engine
    table: Table

    def __init__(self):
        # self.pg_engine = pg_engine
        self.conn = None

    @asynccontextmanager
    async def _get_connection(self) -> AsyncGenerator[None, None]:
        async with create_engine(user=Settings.POSTGRESQL_USER,
                                 database=Settings.POSTGRESQL_DATABASE,
                                 host=Settings.POSTGRESQL_SERVER,
                                 password=Settings.POSTGRESQL_PASSWORD) as engine:
            async with engine.acquire() as conn:
                self.conn = conn
                yield
                self.conn = None

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        async with self._get_connection():
            assert isinstance(self.conn, SAConnection)
            async with self.conn.begin():
                yield
