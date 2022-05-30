from datetime import datetime
from typing import List

from sqlalchemy import Table

from api.repositories.base_repositories import BaseRepository
from api.repositories.tables.event_participants_table import event_participants_table
from api.types.events_participants_types import (
    EventsParticipantsModel,
    EventParticipantRole,
    CreateEventsParticipantsModel,
    UpdateEventsParticipantsModel
)
from api.errors import APIValueNotFound


class EventsParticipantsRepository(BaseRepository):
    table: Table = event_participants_table

    async def create_events_participant(self, event_id: int,
                                        event_participant: CreateEventsParticipantsModel) -> EventsParticipantsModel:
        insert_body = event_participant.dict()
        insert_body['event_id'] = event_id
        insert_body["created_at"] = datetime.utcnow()
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r_ = await self.conn.execute(create_query)
        # r_ = await self._execute(create_query)
        row = await r_.fetchone()
        return EventsParticipantsModel(**row)

    async def accept_events_participant(self, events_participant_id: int) -> EventsParticipantsModel:
        query = (
            self.table.update()
                .where(self.table.c.id == events_participant_id)
                .values(accepted=True)
        ).returning(*self.table.c)
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        return EventsParticipantsModel(**row)

    async def get_events_participants_by_event_id(self, event_id: int) -> List[EventsParticipantsModel]:
        query = (
            self.table.select()
                .where(self.table.c.event_id == event_id)
                .order_by(self.table.c.id)
        )
        r_ = await self.conn.execute(query)
        rows = await r_.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participant_by_role(self, user_id: int,
                                             event_id: int,
                                             role: EventParticipantRole,
                                             accepted: bool = True) -> EventsParticipantsModel:
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
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        return EventsParticipantsModel(**row)

    async def get_events_participant_by_id(self, event_participant_id: int) -> EventsParticipantsModel:
        query = (
            self.table.select()
                .where(self.table.c.id == event_participant_id)
                .order_by(self.table.c.id)
        )
        r_ = await self.conn.execute(query)
        row = await r_.fetchone()
        if row is None:
            raise APIValueNotFound(f'Event participant {event_participant_id} not found')
        return EventsParticipantsModel(**row)

    async def get_events_participants(self, user_id: int, accepted: bool = True) -> List[EventsParticipantsModel]:
        query = (
            self.table.select()
                .where(
                (self.table.c.user_id == user_id)
                & (self.table.c.accepted == accepted)
            )
                .order_by(self.table.c.id)
        )
        r_ = await self.conn.execute(query)
        rows = await r_.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participants_with_role(self, user_id: int,
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
        r_ = await self.conn.execute(query)
        rows = await r_.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participants_by_user_id(self, user_id: int,
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
        r_ = await self.conn.execute(query)
        rows = await r_.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def update_events_participant(self, event_participant_id: int,
                                        event_participant: UpdateEventsParticipantsModel) -> EventsParticipantsModel:
        update_value = {
            "updated_at": datetime.utcnow(),
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
        r_ = await self.conn.execute(delete_query)
        rows = await r_.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]
