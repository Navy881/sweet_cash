import logging
from typing import List

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository

from sweet_cash.types.events_participants_types import EventsParticipantsModel, EventParticipantRole

logger = logging.getLogger(name="events")


class GetEventParticipantsRolesForUser(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int, user_id: int) -> List[EventParticipantRole]:
        roles: List[EventParticipantRole]

        async with self.events_participants_repository.transaction():
            user_events_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_user_and_event(event_id=event_id, user_id=user_id, accepted=True)

            roles = [user_events_participant.role for user_events_participant in user_events_participants]

        return roles