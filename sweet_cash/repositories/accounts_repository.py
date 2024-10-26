
from datetime import datetime, timezone
from typing import List
from sqlalchemy import Table, desc

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.account_table import account_table
from sweet_cash.types.accounts_types import AccountModel, CreateAccountModel, UpdateAccountModel
from sweet_cash.errors import APIValueNotFound


class AccountsRepository(BaseRepository):
    table: Table = account_table

    async def create_account(self, user_id: int, item: CreateAccountModel) -> AccountModel:
        insert_body = item.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return AccountModel(**row)
    
    async def update_account(self, account_id: int, item: UpdateAccountModel) -> AccountModel:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "name": item.name,
            "description": item.description,
            "is_blocked": item.is_blocked
        }
        update_query = (
            self.table.update().where(self.table.c.id == account_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return AccountModel(**row)
    
    async def get_by_id(self, account_id: int) -> AccountModel:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id == account_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound(f'Account {account_id} not found')
        return AccountModel(**row)
    
    async def get_user_account_by_id(self, account_id: int, user_id: int) -> AccountModel:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id == account_id)
                    & (self.table.c.user_id == user_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound(f'Account {account_id} not found')
        return AccountModel(**row)
    
    async def get_by_ids(self, account_ids: List[int]) -> List[AccountModel]:
        query = (
            self.table.select()
                .where(self.table.c.id.in_(account_ids))
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountModel(**row) for row in rows]
    
    async def get_user_accounts_by_ids(self, account_ids: List[int], user_id: int) -> List[AccountModel]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id.in_(account_ids))
                    & (self.table.c.user_id == user_id)
                )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountModel(**row) for row in rows]

    async def get_by_user_id(self, user_id: int, with_blocked = False)-> List[AccountModel]:
        if with_blocked:
            query = (
                self.table.select()
                    .where(
                    (self.table.c.user_id == user_id)
                )
                    .order_by(self.table.c.id)
            )
        else:
            query = (
                self.table.select()
                    .where(
                    (self.table.c.user_id == user_id)
                    & (self.table.c.is_blocked == False)
                )
                    .order_by(self.table.c.id)
            )

        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountModel(**row) for row in rows]
