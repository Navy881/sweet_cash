
from datetime import datetime
from sqlalchemy import Column, Integer, MetaData, Table, Text, types, Boolean

token_metadata = MetaData()

token_table = Table(
    "tokens",
    token_metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("refresh_token", Text, nullable=False),
    Column("token", Text, nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("login_method", Text, nullable=True),
    Column("expire_at", types.DateTime(timezone=False), nullable=False)
)
