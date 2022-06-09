import logging

from api.services.base_service import BaseService
from api.repositories.users_repository import UsersRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_participants_types import (
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    EventParticipantRole
)
from api.errors import APIValueNotFound, APIParamError

logger = logging.getLogger(name="events")


class CreateEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 users_repository: UsersRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.users_repository = users_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int,
                       event_participants: CreateEventsParticipantsModel) -> EventsParticipantsModel:
        user_id: int = event_participants.user_id
        role: EventParticipantRole = event_participants.role

        async with self.users_repository.transaction():
            # Checking user from requests exist
            await self.users_repository.get_by_id(user_id)

        async with self.events_participants_repository.transaction():
            # Checking that requests user is the event manager
            if not await self.events_participants_repository. \
                    check_exist_events_participant_by_role(user_id=self.user_id,
                                                           event_id=event_id,
                                                           role=EventParticipantRole('Manager')):
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

            # Checking that user is not events participant
            if await self.events_participants_repository. \
                    check_exist_events_participant_by_role(user_id=user_id,
                                                           event_id=event_id,
                                                           role=EventParticipantRole(role)):
                raise APIParamError(f'Participant for {user_id} already exist in event {event_id}')

            return await self.events_participants_repository. \
                create_events_participant(event_id=event_id, event_participant=event_participants)
