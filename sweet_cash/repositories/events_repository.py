from datetime import datetime, timezone
from typing import List, Union
from sqlalchemy import Table, select, func, and_, exists

from sweet_cash.repositories.base_repository import BaseRepository

from sweet_cash.repositories.tables.event_tables import event_table, event_participants_table

from sweet_cash.types.events_types import (
    EventModel,
    CreateEventModel,
    CreateEventsParticipantsModel,
    UpdateEventsParticipantsModel,
    EventsParticipantsModel,
    EventParticipantRole
)


class EventsRepository(BaseRepository):
    event_table: Table = event_table
    event_participants_table: Table = event_participants_table

    async def create_event(self, event: CreateEventModel) -> EventModel:
        insert_body = event.dict()
        insert_body["created_at"] = datetime.now(timezone.utc)
        create_query = self.event_table.insert().values(insert_body).returning(*self.event_table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return EventModel(
            **row,
            participants=[]
        )

    async def get_available_events_by_ids(self, user_id: int, event_ids: List[int]) -> List[EventModel]:
        # Подзапрос для participants
        participants_subquery = (
            select(
                self.event_participants_table.c.event_id,
                func.json_agg(
                    func.row_to_json(self.event_participants_table.table_valued())
                ).label("participants")
            )
            .group_by(self.event_participants_table.c.event_id)
            .subquery()
        )

        # Основной запрос
        query = (
            select(
                self.event_table,
                participants_subquery.c.participants
            )
            .outerjoin(
                participants_subquery,
                self.event_table.c.id == participants_subquery.c.event_id
            )
            .where(
                and_(
                    self.event_table.c.id.in_(event_ids),
                    exists(
                        select(1)
                        .where(
                            and_(
                                self.event_table.c.id == self.event_participants_table.c.event_id,
                                self.event_participants_table.c.user_id == user_id,
                                self.event_participants_table.c.accepted == True
                            )
                        )
                    )
                )
            )
        )

        r = await self.conn.execute(query)
        rows = await r.fetchall()

        result: List[EventModel] = []
        for row in rows:
            row_dict = dict(row.items())
            participants_data = row_dict.pop("participants", [])
            participants = [
                EventsParticipantsModel(**{**participant, "role": EventParticipantRole[participant["role"]]})
                for participant in participants_data
            ]
            result.append(
                EventModel(
                    **row_dict,
                    participants=participants
                )
            )
        return result

    async def get_available_events_by_roles(self, user_id: int, roles: List[EventParticipantRole]) -> List[EventModel]:
        # Подзапрос для participants
        participants_subquery = (
            select(
                self.event_participants_table.c.event_id,
                func.json_agg(
                    func.row_to_json(self.event_participants_table.table_valued())
                ).label("participants")
            )
            .group_by(self.event_participants_table.c.event_id)
            .subquery()
        )

        # Основной запрос
        query = (
            select(
                self.event_table,
                participants_subquery.c.participants
            )
            .outerjoin(
                participants_subquery,
                self.event_table.c.id == participants_subquery.c.event_id
            )
            .where(
                exists(
                    select(1)
                    .where(
                        and_(
                            self.event_table.c.id == self.event_participants_table.c.event_id,
                            self.event_participants_table.c.user_id == user_id,
                            self.event_participants_table.c.accepted == True,
                            self.event_participants_table.c.role.in_(roles)
                        )
                    )
                )
            )
        )

        r = await self.conn.execute(query)
        rows = await r.fetchall()

        result: List[EventModel] = []
        for row in rows:
            row_dict = dict(row.items())
            participants_data = row_dict.pop("participants", [])
            participants = [
                EventsParticipantsModel(**{**participant, "role": EventParticipantRole[participant["role"]]})
                for participant in participants_data
            ]
            result.append(
                EventModel(
                    **row_dict,
                    participants=participants
                )
            )
        return result

    async def get_invitations_to_events(self, user_id: int) -> List[EventModel]:
        # Подзапрос для participants
        participants_subquery = (
            select(
                self.event_participants_table.c.event_id,
                func.json_agg(
                    func.row_to_json(self.event_participants_table.table_valued())
                ).label("participants")
            )
            .group_by(self.event_participants_table.c.event_id)
            .subquery()
        )

        # Основной запрос
        query = (
            select(
                self.event_table,
                participants_subquery.c.participants
            )
            .outerjoin(
                participants_subquery,
                self.event_table.c.id == participants_subquery.c.event_id
            )
            .where(
                exists(
                    select(1)
                    .where(
                        and_(
                            self.event_table.c.id == self.event_participants_table.c.event_id,
                            self.event_participants_table.c.user_id == user_id,
                            self.event_participants_table.c.accepted == False
                        )
                    )
                )
            )
        )

        r = await self.conn.execute(query)
        rows = await r.fetchall()

        result: List[EventModel] = []
        for row in rows:
            row_dict = dict(row.items())
            participants_data = row_dict.pop("participants", [])
            participants = [
                EventsParticipantsModel(**{**participant, "role": EventParticipantRole[participant["role"]]})
                for participant in participants_data
            ]
            result.append(
                EventModel(
                    **row_dict,
                    participants=participants
                )
            )
        return result

    async def update_event(self, event_id: int, event: CreateEventModel) -> EventModel:
        update_value = {
            "updated_at": datetime.now(timezone.utc),
            "name": event.name,
            "start": event.start,
            "end": event.end,
            "description": event.description
        }
        update_query = (
            self.event_table.update()
            .where(
                self.event_table.c.id == event_id
            )
            .values(**update_value)
            .returning(*self.event_table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return EventModel(**row)

    async def create_events_participant(self, event_id: int,
                                        event_participant: CreateEventsParticipantsModel) -> EventsParticipantsModel:
        insert_body = event_participant.dict()
        insert_body['event_id'] = event_id
        insert_body["created_at"] = datetime.now(timezone.utc)
        create_query = (
            self.event_participants_table.insert()
            .values(insert_body)
            .returning(*self.event_participants_table.c)
        )
        r = await self.conn.execute(create_query)
        # r_ = await self._execute(create_query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def create_events_owner_participant(
            self, event_id: int,
            event_participant: CreateEventsParticipantsModel
    ) -> EventsParticipantsModel:
        insert_body = event_participant.dict()
        insert_body['event_id'] = event_id
        insert_body["created_at"] = datetime.now(timezone.utc)
        insert_body["accepted"] = True
        create_query = (
            self.event_participants_table.insert()
            .values(insert_body)
            .returning(*self.event_participants_table.c)
        )
        r = await self.conn.execute(create_query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def accept_events_participants(self, events_participant_ids: List[int]) -> List[EventsParticipantsModel]:
        query = (
            self.event_participants_table.update()
                .where(self.event_participants_table.c.id.in_(events_participant_ids))
                .values(accepted=True)
        ).returning(*self.event_participants_table.c)
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participant_by_id(self, event_participant_id: int) -> Union[EventsParticipantsModel, None]:
        query = (
            self.event_participants_table.select()
                .where(self.event_participants_table.c.id == event_participant_id)
                .order_by(self.event_participants_table.c.id)
        )
        r = await self.conn.execute(query)
        row = await r.fetchone()
        if row is None:
            return None
        return EventsParticipantsModel(**row)

    async def get_events_participants_by_event(self, event_id: int) -> List[EventsParticipantsModel]:
        query = (
            self.event_participants_table.select()
            .where(
                self.event_participants_table.c.event_id == event_id
            )
            .order_by(self.event_participants_table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]

    async def get_events_participants_by_user_and_event(self, user_id: int,
                                                        event_id: int,
                                                        accepted: bool = True) -> List[EventsParticipantsModel]:
        query = (
            self.event_participants_table.select()
                .where(
                (self.event_participants_table.c.user_id == user_id)
                & (self.event_participants_table.c.event_id == event_id)
                & (self.event_participants_table.c.accepted == accepted)
            )
            .order_by(self.event_participants_table.c.id)
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
            self.event_participants_table.update()
            .where(
                self.event_participants_table.c.id == event_participant_id
            )
            .values(**update_value)
            .returning(*self.event_participants_table.c)
        )
        r = await self.conn.execute(update_query)
        row = await r.fetchone()
        return EventsParticipantsModel(**row)

    async def delete_events_participants(self, events_participant_ids: List[int]) -> List[EventsParticipantsModel]:
        delete_query = (
            self.event_participants_table.delete()
            .where(
                self.event_participants_table.c.id.in_(events_participant_ids)
            )
            .returning(*self.event_participants_table.c)
        )
        r = await self.conn.execute(delete_query)
        rows = await r.fetchall()
        return [EventsParticipantsModel(**row) for row in rows]