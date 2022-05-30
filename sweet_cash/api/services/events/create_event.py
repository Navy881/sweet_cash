import logging

from api.services.base_service import BaseService
from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_types import EventModel, CreateEventModel
from api.types.events_participants_types import CreateEventsParticipantsModel

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
            event = await self.events_repository.create_event(event)

        async with self.events_participants_repository.transaction():
            event_participant: CreateEventsParticipantsModel = CreateEventsParticipantsModel()
            event_participant.user_id = self.user_id
            event_participant.role = 'Manager'

            events_participant = await self.events_participants_repository.\
                create_events_participant(event_id=event.id, event_participant=event_participant)

            await self.events_participants_repository.accept_events_participant(
                events_participant_id=events_participant.id)

            event.participants = await self.events_participants_repository.\
                get_events_participants_by_event_id(event_id=event.id)
        return event

# import logging
#
# from api.models.event import EventModel
# from api.models.event_participants import EventParticipantsModel, EventParticipantRole
# from api.services.events.create_event_participant import CreateEventParticipant
# from api.services.events.confirm_event_participant import ConfirmEventParticipant
# from api.api import str2datetime
# import api.errors as error
#
# logger = logging.getLogger(name="events")
#
#
# class CreateEvent(object):
#     create_participant = CreateEventParticipant()
#     confirm_participant = ConfirmEventParticipant()
#
#     def __call__(self, **kwargs) -> EventModel:
#         user_id = kwargs.get("user_id")
#         name = kwargs.get("name")
#         start = kwargs.get("start")
#         end = kwargs.get("end")
#         description = kwargs.get("description")
#
#         if start is not None and end is not None:
#             if str2datetime(start) > str2datetime(end):
#                 raise error.APIParamError(f'Start {start} must be less than End {end}')
#
#         event = EventModel(name=name,
#                            start=start,
#                            end=end,
#                            description=description)
#
#         event.create()
#
#         event_id = event.get_id()
#
#         # Create first participant for event
#         participant = EventParticipantsModel(user_id=user_id,
#                                              event_id=event_id,
#                                              role=EventParticipantRole("Manager"))
#
#         participant.create()
#
#         # Confirm participant
#         self.confirm_participant(user_id=user_id, event_id=event_id)
#
#         logger.info(f'User {user_id} created event {event_id}')
#
#         return event
