from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table, desc, select
from psycopg2.errors import UniqueViolation

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.account_tables import account_table,account_admitted_users_table
from sweet_cash.types.accounts_types import (
    AccountModel,
    CreateAccountModel,
    UpdateAccountModel,
    AccountsAdmittedUsersModel
)
from sweet_cash.errors import APIValueNotFound, APIConflict


class AccountsRepository(BaseRepository):
    account_table: Table = account_table
    account_admitted_users_table: Table = account_admitted_users_table

    async def create_account(self, user_id: int, item: CreateAccountModel) -> AccountModel:
        insert_body = item.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["user_id"] = user_id
        create_query = self.account_table.insert().values(insert_body).returning(*self.account_table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return AccountModel(**row)
    
    async def update_account(
            self, user_id: int, account_id: int, item: UpdateAccountModel
    ) -> Union[AccountModel, APIValueNotFound]:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "name": item.name,
            "description": item.description,
            "is_blocked": item.is_blocked
        }
        update_query = (
            self.account_table.update()
            .where(
                (self.account_table.c.id == account_id)
                & (self.account_table.c.user_id == user_id)
            )
            .values(**update_value)
            .returning(*self.account_table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        if not row:
            return APIValueNotFound()
        return AccountModel(**row)

    async def get_user_account_by_id(self, user_id: int, account_id: int) -> Union[AccountModel, APIValueNotFound]:
        query = (
            self.account_table.select()
                .where(
                    (self.account_table.c.id == account_id)
                    & (self.account_table.c.user_id == user_id)
                )
                .order_by(desc(self.account_table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if not row:
            return APIValueNotFound()
        return AccountModel(**row)
    
    async def get_accounts_by_ids(self, account_ids: List[int], with_blocked: bool = False) -> List[AccountModel]:
        query = (
            select(
                self.account_table,
            )
            .where(
                self.account_table.c.id.in_(account_ids)
            )
        )
        if not with_blocked:
            query = query.where(self.account_table.c.is_blocked == False)

        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountModel(**row) for row in rows]

    async def get_available_accounts_by_user_id(
            self,
            user_id: int,
            with_blocked: bool = False
    )-> List[AccountModel]:
        account_owner_query = select(self.account_table).where(
            self.account_table.c.user_id == user_id
        )
        if not with_blocked:
            account_owner_query = account_owner_query.where(self.account_table.c.is_blocked == False)

        admitted_accounts_query = select(self.account_table).join(
            self.account_admitted_users_table,
            self.account_table.c.id == self.account_admitted_users_table.c.account_id
        ).where(
            self.account_admitted_users_table.c.user_id == user_id
        )
        if not with_blocked:
            admitted_accounts_query = admitted_accounts_query.where(self.account_table.c.is_blocked == False)

        combined_query = account_owner_query.union(admitted_accounts_query).order_by(self.account_table.c.id)

        r = await self.conn.execute(combined_query)
        rows = await r.fetchall()
        return [AccountModel(**row) for row in rows]

    async def get_available_accounts_by_ids(
            self,
            user_id: int,
            account_ids: List[int],
            with_blocked: bool = False
    )-> List[AccountModel]:
        account_owner_query = (
            select(
                self.account_table
            )
            .where(
                (self.account_table.c.id.in_(account_ids))
                & (self.account_table.c.user_id == user_id)
            )
        )
        if not with_blocked:
            account_owner_query = account_owner_query.where(self.account_table.c.is_blocked == False)

        admitted_accounts_query = (
            select(
                self.account_table
            )
            .join(
                self.account_admitted_users_table,
                self.account_table.c.id == self.account_admitted_users_table.c.account_id
            )
            .where(
                (self.account_admitted_users_table.c.user_id == user_id)
                & (self.account_admitted_users_table.c.account_id.in_(account_ids))
            )
        )
        if not with_blocked:
            admitted_accounts_query = admitted_accounts_query.where(self.account_table.c.is_blocked == False)

        combined_query = account_owner_query.union(admitted_accounts_query).order_by(self.account_table.c.id)

        r = await self.conn.execute(combined_query)
        rows = await r.fetchall()
        return [AccountModel(**row) for row in rows]

    async def create_admitted_user(
            self, user_id: int, account_id: int
    ) -> Union[AccountsAdmittedUsersModel, APIConflict]:
        insert_body = dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["account_id"] = account_id
        insert_body["user_id"] = user_id
        create_query = (self.account_admitted_users_table.insert().values(insert_body)
                        .returning(*self.account_admitted_users_table.c))
        try:
            r_ = await self.conn.execute(create_query)
            row = await r_.fetchone()
            return AccountsAdmittedUsersModel(**row)
        except UniqueViolation:
            return APIConflict()

    async def delete_admitted_user(
            self, user_id: int, account_id: int
    ) -> Union[AccountsAdmittedUsersModel, APIValueNotFound]:
        delete_query = (
            self.account_admitted_users_table.delete()
            .where(
                (self.account_admitted_users_table.c.user_id == user_id)
                & (self.account_admitted_users_table.c.account_id == account_id)
            )
            .returning(*self.account_admitted_users_table.c))
        r = await self.conn.execute(delete_query)
        row = await r.fetchone()
        if not row:
            return APIValueNotFound()
        return AccountsAdmittedUsersModel(**row)

    async def get_admitted_users_by_account_ids(self, account_ids: List[int]) -> List[AccountsAdmittedUsersModel]:
        query = (
            self.account_admitted_users_table.select()
            .where(self.account_admitted_users_table.c.account_id.in_(account_ids))
            .order_by(self.account_admitted_users_table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [AccountsAdmittedUsersModel(**row) for row in rows]


