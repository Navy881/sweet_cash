
from sqlalchemy import Column, Integer, MetaData, Table, types, String, JSON

metadata = MetaData()

receipt_table = Table(
    "receipts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("user_id", Integer, index=True, nullable=False),
    Column("external_id", String, index=True, nullable=False),
    Column("data", JSON, nullable=True),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)