
import logging

from api.services.base_service import BaseService
from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_types import EventModel, CreateEventModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from api.errors import APIValueNotFound

logger = logging.getLogger(name="events")


class UpdateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int, event: CreateEventModel) -> EventModel:
        async with self.events_participants_repository.transaction():
            events_participant: EventsParticipantsModel = await self.events_participants_repository.\
                get_events_participant_by_role(user_id=self.user_id,
                                               event_id=event_id,
                                               role=EventParticipantRole('Manager'))

            if events_participant is None:
                raise APIValueNotFound(f'User {self.user_id} not associated with the events {event_id}')

        async with self.events_repository.transaction():
            return await self.events_repository.update_event(event_id=event_id, event=event)


# import logging
#
# from api.services.events.get_events import GetEvents
# from api.services.events.get_event_participant import GetEventParticipant
# from api.models.event import EventModel
# from api.api import str2datetime
# import api.errors as error
#
# logger = logging.getLogger(name="events")
#
#
# class UpdateEvent(object):
#     get_events = GetEvents()
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> EventModel:
#         user_id = kwargs.get("user_id")
#         event_id = kwargs.get("event_id")
#         name = kwargs.get("name")
#         start = kwargs.get("start")
#         end = kwargs.get("end")
#         description = kwargs.get("description")
#
#         if start is not None and end is not None:
#             if str2datetime(start) > str2datetime(end):
#                 raise error.APIParamError(f'Start {start} must be less than End {end}')
#
#         # Get event
#         event = self.get_events(user_id=user_id, event_ids=[event_id])[0]
#
#         # Checking that user is the event manager
#         self.get_event_participant(event_id=event_id,
#                                    user_id=user_id,
#                                    accepted=True,
#                                    role='Manager')
#
#         event.update(name=name,
#                      start=start,
#                      end=end,
#                      description=description)
#
#         logger.info(f'User {user_id} updated event {event.id}')
#
#         return event
