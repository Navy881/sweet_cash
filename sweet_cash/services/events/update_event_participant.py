import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.types.events_participants_types import (
    EventsParticipantsModel,
    UpdateEventsParticipantsModel,
    EventParticipantRole
)
from sweet_cash.errors import APIConflict, APIValueNotFound


logger = logging.getLogger(name="events")


class UpdateEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_participant_id: int,
                       event_participants: UpdateEventsParticipantsModel) -> EventsParticipantsModel:
        async with self.events_participants_repository.transaction():
            # Checking participant exist
            event_participant: EventsParticipantsModel = await self.events_participants_repository. \
                get_events_participant_by_id(event_participant_id)

            event_id: int = event_participant.event_id

            # Checking that requests user is user from requests
            if self.user_id == event_participant.user_id:
                raise APIConflict(f'User {self.user_id} is trying to update his participant {event_participant_id}')

            # Checking that requests user is the event manager
            if not await self.events_participants_repository. \
                    check_exist_events_participant_by_role(user_id=self.user_id,
                                                           event_id=event_id,
                                                           role=EventParticipantRole('Manager')):
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

            return await self.events_participants_repository. \
                update_events_participant(event_participant_id=event_participant_id,
                                          event_participant=event_participants)
