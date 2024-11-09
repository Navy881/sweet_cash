import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_by_user import GetEventParticipantsByUser
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel


logger = logging.getLogger(name="events")


class GetEventsInvitations(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_by_user: GetEventParticipantsByUser,
                 get_event_participants_by_event: GetEventParticipantsByEvent,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_by_user = get_event_participants_by_user
        self.get_event_participants_by_event = get_event_participants_by_event
        self.events_repository = events_repository

    async def __call__(self) -> List[EventModel]:

        events_participants: List[EventsParticipantsModel] = \
            await self.get_event_participants_by_user(user_id=self.user_id, accepted=False)

        event_ids = [events_participant.event_id for events_participant in events_participants]

        # Get events
        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository.get_events(event_ids=event_ids)

            # Addition events_participants for events
            for event in events:
                event.participants = await self.get_event_participants_by_event(event.id)

        return events
