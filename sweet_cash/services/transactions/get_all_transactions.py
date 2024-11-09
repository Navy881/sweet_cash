import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_available_account_by_id import GetAvailableAccountById
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_participants_types import EventParticipantRole


logger = logging.getLogger(name="transactions")


class GetAllTransactions(BaseService):
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

    async def __call__(self, event_id: int, start: str, end: str, limit: int, offset: int) -> List[TransactionModel]:
        transactions: List[TransactionModel]

        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

        async with self.transactions_repository.transaction():
            if EventParticipantRole.PARTNER in users_roles:
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

        # Update transactions user and accounts
        for i, transaction in enumerate(transactions):
            transactions[i].user = await self.get_user_by_id(transaction.user_id)

            if transaction.source_account_id:
                transactions[i].source_account = await self.get_available_account_by_id(transaction.source_account_id)

            if transaction.target_account_id:
                transactions[i].target_account = await self.get_available_account_by_id(transaction.target_account_id)

        return transactions
