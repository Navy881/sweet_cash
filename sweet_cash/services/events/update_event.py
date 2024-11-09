import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel, CreateEventModel
from sweet_cash.types.events_participants_types import EventParticipantRole

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="events")


class UpdateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_event_participants_by_event: GetEventParticipantsByEvent,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_event_participants_by_event = get_event_participants_by_event
        self.events_repository = events_repository

    async def __call__(self, event_id: int, event: CreateEventModel) -> EventModel:
        user_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

        if EventParticipantRole.MANAGER not in user_roles:
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        # Update event
        async with self.events_repository.transaction():
            event: EventModel = await self.events_repository.update_event(event_id=event_id, event=event)

            # Addition events_participants for event
            event.participants = await self.get_event_participants_by_event(event.id)

        return event
