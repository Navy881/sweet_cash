from datetime import datetime, timezone
import bcrypt
from typing import Union, List

from sqlalchemy import Table, desc

from sweet_cash.repositories.base_repository import BaseRepository
from sweet_cash.repositories.tables.user_table import user_table
from sweet_cash.types.users_types import UserModel, RegisterUserResponseModel, RegisterUserModel


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

    async def get_by_email(self, email: str) -> Union[UserModel, None]:
        query = (
            self.table.select()
                .where(
                    (self.table.c.email == email)
                )
                .order_by(desc(self.table.c.created_at))
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            return None
        return UserModel(**row)

    async def get_by_id(self, user_id: int) -> Union[UserModel, None]:
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
            return None
        return UserModel(**row)

    async def create_user(self, item: RegisterUserModel) -> RegisterUserResponseModel:
        insert_body = item.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["password"] = bcrypt.hashpw(item.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return RegisterUserResponseModel(**row)

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
    
    async def update_user(self, user: RegisterUserModel) -> UserModel:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "password": bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        }
        update_query = (
            self.table.update().where(self.table.c.email == user.email).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return UserModel(**row)

    async def get_by_ids(self, user_ids: List[int]) -> List[UserModel]:
        query = (
            self.table.select()
            .where(self.table.c.id.in_(user_ids))
            .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [UserModel(**row) for row in rows]