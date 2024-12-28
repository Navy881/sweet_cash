import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events_participants import EnrichEventsParticipants

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventsParticipantsModel


logger = logging.getLogger(name="events")


class ConfirmEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 enrich_events_participants: EnrichEventsParticipants,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.enrich_events_participants = enrich_events_participants
        self.events_repository = events_repository

    async def __call__(self, event_id: int) -> List[EventsParticipantsModel]:
        async with self.events_repository.transaction():
            # Get not accepted events participants
            event_participants: List[EventsParticipantsModel] = await self.events_repository.\
                get_events_participants_by_user_and_event(user_id=self.user_id, event_id=event_id, accepted=False)

            event_participants = await self.events_repository. \
                accept_events_participants([participant.id for participant in event_participants])

            await self.enrich_events_participants(event_participants)
        return event_participants
