from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table, desc

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.accounts_admitted_users import account_admitted_users_table
from sweet_cash.types.accounts_admitted_users_types import AccountsAdmittedUsersModel


class AccountsAdmittedUsersRepository(BaseRepository):
    table: Table = account_admitted_users_table

    async def create_admitted_user(self, account_id: int, user_id: int) -> AccountsAdmittedUsersModel:
        insert_body = dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["account_id"] = account_id
        insert_body["user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return AccountsAdmittedUsersModel(**row)

    async def get_by_id(self, item_id: int) -> Union[AccountsAdmittedUsersModel, None]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id == item_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            return None
        return AccountsAdmittedUsersModel(**row)
    
    async def get_by_account_id_and_user_id(self, account_id: int, user_id: int) -> Union[AccountsAdmittedUsersModel, None]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.account_id == account_id)
                    & (self.table.c.user_id == user_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            return None
        return AccountsAdmittedUsersModel(**row)
    
    async def get_by_user_id(self, user_id: int)-> List[AccountsAdmittedUsersModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountsAdmittedUsersModel(**row) for row in rows]
    
    async def get_by_account_id(self, account_id: int)-> List[AccountsAdmittedUsersModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.account_id == account_id)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountsAdmittedUsersModel(**row) for row in rows]

    async def delete_admitted_user(self, item_id: int) -> AccountsAdmittedUsersModel:
        delete_query = self.table.delete().where(self.table.c.id == item_id).returning(*self.table.c)
        r = await self.conn.execute(delete_query)
        row = await r.fetchone()
        return AccountsAdmittedUsersModel(**row)
