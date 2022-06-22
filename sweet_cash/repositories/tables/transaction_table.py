
from sqlalchemy import Column, Integer, MetaData, Table, Text, types, Sequence, Enum, Float

from sweet_cash.types.transactions_types import TransactionType

metadata = MetaData()

transaction_table = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("number", Integer, Sequence('transaction_num', start=1, increment=1)),
    Column("user_id", Integer, index=True, nullable=False),
    Column("event_id", Integer, index=True, nullable=False),
    Column("type", Enum(TransactionType), nullable=False),
    Column("category_id", Integer, nullable=False),
    Column("amount", Float, nullable=False),
    Column("transaction_date", types.DateTime(timezone=False), nullable=False),
    Column("description", Text, nullable=True),
    Column("receipt_id", Integer, nullable=True),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)
