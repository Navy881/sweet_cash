
from sqlalchemy import Column, Integer, MetaData, Table, types, Enum, Float

from sweet_cash.types.transactions_types import TransactionType


metadata = MetaData()

limit_table = Table(
    "limits",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("created_by_user_id", Integer, nullable=False),
    Column("start", types.DateTime(timezone=False), nullable=False),
    Column("end", types.DateTime(timezone=False), nullable=False),
    Column("event_id", Integer, index=True, nullable=False),
    Column("type", Enum(TransactionType), nullable=False),
    Column("category_id", Integer, nullable=True),
    Column("amount", Float, nullable=False),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)
