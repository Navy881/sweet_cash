
from datetime import datetime

from sqlalchemy import Table, desc

from api.repositories.base_repositories import BaseRepository
from api.repositories.tables.nalog_ru_sessions_table import nalog_ru_sessions_table
from api.types.nalog_ru_types import NalogRuSessionModel
from api.errors import APIValueNotFound


class NalogRuSessionsRepository(BaseRepository):
    table: Table = nalog_ru_sessions_table

    async def create_nalog_ru_session(self, user_id: int, nalog_ru_session: NalogRuSessionModel) -> NalogRuSessionModel:
        insert_body = nalog_ru_session.dict()
        insert_body["created_at"] = datetime.utcnow()
        insert_body["user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        row = await r_.fetchone()
        return NalogRuSessionModel(**row)

    async def check_exist_by_user_id(self, user_id: int) -> bool:
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

    async def update_nalog_ru_session(self, user_id: int, nalog_ru_session: NalogRuSessionModel) -> NalogRuSessionModel:
        update_value = {
            "updated_at": datetime.utcnow(),
            "sessionId": nalog_ru_session.sessionId,
            "refresh_token": nalog_ru_session.refresh_token
        }
        update_query = (
            self.table.update().where(self.table.c.user_id == user_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return NalogRuSessionModel(**row)

    async def get_session_by_user(self, user_id: int) -> NalogRuSessionModel:
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
            raise APIValueNotFound(f'User {user_id} is not registered in NalogRU')
        return NalogRuSessionModel(**row)
