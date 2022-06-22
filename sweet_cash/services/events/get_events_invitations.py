
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.events_repository import EventsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.types.events_types import EventModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel


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
            # Get users events participants
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants(user_id=self.user_id, accepted=False)

            available_events_ids = [events_participant.event_id for events_participant in events_participants]

            # Get events_participants for event
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_by_event_id(event_ids=available_events_ids)

        async with self.events_repository.transaction():
            # Get events
            events: List[EventModel] = await self.events_repository.get_events(event_ids=available_events_ids)

            # Addition events_participants for events
            for event in events:
                event.participants = [events_participant for events_participant in events_participants
                                      if events_participant.event_id == event.id]

            return events
