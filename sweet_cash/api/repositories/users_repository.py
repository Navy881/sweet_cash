
from datetime import datetime
import bcrypt

from sqlalchemy import Table, desc

from sweet_cash.api.repositories.base_repositories import BaseRepository
from sweet_cash.api.repositories.tables.user_table import user_table
from sweet_cash.api.types.users_types import UserModel, CreateUserModel, RegisterUserModel
from sweet_cash.api.errors import APIValueNotFound, APIAuthError


class UsersRepository(BaseRepository):
    table: Table = user_table

    async def check_exist_by_email(self, email: str) -> bool:
        query = (
            self.table.select()
                .where(
                    (self.table.c.email == email)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            return False
        return True

    async def get_by_email(self, email: str, confirmed: bool = True) -> UserModel:
        query = (
            self.table.select()
                .where(
                    (self.table.c.email == email)
                    & (self.table.c.confirmed == confirmed)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            raise APIValueNotFound(f'User with login "{email}" not found')
        return UserModel(**row)

    async def get_by_id(self, user_id: int) -> UserModel:
        query = (
            self.table.select()
                .where(
                    (self.table.c.id == user_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound(f'User {user_id} not found')
        return UserModel(**row)

    #
    # async def find_bindings(self, wave_id: int, end_date: datetime, start_date: datetime) -> list[BindingModel]:
    #     query = self.table.select().where(
    #         (self.table.c.wave_id == wave_id)
    #         & (self.table.c.end_date >= start_date)
    #         & (self.table.c.start_date <= end_date)
    #     )
    #     r_ = await self._execute(query)
    #     rows = await r_.fetchall()
    #     return [BindingModel(**row) for row in rows]
    #
    # async def get(self, wave_id: int, limit: int = 100, offset: int = 0) -> list[BindingModel]:
    #     query = (
    #         self.table.select()
    #             .where(self.table.c.wave_id == wave_id)
    #             .order_by(self.table.c.start_date)
    #             .limit(limit)
    #             .offset(offset)
    #     )
    #     r_ = await self._execute(query)
    #     rows = await r_.fetchall()
    #     return [BindingModel(**row) for row in rows]

    async def create_user(self, item: RegisterUserModel) -> CreateUserModel:
        insert_body = item.dict()
        insert_body["created_at"] = datetime.utcnow()
        insert_body["password"] = bcrypt.hashpw(item.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return CreateUserModel(**row)

    async def confirm_user(self, user_id: int) -> UserModel:
        update_value = {
            "confirmed": True,
        }
        update_query = (
            self.table.update().where(self.table.c.id == user_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return UserModel(**row)

    # async def delete(self, wave_id: int, binding_id: int) -> BindingModel:
    #     delete_query = (
    #         self.table.delete()
    #             .where((self.table.c.wave_id == wave_id) & (self.table.c.id == binding_id))
    #             .returning(*self.table.c)
    #     )
    #     r_ = await self._execute(delete_query)
    #     row = await r_.fetchone()
    #     if row is None:
    #         raise NotFoundError
    #     return BindingModel(**row)
    #
    # async def delete_bindings_by_wave_id(self, wave_id: int) -> list[BindingModel]:
    #     delete_query = self.table.delete().where(self.table.c.wave_id == wave_id).returning(*self.table.c)
    #     r_ = await self._execute(delete_query)
    #     rows = await r_.fetchall()
    #     return [BindingModel(**row) for row in rows]

    @staticmethod
    def check_password(password: str, given_password: str):
        result = bcrypt.checkpw(given_password.encode("utf-8"), password.encode("utf-8"))
        if not result:
            raise APIAuthError('Wrong password')
