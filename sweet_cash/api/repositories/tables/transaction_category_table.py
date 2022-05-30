
from sqlalchemy import Column, Integer, MetaData, Table, types, String

metadata = MetaData()

transaction_category_table = Table(
    "transactions_categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("name", String, index=True, nullable=False),
    Column("parent_category_id", Integer, nullable=True),
    Column("description", String, nullable=True),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)
