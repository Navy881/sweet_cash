import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_types import EventModel
from api.types.events_participants_types import EventsParticipantsModel
from api.api import ids2list
from api.errors import APIValueNotFound

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
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants(user_id=self.user_id)

            available_events_ids: List[int] = [events_participant.event_id for events_participant in events_participants]

            if not set(events_ids).issubset(set(available_events_ids)):
                unavailable_events_ids: set = set(events_ids) - set(available_events_ids)
                raise APIValueNotFound(f'User {self.user_id} not associated with the events {unavailable_events_ids}')

        async with self.events_repository.transaction():
            return await self.events_repository.get_events(event_ids=events_ids)

# import logging
#
# from api.services.events.get_event_participant import GetEventParticipant
# from api.models.event import EventModel
# from api.api import ids2list
# import api.errors as error
#
# logger = logging.getLogger(name="events")
#
#
# class GetEvents(object):
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> [EventModel]:
#         user_id = kwargs.get("user_id")
#         event_ids = ids2list(kwargs.get("event_ids"))
#
#         events = []
#         for event_id in event_ids:
#             # Checking that user is a participant in event
#             self.get_event_participant(event_id=event_id, user_id=user_id)
#
#             # Get event
#             event = EventModel.get_by_id(event_id=event_id)
#
#             if event is None:
#                 logger.warning(f'User {user_id} is trying to get a non-existent event {event_id}')
#                 raise error.APIValueNotFound(f'Event {event_id} not found for user {user_id}')
#
#             events.append(event)
#
#         logger.info(f'User {user_id} got events {event_ids}')
#
#         return events
