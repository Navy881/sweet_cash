import logging
from typing import List

from sweet_cash.api.services.base_service import BaseService
from sweet_cash.api.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.api.repositories.transactions_repository import TransactionsRepository
from sweet_cash.api.types.transactions_types import TransactionModel
from sweet_cash.api.types.events_participants_types import EventParticipantRole
from sweet_cash.api.utils import ids2list


logger = logging.getLogger(name="transactions")


class GetTransactions(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction_ids: str) -> List[TransactionModel]:
        transaction_ids: List[id] = ids2list(transaction_ids)
        result: List = []

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository.get_transactions(transaction_ids)

        async with self.events_participants_repository.transaction():
            for transaction in transactions:
                if transaction.user_id != self.user_id:
                    if not await self.events_participants_repository. \
                            check_exist_events_participant_by_role(user_id=self.user_id,
                                                                   event_id=transaction.event_id,
                                                                   role=EventParticipantRole.MANAGER.name):
                        continue

                result.append(transaction)
            return result
