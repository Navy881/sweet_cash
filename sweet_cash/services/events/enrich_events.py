import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.users_types import UserModel
from sweet_cash.types.events_types import EventModel


logger = logging.getLogger(name="transactions")


class EnrichEvents(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.events_repository = events_repository

    async def __call__(self, events: List[EventModel]):
        user_ids = {participant.user_id for event in events if event.participants for participant in event.participants}
        users: Dict[int, UserModel] = await self.get_users_by_ids(list(user_ids))

        for event in events:
            if event.participants:
                for participant in event.participants:
                    participant.user = users.get(participant.user_id)


        # event_ids = [event.id for event in events]
        #
        # async with self.events_repository.transaction():
        #     participants: List[EventsParticipantsModel] = await self.events_repository.\
        #         get_events_participants_by_event_ids(event_ids=event_ids)
        #
        # user_ids = [participant.user_id for participant in participants]
        #
        # users: Dict[int, UserModel] = await self.get_users_by_ids(
        #     list(set(user_ids))
        # )
        #
        # for event in events:
        #     if not event.participants:
        #         event.participants = []
        #
        #     for participant in participants:
        #         try:
        #             participant.user = users[participant.user_id]
        #         except KeyError:
        #             participant.user = None
        #         if participant.event_id == event.id:
        #             event.participants.append(participant)
        #
        # return events
