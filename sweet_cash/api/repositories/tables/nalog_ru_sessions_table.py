
from sqlalchemy import Column, Integer, MetaData, Table, Text, types


metadata = MetaData()

nalog_ru_sessions_table = Table(
    "nalog_ru_sessions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("user_id", Integer, index=True, nullable=False),
    Column("sessionId", Text, nullable=False),
    Column("refresh_token", Text, nullable=True)
)
