import logging
from typing import List

from sweet_cash.api.services.base_service import BaseService
from sweet_cash.api.repositories.events_repository import EventsRepository
from sweet_cash.api.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.api.types.events_types import EventModel
from sweet_cash.api.types.events_participants_types import EventsParticipantsModel
from sweet_cash.api.utils import ids2list
from sweet_cash.api.errors import APIValueNotFound


logger = logging.getLogger(name="events")


class GetEvents(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self, events_ids: str) -> List[EventModel]:
        events_ids: List[id] = ids2list(events_ids)

        async with self.events_participants_repository.transaction():
            # Get users events participants
            user_events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants(user_id=self.user_id)

            available_events_ids: List[int] = [events_participant.event_id
                                               for events_participant in user_events_participants]

            if not set(events_ids).issubset(set(available_events_ids)):
                unavailable_events_ids: set = set(events_ids) - set(available_events_ids)
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {unavailable_events_ids}')

            # Get events_participants for event
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_by_event_id(event_ids=events_ids)

        async with self.events_repository.transaction():
            # Get events
            events: List[EventModel] = await self.events_repository.get_events(event_ids=events_ids)

            # Addition events_participants for events
            for event in events:
                event.participants = [events_participant for events_participant in events_participants
                                      if events_participant.event_id == event.id]

            return events
