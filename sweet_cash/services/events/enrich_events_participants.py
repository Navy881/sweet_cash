import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.users_types import UserModel
from sweet_cash.types.events_types import EventsParticipantsModel


logger = logging.getLogger(name="transactions")


class EnrichEventsParticipants(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.events_repository = events_repository

    async def __call__(self, events_participants: List[EventsParticipantsModel]):
        user_ids = {participant.user_id for participant in events_participants}
        users: Dict[int, UserModel] = await self.get_users_by_ids(list(user_ids))

        for participant in events_participants:
            participant.user = users.get(participant.user_id)
