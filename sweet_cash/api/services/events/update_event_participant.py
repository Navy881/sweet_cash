
import logging

from api.services.base_service import BaseService
from api.repositories.users_repository import UsersRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_participants_types import (
    EventsParticipantsModel,
    UpdateEventsParticipantsModel,
    EventParticipantRole
)
from api.errors import APIConflict, APIValueNotFound, APIParamError


logger = logging.getLogger(name="events")


class UpdateEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_participant_id: int,
                       event_participants: UpdateEventsParticipantsModel) -> EventsParticipantsModel:
        async with self.events_participants_repository.transaction():
            # Checking participant exist
            event_participant: EventsParticipantsModel = await self.events_participants_repository.\
                get_events_participant_by_id(event_participant_id)

            event_id: int = event_participant.event_id

            # Checking that requests user is user from requests
            if self.user_id == event_participant.user_id:
                raise APIConflict(f'User {self.user_id} is trying to update his participant {event_participant_id}')

            # Checking that requests user is the event manager
            event_participant: EventsParticipantsModel = await self.events_participants_repository.\
                get_events_participant_by_role(user_id=self.user_id,
                                               event_id=event_id,
                                               role=EventParticipantRole('Manager'))

            if event_participant is None:
                raise APIValueNotFound(f'User {self.user_id} not associated with the events {event_id}')

            return await self.events_participants_repository.\
                update_events_participant(event_participant_id=event_participant_id,
                                          event_participant=event_participants)

# import logging
#
# from api.services.events.get_event_participant import GetEventParticipant
# from api.models.event_participants import EventParticipantsModel, EventParticipantRole
# import api.errors as error
#
# logger = logging.getLogger(name="events")
#
#
# class UpdateEventParticipant(object):
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> EventParticipantsModel:
#         user_id = kwargs.get("user_id")
#         event_id = kwargs.get("event_id")
#         participant_id = kwargs.get("participant_id")
#         role = kwargs.get("role")
#
#         if not EventParticipantRole.has_value(role):
#             logger.warning(f'User {user_id} is trying to create participant with invalid '
#                            f'role {role}')
#             raise error.APIParamError(f'Invalid participant role {role}')
#
#         # Checking that user is the event manager
#         self.get_event_participant(event_id=event_id,
#                                    user_id=user_id,
#                                    accepted=True,
#                                    role='Manager')
#
#         # Get event participant for user
#         participant = self.get_event_participant(participant_id=participant_id)
#
#         if participant.event_id != event_id:
#             logger.warning(f'User {user_id} is trying to update participant {participant_id} form other event')
#             raise error.APIParamError(f'Participant {participant_id} not in event {event_id}')
#
#         if participant.user_id == user_id:
#             logger.warning(f'User {user_id} is trying to update his participant {participant_id}')
#             raise error.APIConflict(f'You cannot update your participant')
#
#         participant.update(role=EventParticipantRole(role))
#
#         logger.info(f'User {user_id} update event {event_id} with role {participant.role}')
#
#         return participant
