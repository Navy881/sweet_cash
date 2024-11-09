import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_by_user_and_roles import GetEventParticipantsByUserAndRoles
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel, EventParticipantRole

from sweet_cash.errors import APIParamError


logger = logging.getLogger(name="events")


class GetEventsByRoles(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_by_user_and_roles: GetEventParticipantsByUserAndRoles,
                 get_event_participants_by_event: GetEventParticipantsByEvent,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_by_user_and_roles = get_event_participants_by_user_and_roles
        self.get_event_participants_by_event = get_event_participants_by_event
        self.events_repository = events_repository

    async def __call__(self, roles: str) -> List[EventModel]:
        roles: List[EventParticipantRole] = self._roles2list(roles)

        user_events_participants: List[EventsParticipantsModel] = \
            await self.get_event_participants_by_user_and_roles(user_id=self.user_id, roles=roles)

        available_events_ids = [events_participant.event_id for events_participant in user_events_participants]

        # Get events
        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository.get_events(event_ids=available_events_ids)

            # Addition events_participants for events
            for event in events:
                event.participants = await self.get_event_participants_by_event(event.id)

        return events

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
