import logging
from typing import List

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventsParticipantsModel, EventParticipantRole

logger = logging.getLogger(name="events")


class GetEventParticipantsRolesForUser(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository

    async def __call__(self, event_id: int, user_id: int) -> List[EventParticipantRole]:
        roles: List[EventParticipantRole]

        async with self.events_repository.transaction():
            user_events_participants: List[EventsParticipantsModel] = await self.events_repository. \
                get_events_participants_by_user_and_event(event_id=event_id, user_id=user_id, accepted=True)

            roles = [user_events_participant.role for user_events_participant in user_events_participants]

        return roles