
from datetime import datetime

from sqlalchemy import Table

from api.repositories.base_repositories import BaseRepository
from api.tables.event_table import event_table
from api.types.events_types import EventModel, CreateEventModel


class EventsRepository(BaseRepository):
    table: Table = event_table

    # async def search_one(self, wave_id: int, search_datetime: datetime) -> BindingModel:
    #     query = (
    #         self.table.select()
    #             .where(
    #             (self.table.c.wave_id == wave_id)
    #             & between(
    #                 search_datetime,
    #                 self.table.c.start_date,
    #                 self.table.c.end_date,
    #             )
    #         )
    #             .order_by(desc(self.table.c.created_at))
    #     )
    #     r_ = await self._execute(query)
    #     row = await r_.fetchone()
    #     if row is None:
    #         raise NotFoundError
    #     return BindingModel(**row)
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

    async def create_event(self, item: CreateEventModel) -> EventModel:
        insert_body = item.dict()
        insert_body["created_at"] = datetime.utcnow()
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        # r_ = await self._execute(create_query)
        row = await r_.fetchone()
        return EventModel(**row)

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