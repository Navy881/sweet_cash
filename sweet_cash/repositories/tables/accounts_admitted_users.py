
from sqlalchemy import Column, Integer, MetaData, Table, types


metadata = MetaData()

account_admitted_users_table = Table(
    "accounts_admitted_users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("account_id", Integer, index=True, nullable=False),
    Column("user_id", Integer, index=True, nullable=False)
)
