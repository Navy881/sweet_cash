from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.debt_table import debt_table

from sweet_cash.types.debts_types import DebtModel, CreateDebtModel

from sweet_cash.errors import APIValueNotFound


class DebtsRepository(BaseRepository):
    table: Table = debt_table

    async def create_debt(self, user_id: int, item: CreateDebtModel) -> DebtModel:
        insert_body = item.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return DebtModel(**row)
    
    async def update_debt(self, user_id: int, debt_id: int, item: CreateDebtModel) -> Union[DebtModel, APIValueNotFound]:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "type": item.type,
            "amount": item.amount,
            "currency": item.currency,
            "percentage_rate": item.percentage_rate,
            "due_date": item.due_date,
            "debtor": item.debtor,
            "creditor": item.creditor,
            "description": item.description,
            "closed_at": item.closed_at
        }

        update_query = (
            self.table.update().where(
                (self.table.c.id == debt_id)
                & (self.table.c.user_id == user_id)
            )
            .values(**update_value)
            .returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        if not row:
            return APIValueNotFound()
        return DebtModel(**row)
    
    async def get_user_debts_by_ids(self, debt_ids: List[int], user_id: int) -> List[DebtModel]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id.in_(debt_ids))
                    & (self.table.c.user_id == user_id)
                )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [DebtModel(**row) for row in rows]

    async def get_debts_by_user_id(self, user_id: int)-> List[DebtModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [DebtModel(**row) for row in rows]
