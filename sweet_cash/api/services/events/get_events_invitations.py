
import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_types import EventModel
from api.types.events_participants_types import EventsParticipantsModel


logger = logging.getLogger(name="events")


class GetEventsInvitations(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self) -> List[EventModel]:
        async with self.events_participants_repository.transaction():
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants(user_id=self.user_id, accepted=False)

        available_events_ids = [events_participant.event_id for events_participant in events_participants]

        async with self.events_repository.transaction():
            return await self.events_repository.get_events(event_ids=available_events_ids)
