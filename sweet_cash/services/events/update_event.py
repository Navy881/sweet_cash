import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events import EnrichEvents

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import (
    EventModel,
    CreateEventModel,
    EventParticipantRole,
    EventsParticipantsModel
)

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="events")


class UpdateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_events: EnrichEvents,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.enrich_events = enrich_events
        self.events_repository = events_repository

    async def __call__(self, event_id: int, event: CreateEventModel) -> EventModel:
        async with self.events_repository.transaction():
            user_events_participants: List[EventsParticipantsModel] = await self.events_repository. \
                get_events_participants_by_user_and_event(event_id=event_id, user_id=self.user_id, accepted=True)

            if EventParticipantRole.MANAGER not in [participant.role for participant in user_events_participants]:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

            event: EventModel = await self.events_repository.update_event(event_id=event_id, event=event)

            # Addition events_participants for event
            event.participants = await self.events_repository.get_events_participants_by_event(event_id)

            await self.enrich_events([event])
            return event
