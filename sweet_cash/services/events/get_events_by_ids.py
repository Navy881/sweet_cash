import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_by_user import GetEventParticipantsByUser
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel

from sweet_cash.errors import APIValueNotFound

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="events")


class GetEventsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_by_user: GetEventParticipantsByUser,
                 get_event_participants_by_event: GetEventParticipantsByEvent,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_by_user = get_event_participants_by_user
        self.get_event_participants_by_event = get_event_participants_by_event
        self.events_repository = events_repository

    async def __call__(self, events_ids: str) -> List[EventModel]:
        events_ids: List[id] = ids2list(events_ids)

        user_participants: List[EventsParticipantsModel] = \
            await self.get_event_participants_by_user(self.user_id, accepted=True)

        available_events_ids: List[int] = [user_participant.event_id
                                           for user_participant in user_participants]

        if not set(events_ids).issubset(set(available_events_ids)):
            unavailable_events_ids: set = set(events_ids) - set(available_events_ids)
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {unavailable_events_ids}')

        # Get events
        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository.get_events(event_ids=events_ids)

            # Addition events_participants for events
            for event in events:
                event.participants = await self.get_event_participants_by_event(event.id)

        return events
