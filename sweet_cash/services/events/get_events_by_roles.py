import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events import EnrichEvents

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import EventModel, EventParticipantRole

from sweet_cash.errors import APIParamError


logger = logging.getLogger(name="events")


class GetEventsByRoles(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_events: EnrichEvents,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.enrich_events = enrich_events
        self.events_repository = events_repository

    async def __call__(self, roles: str) -> List[EventModel]:
        roles: List[EventParticipantRole] = self._roles2list(roles)

        async with self.events_repository.transaction():
            events: List[EventModel] = await self.events_repository \
                .get_available_events_by_roles(user_id=self.user_id, roles=roles)

            await self.enrich_events(events)
        return events

    @staticmethod
    def _roles2list(roles: str):
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
