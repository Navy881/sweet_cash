import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository

from sweet_cash.types.events_participants_types import (
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    EventParticipantRole
)


logger = logging.getLogger(name="events")


class CreateEventParticipantForOwner(BaseService):
    def __init__(self, user_id: int,
                 get_user_by_id: GetUserById,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int) -> EventsParticipantsModel:
        async with self.events_participants_repository.transaction():
            event_participant: CreateEventsParticipantsModel = CreateEventsParticipantsModel(
                user_id=self.user_id,
                role=EventParticipantRole.MANAGER
            )
            event_participant: EventsParticipantsModel = await self.events_participants_repository. \
                create_events_participant_for_owner(event_id=event_id, event_participant=event_participant)
            
            event_participant.user = await self.get_user_by_id(self.user_id)

        return event_participant