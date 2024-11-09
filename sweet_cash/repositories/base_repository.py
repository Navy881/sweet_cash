from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiopg.sa import Engine, SAConnection
from sqlalchemy import Table


class BaseRepository:
    engine: Engine
    table: Table

    def __init__(self, pg_engine: Engine):
        self.pg_engine = pg_engine
        self.conn = None

    @asynccontextmanager
    async def _get_connection(self) -> AsyncGenerator[None, None]:
        async with self.pg_engine.acquire() as conn:
            self.conn = conn
            yield
            self.conn = None

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        async with self._get_connection():
            assert isinstance(self.conn, SAConnection)
            async with self.conn.begin():
                yield
