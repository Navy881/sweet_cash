from typing import AsyncGenerator, List

import pytest
from aiopg.sa import Engine, SAConnection, create_engine
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.ddl import CreateTable

from sweet_cash.app import create_app
from sweet_cash.settings import Settings
from sweet_cash.db import engine

from sweet_cash.repositories.tables import (
    user_table,
    token_table,
    event_table,
    event_participants_table,
    transaction_table,
    transaction_category_table,
    receipt_table,
    nalog_ru_sessions_table
)


# TABLES = [
#     user_table.user_table,
#     token_table.token_table,
#     event_table.event_table,
#     event_participants_table.event_participants_table,
#     transaction_table.transaction_table,
#     transaction_category_table.transaction_category_table,
#     receipt_table.receipt_table,
#     nalog_ru_sessions_table.nalog_ru_sessions_table
# ]


@pytest.fixture
def test_app() -> FastAPI:
    settings = Settings()
    return create_app(settings=settings)


@pytest.fixture
async def client(test_app: FastAPI) -> AsyncGenerator[TestClient, None]:
    async with TestClient(test_app) as client:
        yield client


async def drop_tables(connection: SAConnection):
    await connection.execute("DROP SCHEMA public CASCADE;")
    await connection.execute("CREATE SCHEMA public;")
    await connection.execute("CREATE EXTENSION IF NOT EXISTS hstore SCHEMA public;")


def create_all_tables(engine):
    user_table.metadata.create_all(bind=engine)
    token_table.metadata.create_all(bind=engine)
    event_table.metadata.create_all(bind=engine)
    event_participants_table.metadata.create_all(bind=engine)
    transaction_table.metadata.create_all(bind=engine)
    transaction_category_table.metadata.create_all(bind=engine)
    receipt_table.metadata.create_all(bind=engine)
    nalog_ru_sessions_table.metadata.create_all(bind=engine)


# async def create_tables(connection: SAConnection, tables: List[Table]):
#     for table in tables:
#         ddl = str(CreateTable(table).compile(dialect=postgresql.dialect()))
#         print(ddl)
#         await connection.execute(ddl)


@pytest.fixture
async def connection(db_engine: Engine) -> AsyncGenerator[SAConnection, None]:
    async with db_engine.acquire() as connection:
        yield connection


@pytest.fixture(autouse=True)
async def db_engine(test_settings: Settings) -> AsyncGenerator[Engine, None]:
    async with create_engine(test_settings.POSTGRESQL_DATABASE_URI) as db_engine:
        async with db_engine.acquire() as connection:
            await drop_tables(connection)
            # await create_tables(connection, TABLES)
            sql_alchemy_engine = engine(test_settings.POSTGRESQL_DATABASE_URI)
            create_all_tables(sql_alchemy_engine)

        yield db_engine


@pytest.fixture
def test_settings() -> Settings:
    return Settings()


###############################


# @pytest.fixture(scope="session")
# def postgres_container():
#     with PostgresContainer() as container:
#         yield container
#
#
# @pytest.fixture(scope="session")
# def redis_container():
#     with RedisContainer() as container:
#         yield container
#
#
# @pytest.fixture
# def test_settings(postgres_container: PostgresContainer, redis_container: RedisContainer) -> Settings:
#     return Settings(
#         compilation_url="http://compilation_url",
#         compilation_timeout=1,
#         meta_url="http://meta_url",
#         meta_timeout=1,
#         postgres_dsn=postgres_container.get_connection_url().replace("+psycopg2", ""),
#         redis_dsn=f"redis://{redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}",
#         buttons=[
#             ButtonModel(
#                 name="lifestyle_news",
#                 title="Новости",
#                 subcategories=[
#                     SubButtonMode(name="sport", title="Спорт", image_src=""),
#                     SubButtonMode(name="playbill", title="Афиша", image_src=""),
#                 ],
#             )
#         ],
#     )
#
#
#
#
# @pytest.fixture(autouse=True)
# def clear_cache(redis_container: RedisContainer):
#     redis_container.get_client().flushdb()
#
# @pytest.fixture
# def mock_session():
#     with aioresponses() as mock:
#         yield mock
