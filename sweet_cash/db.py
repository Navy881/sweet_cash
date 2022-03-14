# import databases
import asyncio

from aiopg.sa import create_engine, Engine
# from sqlalchemy import MetaData
# from sqlalchemy.orm import sessionmaker
#
from settings import Settings

# loop = asyncio.get_event_loop()
# engine = loop.run_until_complete(create_engine(user=Settings.POSTGRESQL_USER,
#                                                database=Settings.POSTGRESQL_DATABASE,
#                                                host=Settings.POSTGRESQL_SERVER,
#                                                password=Settings.POSTGRESQL_PASSWORD))

#
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# metadata = MetaData()
#
# database = databases.Database(Settings.POSTGRESQL_DATABASE_URI)
#
# # from flask_sqlalchemy import SQLAlchemy
# #
# # db = SQLAlchemy()

from typing import Any
#
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import as_declarative
# from sqlalchemy.orm import sessionmaker
#
# from settings import Settings
#
#
engine = create_engine(Settings.POSTGRESQL_DATABASE_URI, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @as_declarative()
# class Base:
#     id: Any
