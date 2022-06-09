
from datetime import datetime
from typing import List, Any

from sqlalchemy import Table

from api.repositories.base_repositories import BaseRepository
from api.repositories.tables.transaction_table import transaction_table
from api.types.transactions_types import CreateTransactionModel, TransactionModel
from api.errors import APIValueNotFound


class TransactionsRepository(BaseRepository):
    table: Table = transaction_table

    async def create_transaction(self, user_id: int, transaction: CreateTransactionModel) -> TransactionModel:
        insert_body = transaction.dict()
        insert_body["created_at"] = datetime.utcnow()
        insert_body["user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return TransactionModel(**row)

    async def get_transaction_by_id(self, transaction_id: int) -> TransactionModel:
        query = (
            self.table.select()
                .where(self.table.c.id == transaction_id)
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            raise APIValueNotFound(f'Transaction {transaction_id} not found')
        return TransactionModel(**row)

    async def update_transaction(self, transaction_id: int, transaction: CreateTransactionModel) -> TransactionModel:
        update_value = {
            "updated_at": datetime.utcnow(),
            "type": transaction.type,
            "category_id": transaction.category_id,
            "amount": transaction.amount,
            "transaction_date": transaction.transaction_date,
            "description": transaction.description
        }
        update_query = (
            self.table.update().where(self.table.c.id == transaction_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return TransactionModel(**row)

    async def get_transactions(self, transaction_ids: List[int]) -> List[TransactionModel]:
        query = (
            self.table.select()
                .where(self.table.c.id.in_(transaction_ids))
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [TransactionModel(**row) for row in rows]

    async def get_transactions_page(self, event_id: int,
                                    start: str,
                                    end: str,
                                    user_id: int = None,
                                    limit: int = 100,
                                    offset: int = 0) -> List[TransactionModel]:

        query = (
            self.table.select()
                .where(
                (self.table.c.event_id == event_id)
                & (self.table.c.transaction_date >= start)
                & (self.table.c.transaction_date <= end)
            )
        )

        if user_id is not None:
            query = query.where(self.table.c.user_id == user_id)

        query = query.order_by(self.table.c.transaction_date)
        query = query.limit(limit)
        query = query.offset(offset)

        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [TransactionModel(**row) for row in rows]

    async def delete_transaction(self, transaction_id: int) -> TransactionModel:
        delete_query = self.table.delete().where(self.table.c.id == transaction_id).returning(*self.table.c)
        r = await self.conn.execute(delete_query)
        row = await r.fetchone()
        return TransactionModel(**row)
