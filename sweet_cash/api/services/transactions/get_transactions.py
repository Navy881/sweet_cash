import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.transactions_types import TransactionModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole

logger = logging.getLogger(name="transactions")


class GetAllTransactions(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, event_id: int, start: str, end: str, limit: int, offset: int) -> List[TransactionModel]:
        async with self.events_participants_repository.transaction():
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel]

            if len(event_participants) == 0:
                transactions = []

            elif EventParticipantRole.PARTNER in [event_participant.role for event_participant in event_participants]:
                transactions: List[TransactionModel] = await self.transactions_repository. \
                    get_transactions_page(event_id=event_id,
                                          start=start,
                                          end=end,
                                          user_id=self.user_id,
                                          limit=limit,
                                          offset=offset)

            else:
                transactions: List[TransactionModel] = await self.transactions_repository. \
                    get_transactions_page(event_id=event_id,
                                          start=start,
                                          end=end,
                                          limit=limit,
                                          offset=offset)

            return transactions
