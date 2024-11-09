import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_available_account_by_id import GetAvailableAccountById
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_participants_types import EventParticipantRole

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="transactions")


class GetTransactionsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 get_available_account_by_id: GetAvailableAccountById,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.get_available_account_by_id = get_available_account_by_id
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

            # Update transactions user
            transaction.user = await self.get_user_by_id(transaction.user_id)

            # Update transactions accounts
            if transaction.source_account_id:
                transaction.source_account = await self.get_available_account_by_id(transaction.source_account_id)

            if transaction.target_account_id:
                transaction.target_account = await self.get_available_account_by_id(transaction.target_account_id)

            result.append(transaction)

        return result
