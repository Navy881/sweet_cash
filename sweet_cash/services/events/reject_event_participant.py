
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.types.events_participants_types import EventsParticipantsModel


logger = logging.getLogger(name="events")


class RejectEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int) -> List[EventsParticipantsModel]:
        async with self.events_participants_repository.transaction():
            # Get not accepted events participants
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id, accepted=False)

            return await self.events_participants_repository.\
                delete_events_participants([event_participant.id for event_participant in event_participants])
