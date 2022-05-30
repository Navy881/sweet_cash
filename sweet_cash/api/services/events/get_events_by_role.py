
import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_types import EventModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from api.errors import APIParamError

logger = logging.getLogger(name="events")


class GetEventsByRole(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository

    async def __call__(self, roles: str) -> List[EventModel]:
        roles: List[EventParticipantRole] = self._roles2list(roles)

        async with self.events_participants_repository.transaction():
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_with_role(user_id=self.user_id, roles=roles)
        available_events_ids = [events_participant.event_id for events_participant in events_participants]

        async with self.events_repository.transaction():
            return await self.events_repository.get_events(event_ids=available_events_ids)

    @staticmethod
    def _roles2list(roles: str):
        if roles is None:
            return None

        roles_list = []
        roles_split = roles.split(',')

        for role in roles_split:
            try:
                if not EventParticipantRole.has_value(role):
                    raise APIParamError(f'Invalid participant role {role}')

                roles_list.append(EventParticipantRole(role))
            except ValueError:
                continue

        return roles_list


# import logging
#
# from api.models.event import EventModel
# from api.models.event_participants import EventParticipantsModel, EventParticipantRole
# import api.errors as error
#
# logger = logging.getLogger(name="events")
#
#
# class GetEventsByFilter(object):
#
#     @staticmethod
#     def _roles2list(roles: str):
#
#         if roles is None:
#             return None
#
#         roles_list = []
#
#         roles_split = roles.split(',')
#
#         for role in roles_split:
#
#             if not EventParticipantRole.has_value(role):
#                 raise error.APIParamError(f'Invalid participant role {role}')
#
#             roles_list.append(EventParticipantRole(role))
#
#         return roles_list
#
#     def __call__(self, **kwargs) -> [EventModel]:
#         user_id = kwargs.get("user_id")
#         roles = self._roles2list(kwargs.get("role"))
#         accepted = kwargs.get("accepted")
#
#         # Get event participants
#         if roles is not None:
#             # Get accepted participants for roles
#             participants = EventParticipantsModel.get_by_user_role(user_id=user_id, roles=roles)
#         else:
#             participants = EventParticipantsModel.get_by_user(user_id=user_id, accepted=accepted)
#
#         # Get event_ids from participants
#         event_ids = []
#         for participant in participants:
#             event_ids.append(participant.event_id)
#
#         # Get all existing events
#         events = EventModel.get_by_ids(event_ids=event_ids)
#
#         logger.info(f'User {user_id} got events')
#
#         return events
