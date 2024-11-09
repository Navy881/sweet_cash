import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="events")


class GetEventById(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_event_participants_by_event: GetEventParticipantsByEvent,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_event_participants_by_event = get_event_participants_by_event
        self.events_repository = events_repository

    async def __call__(self, event_id: int) -> EventModel:
        user_roles = await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)
        if len(user_roles) == 0:
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        # Get event
        async with self.events_repository.transaction():
            event = await self.events_repository.get_by_id(event_id=event_id)
            if event is None:
                raise APIValueNotFound(f'Event {event_id} not found')

            event.participants = await self.get_event_participants_by_event(event.id)

        return event
