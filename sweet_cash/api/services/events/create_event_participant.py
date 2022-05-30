import logging

from api.services.base_service import BaseService
from api.repositories.users_repository import UsersRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_participants_types import (
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    EventParticipantRole
)
from api.errors import APIValueNotFound, APIParamError

logger = logging.getLogger(name="events")


class CreateEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 users_repository: UsersRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.users_repository = users_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int,
                       event_participants: CreateEventsParticipantsModel) -> EventsParticipantsModel:
        user_id: int = event_participants.user_id
        role: EventParticipantRole = event_participants.role

        async with self.users_repository.transaction():
            # Checking user from requests exist
            await self.users_repository.get_by_id(user_id)

        async with self.events_participants_repository.transaction():
            # Checking that requests user is the event manager
            event_participant: EventsParticipantsModel = await self.events_participants_repository.\
                get_events_participant_by_role(user_id=self.user_id,
                                               event_id=event_id,
                                               role=EventParticipantRole('Manager'))

            if event_participant is None:
                raise APIValueNotFound(f'User {self.user_id} not associated with the events {event_id}')

            # Checking that user is not events participant
            event_participant: EventsParticipantsModel = await self.events_participants_repository.\
                get_events_participant_by_role(user_id=user_id,
                                               event_id=event_id,
                                               role=EventParticipantRole(role))

            if event_participant is not None:
                raise APIParamError(f'Participant for {user_id} already exist in event {event_id}')

            return await self.events_participants_repository.\
                create_events_participant(event_id=event_id, event_participant=event_participants)

# import logging
#
# from api.services.events.get_event_participant import GetEventParticipant
# from api.services.users.get_user import GetUser
# from api.models.event_participants import EventParticipantsModel, EventParticipantRole
# import api.errors as error
#
# logger = logging.getLogger(name="events")
#
#
# class CreateEventParticipant(object):
#     get_user = GetUser()
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> EventParticipantsModel:
#         request_user_id = kwargs.get("request_user_id")
#         user_id = kwargs.get("user_id")
#         event_id = kwargs.get("event_id")
#         role = kwargs.get("role")
#
#         if not EventParticipantRole.has_value(role):
#             logger.warning(f'User {user_id} is trying to create participant with invalid '
#                            f'role {role}')
#             raise error.APIParamError(f'Invalid participant role {role}')
#
#         # Checking user exist
#         self.get_user(user_id=user_id)
#
#         # Checking that user from request is the event manager
#         self.get_event_participant(event_id=event_id,
#                                    user_id=request_user_id,
#                                    accepted=True,
#                                    role='Manager')
#
#         # Checking that user is not event participant
#         participant = EventParticipantsModel.get_by_event_and_user(event_id=event_id, user_id=int(user_id))
#
#         if participant is not None:
#             logger.warning(f'User {request_user_id} is trying to create existing event participant {user_id} '
#                            f'from event {event_id}')
#             raise error.APIParamError(f'Participant for {user_id} already exist in event {event_id}')
#
#         participant = EventParticipantsModel(user_id=user_id,
#                                              event_id=event_id,
#                                              role=EventParticipantRole(role))
#
#         participant.create()
#
#         logger.info(f'User {user_id} added to event {event_id} with role {role}')
#
#         return participant
