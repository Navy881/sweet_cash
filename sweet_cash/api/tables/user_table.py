
from sqlalchemy import Column, Integer, MetaData, Table, Text, types, Boolean

user_metadata = MetaData()

user_table = Table(
    "users",
    user_metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("name", Text, nullable=False),
    Column("email", Text, nullable=False, unique=True),
    Column("phone", Text, nullable=False),
    Column("password", Text, nullable=False),
    Column("confirmed", Boolean, nullable=True, default=False),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)
