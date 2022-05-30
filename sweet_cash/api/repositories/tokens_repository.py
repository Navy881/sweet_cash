
from datetime import datetime, timedelta
import uuid
from typing import Optional

import jwt
from sqlalchemy import Table, desc

from api.repositories.base_repositories import BaseRepository
from api.repositories.tables.token_table import token_table
from api.types.users_types import TokenModel, RefreshTokenModel
from api.errors import APIValueNotFound
from settings import Settings


class TokenRepository(BaseRepository):
    table: Table = token_table

    async def get_access_token(self, refresh_token: str) -> TokenModel:
        query = (
            self.table.select()
                .where(
                (self.table.c.refresh_token == refresh_token)
            )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound()
        return TokenModel(**row)

    async def get_token_by_user(self, user_id: int) -> TokenModel:
        query = (
            self.table.select()
                .where(
                    (self.table.c.user_id == user_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound(f'User {user_id} is not authorized')
        return TokenModel(**row)

    async def get_user_by_token(self, token: str) -> TokenModel:
        query = (
            self.table.select()
                .where(
                    (self.table.c.token == token)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound('User not found')
        return TokenModel(**row)

    async def check_exist_token_by_user(self, user_id: int) -> bool:
        query = (
            self.table.select()
                .where(
                    (self.table.c.user_id == user_id)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            return False
        return True

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

    async def create_access_token(self, item: dict) -> RefreshTokenModel:
        expires_delta = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        insert_body = item
        insert_body["created_at"] = datetime.utcnow()
        insert_body["refresh_token"] = self._create_refresh_token()
        insert_body["token"] = self._create_access_token(data={"sub": insert_body["user_id"]},
                                                         expires_delta=expires_delta)
        insert_body["expire_at"] = datetime.utcnow() + expires_delta
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return RefreshTokenModel(**row)

    async def update_access_token(self, refresh_token: str, item: dict) -> RefreshTokenModel:
        expires_delta = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        update_body = item
        update_body["updated_at"] = datetime.utcnow()
        update_body["refresh_token"] = self._create_refresh_token()
        update_body["token"] = self._create_access_token(data={"sub": update_body["user_id"]},
                                                         expires_delta=expires_delta)
        update_body["expire_at"] = datetime.utcnow() + expires_delta
        update_query = (
            self.table.update()
                .where(self.table.c.refresh_token == refresh_token)
                .values(**update_body)
                .returning(*self.table.c)
        )
        r_ = await self.conn.execute(update_query)
        row = await r_.fetchone()
        return RefreshTokenModel(**row)

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
    def _create_refresh_token():
        refresh_token = str(uuid.uuid4())
        return refresh_token

    @staticmethod
    def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        return encoded_jwt
