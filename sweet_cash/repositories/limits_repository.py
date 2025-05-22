from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table

from sweet_cash.repositories.base_repository import BaseRepository

from sweet_cash.repositories.tables.limit_table import limit_table

from sweet_cash.types.limits_types import LimitModel, CreateLimitModel, UpdateLimitModel


class LimitsRepository(BaseRepository):
    table: Table = limit_table

    async def create_limit(self, user_id: int, limit: CreateLimitModel) -> LimitModel:
        insert_body = limit.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["created_by_user_id"] = user_id
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return LimitModel(**row)

    async def get_limit_by_id(self, limit_id: int) -> Union[LimitModel, None]:
        query = (
            self.table.select()
                .where(self.table.c.id == limit_id)
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            return None
        return LimitModel(**row)

    async def update_limit(self, limit_id: int, limit: UpdateLimitModel) -> LimitModel:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "start": limit.start,
            "end": limit.end,
            "type": limit.type,
            "category_id": limit.category_id,
            "amount": limit.amount
        }
        update_query = (
            self.table.update().where(self.table.c.id == limit_id).values(**update_value).returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return LimitModel(**row)

    async def get_limits_by_ids(self, limit_ids: List[int]) -> List[LimitModel]:
        query = (
            self.table.select()
                .where(self.table.c.id.in_(limit_ids))
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [LimitModel(**row) for row in rows]

    async def get_limits_page(self, event_id: int,
                                    limit: int = 100,
                                    offset: int = 0) -> List[LimitModel]:

        query = (
            self.table.select()
                .where(
                (self.table.c.event_id == event_id)
            )
        )

        query = query.order_by(self.table.c.created_at.desc())
        query = query.limit(limit)
        query = query.offset(offset)

        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [LimitModel(**row) for row in rows]

    async def delete_limit(self, limit_id: int) -> LimitModel:
        delete_query = self.table.delete().where(self.table.c.id == limit_id).returning(*self.table.c)
        r = await self.conn.execute(delete_query)
        row = await r.fetchone()
        return LimitModel(**row)
