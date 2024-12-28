import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events import EnrichEvents

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import (
    EventModel,
    CreateEventModel,
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    EventParticipantRole
)


logger = logging.getLogger(name="events")


class CreateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_events: EnrichEvents,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.enrich_events = enrich_events
        self.events_repository = events_repository

    async def __call__(self, event: CreateEventModel) -> EventModel:
        # Create event
        async with self.events_repository.transaction():
            event_model = await self.events_repository.create_event(event)

            event_participant: CreateEventsParticipantsModel = CreateEventsParticipantsModel(
                user_id=self.user_id,
                role=EventParticipantRole.MANAGER
            )
            event_participant: EventsParticipantsModel = await self.events_repository. \
                create_events_owner_participant(event_id=event_model.id, event_participant=event_participant)
            event_model.participants.append(event_participant)

            await self.enrich_events([event_model])
            return event_model
