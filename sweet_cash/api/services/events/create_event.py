import logging

from api.services.base_service import BaseService
from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_types import EventModel, CreateEventModel
from api.types.events_participants_types import CreateEventsParticipantsModel, EventParticipantRole

logger = logging.getLogger(name="events")


class CreateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event: CreateEventModel) -> EventModel:
        async with self.events_repository.transaction():
            # Create event
            event = await self.events_repository.create_event(event)

        async with self.events_participants_repository.transaction():
            # Create events participant
            event_participant: CreateEventsParticipantsModel = CreateEventsParticipantsModel(
                user_id=self.user_id,
                role=EventParticipantRole.MANAGER
            )

            events_participant = await self.events_participants_repository.\
                create_events_participant(event_id=event.id, event_participant=event_participant)

            # Accept events participant
            await self.events_participants_repository.accept_events_participant(
                events_participant_id=events_participant.id)

            # Addition events_participants for event
            event.participants = await self.events_participants_repository.\
                get_events_participants_by_event_id(event_ids=[event.id])
        return event
