import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository

from sweet_cash.types.events_participants_types import EventsParticipantsModel
from sweet_cash.types.users_types import UserModel

logger = logging.getLogger(name="events")


class GetEventParticipantsByEvent(BaseService):
    def __init__(self, user_id: int,
                 get_user_by_id: GetUserById,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int) -> List[EventsParticipantsModel]:
        event_participants: List[EventsParticipantsModel]

        async with self.events_participants_repository.transaction():
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_event(event_id=event_id, accepted=True)

        user: UserModel = await self.get_user_by_id(self.user_id)
        for event_participant in event_participants:
            event_participant.user = user

        return event_participants