
import logging
from typing import List

from sweet_cash.api.services.base_service import BaseService
from sweet_cash.api.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.api.types.events_participants_types import EventsParticipantsModel


logger = logging.getLogger(name="events")


class ConfirmEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int) -> List[EventsParticipantsModel]:
        async with self.events_participants_repository.transaction():
            # Get not accepted events participants
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id, accepted=False)

            result: List = []

            for event_participant in event_participants:
                result.append(await self.events_participants_repository.accept_events_participant(event_participant.id))

            return result
