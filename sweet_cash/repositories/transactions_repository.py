from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table, or_

from sweet_cash.repositories.base_repository import BaseRepository

from sweet_cash.repositories.tables.transaction_table import transaction_table

from sweet_cash.types.transactions_types import (
    CreateTransactionModel,
    TransactionModel,
    UpdateTransactionModel,
    TransactionType
)


class TransactionsRepository(BaseRepository):
    table: Table = transaction_table

    async def create_transaction(self, user_id: int, transaction: CreateTransactionModel) -> TransactionModel:
        insert_body = transaction.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return TransactionModel(**row)

    async def get_transaction_by_id(self, transaction_id: int) -> Union[TransactionModel, None]:
        query = (
            self.table.select()
                .where(self.table.c.id == transaction_id)
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            return None
        return TransactionModel(**row)

    async def update_transaction(self, transaction_id: int, transaction: UpdateTransactionModel) -> TransactionModel:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "type": transaction.type,
            "category_id": transaction.category_id,
            "amount": transaction.amount,
            "transfer_fee": transaction.transfer_fee,
            "transaction_date": transaction.transaction_date,
            "description": transaction.description,
            "source_account_id": transaction.source_account_id,
            "target_account_id": transaction.target_account_id
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

        query = query.order_by(self.table.c.transaction_date.desc())
        query = query.limit(limit)
        query = query.offset(offset)

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

        query = query.order_by(self.table.c.transaction_date.desc())
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

    async def get_transactions_by_account_id(self, account_id: int) -> List[TransactionModel]:
        query = (
            self.table.select()
                .where(
                    or_(
                        self.table.c.source_account_id == account_id,
                        self.table.c.target_account_id == account_id
                    )
                )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [TransactionModel(**row) for row in rows]

    async def get_transactions_by_event_and_type(
            self,
            event_id: int,
            start: str,
            end: str,
            transaction_type: TransactionType,
            category_ids: List[int] = None
    ) -> List[TransactionModel]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.event_id == event_id)
                    & (self.table.c.transaction_date >= start)
                    & (self.table.c.transaction_date <= end)
                    & (self.table.c.type == TransactionType(transaction_type))
                )
                .order_by(self.table.c.id)
        )

        if category_ids is not None:
            query = query.where(self.table.c.category_id.in_(category_ids))

        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [TransactionModel(**row) for row in rows]

    async def get_transactions_by_account_id_page(self, account_id: int,
                                                  start: str,
                                                  end: str,
                                                  limit: int = 100,
                                                  offset: int = 0) -> List[TransactionModel]:

        query = (
            self.table.select()
                .where(
                or_(
                    self.table.c.source_account_id == account_id,
                    self.table.c.target_account_id == account_id
                )
                & (self.table.c.transaction_date >= start)
                & (self.table.c.transaction_date <= end)
            )
        )

        query = query.order_by(self.table.c.transaction_date.desc())
        query = query.limit(limit)
        query = query.offset(offset)

        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [TransactionModel(**row) for row in rows]