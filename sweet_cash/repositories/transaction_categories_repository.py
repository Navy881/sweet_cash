from sqlalchemy import Table
from datetime import datetime
from typing import List

from sweet_cash.repositories.base_repositories import BaseRepository
from sweet_cash.repositories.tables.transaction_category_table import transaction_category_table
from sweet_cash.types.transaction_categories_types import TransactionCategoryModel, CreateTransactionCategoryModel
from sweet_cash.errors import APIValueNotFound


class TransactionCategoriesRepository(BaseRepository):
    table: Table = transaction_category_table

    async def get_transaction_category_by_id(self, transaction_category_id: int) -> TransactionCategoryModel:
        query = (
            self.table.select()
                .where(
                (self.table.c.id == transaction_category_id)
                & (self.table.c.deleted.is_(None))
                )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            raise APIValueNotFound(f'Transaction category {transaction_category_id} not found')
        return TransactionCategoryModel(**row)

    async def create_transaction_category(self, transaction_category: CreateTransactionCategoryModel) -> \
            TransactionCategoryModel:
        insert_body = transaction_category.dict()
        insert_body["created_at"] = datetime.utcnow()
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return TransactionCategoryModel(**row)

    async def update_transaction_category(self, transaction_category_id: int,
                                          transaction_category: CreateTransactionCategoryModel) -> \
            TransactionCategoryModel:
        update_value = {
            "updated_at": datetime.utcnow(),
            "name": transaction_category.name,
            "parent_category_id": transaction_category.parent_category_id,
            "description": transaction_category.description
        }
        update_query = (
            self.table.update().where(self.table.c.id == transaction_category_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return TransactionCategoryModel(**row)

    async def delete_transaction_category(self, transaction_category_id: int) -> TransactionCategoryModel:
        update_value = {
            "deleted": datetime.utcnow()
        }
        update_query = (
            self.table.update().where(self.table.c.id == transaction_category_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return TransactionCategoryModel(**row)

    async def get_transaction_categories(self) -> List[TransactionCategoryModel]:
        query = (
            self.table.select()
                .where(self.table.c.deleted.is_(None))
                .order_by(self.table.c.id.desc())
        )
        r_ = await self.conn.execute(query)
        rows = await r_.fetchall()
        return [TransactionCategoryModel(**row) for row in rows]
