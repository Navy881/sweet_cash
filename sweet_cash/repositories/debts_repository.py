from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table, desc

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.debt_table import debt_table
from sweet_cash.types.debts_types import DebtModel, CreateDebtModel


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
    
    async def update_debt(self, debt_id: int, item: CreateDebtModel) -> DebtModel:
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
            self.table.update().where(self.table.c.id == debt_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return DebtModel(**row)
    
    async def get_by_id(self, debt_id: int) -> Union[DebtModel, None]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id == debt_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            return None
        return DebtModel(**row)
    
    async def get_user_debt_by_id(self, debt_id: int, user_id: int) -> Union[DebtModel, None]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id == debt_id)
                    & (self.table.c.user_id == user_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            return None
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

    async def get_by_user_id(self, user_id: int)-> List[DebtModel]:
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
