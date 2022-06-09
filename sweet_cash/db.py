
from settings import Settings

from sqlalchemy import create_engine

engine = create_engine(Settings.POSTGRESQL_DATABASE_URI, pool_pre_ping=True)
