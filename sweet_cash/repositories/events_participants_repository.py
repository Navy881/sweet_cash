from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table

from sweet_cash.repositories.base_repository import BaseRepository

from sweet_cash.repositories.tables.event_participants_table import event_participants_table

from sweet_cash.types.events_participants_types import (
    EventsParticipantsModel,
    EventParticipantRole,
    CreateEventsParticipantsModel,
    UpdateEventsParticipantsModel
)


class EventsParticipantsRepository(BaseRepository):
    table: Table = event_participants_table

    async def create_events_participant(self, event_id: int,
                                        event_participant: CreateEventsParticipantsModel) -> EventsParticipantsModel:
        insert_body = event_participant.dict()
        insert_body['event_id'] = event_id
        insert_body["created_at"] = datetime.now(timezone.utc)
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        # r_ = await self._execute(create_query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def create_events_participant_for_owner(
            self, event_id: int,
            event_participant: CreateEventsParticipantsModel
    ) -> EventsParticipantsModel:
        insert_body = event_participant.dict()
        insert_body['event_id'] = event_id
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["accepted"] = True
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def accept_events_participant(self, events_participant_id: int) -> EventsParticipantsModel:
        query = (
            self.table.update()
                .where(self.table.c.id == events_participant_id)
                .values(accepted=True)
        ).returning(*self.table.c)
        r = await self.conn.execute(query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def check_exist_events_participant_by_role(self, user_id: int,
                                                     event_id: int,
                                                     role: str,
                                                     accepted: bool = True) -> bool:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
                & (self.table.c.event_id == event_id)
                & (self.table.c.role == role)
                & (self.table.c.accepted == accepted)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            return False
        return True

    async def get_events_participant_by_id(self, event_participant_id: int) -> Union[EventsParticipantsModel, None]:
        query = (
            self.table.select()
                .where(self.table.c.id == event_participant_id)
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            return None
        return EventsParticipantsModel(**row)

    async def get_events_participants_by_user(
            self, user_id: int, accepted: bool = True
    ) -> List[EventsParticipantsModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
                & (self.table.c.accepted == accepted)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participants_by_event(
            self, event_id: int, accepted: bool = True
    ) -> List[EventsParticipantsModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.event_id == event_id)
                & (self.table.c.accepted == accepted)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participants_by_user_and_roles(self, user_id: int,
                                                        roles: List[EventParticipantRole],
                                                        accepted: bool = True) -> List[EventsParticipantsModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
                & (self.table.c.role.in_(roles))
                & (self.table.c.accepted == accepted)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participants_by_user_and_event(self, user_id: int,
                                                        event_id: int,
                                                        accepted: bool = True) -> List[EventsParticipantsModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
                & (self.table.c.event_id == event_id)
                & (self.table.c.accepted == accepted)
            )
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def update_events_participant(self, event_participant_id: int,
                                        event_participant: UpdateEventsParticipantsModel) -> EventsParticipantsModel:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "role": event_participant.role,
        }
        update_query = (
            self.table.update().where(self.table.c.id == event_participant_id).values(**update_value)
                .returning(*self.table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def delete_events_participants(self, events_participant_ids: List[int]) -> List[EventsParticipantsModel]:
        delete_query = self.table.delete().where(self.table.c.id.in_(events_participant_ids)).returning(*self.table.c)
        r = await self.conn.execute(delete_query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]
