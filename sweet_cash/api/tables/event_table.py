
from sqlalchemy import Column, Integer, MetaData, Table, Text, types
#from db import metadata

event_metadata = MetaData()

event_table = Table(
    "events",
    event_metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("name", Text, nullable=False),
    Column("description", Text, nullable=True),
    Column("start", types.DateTime(timezone=False), nullable=True),
    Column("end", types.DateTime(timezone=False), nullable=True),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)
