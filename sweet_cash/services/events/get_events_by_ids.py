import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events import EnrichEvents

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="events")


class GetEventsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_events: EnrichEvents,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.enrich_events = enrich_events
        self.events_repository = events_repository

    async def __call__(self, events_ids: str) -> List[EventModel]:
        events_ids: List[id] = ids2list(events_ids)

        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository \
                .get_available_events_by_ids(user_id=self.user_id, event_ids=events_ids)

            await self.enrich_events(events)
            return events

class GetEventsByIdsInternal(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository

    async def __call__(self, events_ids: List[int]) -> Dict[int, EventModel]:
        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository \
                .get_available_events_by_ids(user_id=self.user_id, event_ids=events_ids)

            return {event.id: event for event in events}
