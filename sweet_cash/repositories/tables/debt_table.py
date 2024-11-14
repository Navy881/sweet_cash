from sqlalchemy import Column, Integer, MetaData, Table, types, Text, Enum, Float

from sweet_cash.types.debts_types import DebtType


metadata = MetaData()

debt_table = Table(
    "debts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("user_id", Integer, index=True, nullable=False),
    Column("type", Enum(DebtType), nullable=False),
    Column("amount", Float, nullable=False),
    Column("currency", Text, nullable=False),
    Column("percentage_rate", Integer, nullable=False),
    Column("due_date", types.DateTime(timezone=False), nullable=False),
    Column("debtor", Text, nullable=True),
    Column("creditor", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("closed_at", types.DateTime(timezone=False), nullable=True)
)
