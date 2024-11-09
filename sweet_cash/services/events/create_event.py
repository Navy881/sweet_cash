import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.create_event_participant_for_owner import CreateEventParticipantForOwner

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel, CreateEventModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel


logger = logging.getLogger(name="events")


class CreateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 create_event_participant_for_owner: CreateEventParticipantForOwner,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.create_event_participant_for_owner = create_event_participant_for_owner
        self.events_repository = events_repository

    async def __call__(self, event: CreateEventModel) -> EventModel:
        # Create event
        async with self.events_repository.transaction():
            event_model = await self.events_repository.create_event(event)

        participant: EventsParticipantsModel = await self.create_event_participant_for_owner(event_model.id)
        event_model.participants = [participant]
        
        return event_model
