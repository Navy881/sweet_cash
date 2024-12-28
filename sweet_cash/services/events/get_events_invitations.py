import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events import EnrichEvents

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel


logger = logging.getLogger(name="events")


class GetEventsInvitations(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_events: EnrichEvents,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.enrich_events = enrich_events
        self.events_repository = events_repository

    async def __call__(self) -> List[EventModel]:
        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository.get_invitations_to_events(user_id=self.user_id)
            await self.enrich_events(events)
            return events
