
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Optional, Union, List
from sqlalchemy import Table, desc

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.token_table import token_table
from sweet_cash.types.users_types import TokenModel, RefreshTokenModel
from sweet_cash.errors import APIValueNotFound
from sweet_cash.settings import Settings


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
            raise APIValueNotFound('Token not found')
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

    async def get_user_by_token(self, token: str) -> Union[TokenModel, None]:
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
            return None
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
    
    async def get_tokens_by_user(self, user_id: int) -> List[TokenModel]:
        query = (
            self.table.select()
                .where(self.table.c.user_id == user_id)
                .order_by(self.table.c.expire_at)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [TokenModel(**row) for row in rows]

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
