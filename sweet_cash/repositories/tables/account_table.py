
from sqlalchemy import Column, Integer, MetaData, Table, types, Boolean, Text


metadata = MetaData()

account_table = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("name", Text, nullable=False),
    Column("description", Text, nullable=True),
    Column("user_id", Integer, index=True, nullable=False),
    Column("is_blocked", Boolean, nullable=True, default=False)
)
