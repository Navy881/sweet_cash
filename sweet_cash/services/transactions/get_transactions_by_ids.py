import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transactions.enrich_transactions import EnrichTransactions
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_types import EventParticipantRole

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="transactions")


class GetTransactionsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_transactions: EnrichTransactions,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.enrich_transactions = enrich_transactions
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction_ids: str) -> List[TransactionModel]:
        transaction_ids: List[id] = ids2list(transaction_ids)
        result: List = []

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository.get_transactions(transaction_ids)

        for transaction in transactions:
            if transaction.user_id != self.user_id:
                users_roles: List[EventParticipantRole] = \
                    await self.get_event_participants_roles_for_user(event_id=transaction.event_id,
                                                                     user_id=self.user_id)
                if not any(role in users_roles for role in
                           [EventParticipantRole.MANAGER, EventParticipantRole.OBSERVER]):
                    continue

            result.append(transaction)

        result = await self.enrich_transactions(result)
        return result
