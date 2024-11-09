import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_available_account_by_id import GetAvailableAccountById
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_participants_types import EventParticipantRole

from sweet_cash.errors import APIConflict, APIValueNotFound


logger = logging.getLogger(name="transactions")


class DeleteTransaction(BaseService):
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

    async def __call__(self, transaction_id: int) -> TransactionModel:
        async with self.transactions_repository.transaction():
            transaction = await self.transactions_repository.get_transaction_by_id(transaction_id)
            if transaction is None:
                raise APIValueNotFound(f'Transaction {transaction_id} not found')

            event_id: int = transaction.event_id

            if transaction.user_id != self.user_id:
                # Checking that user in event
                users_roles: List[EventParticipantRole] = \
                    await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

                if EventParticipantRole.MANAGER not in users_roles:
                    raise APIConflict(f'Updating a transaction {transaction_id} unavailable for user {self.user_id}')

            transaction = await self.transactions_repository.delete_transaction(transaction_id)
            
        # Update transactions user
        transaction.user = await self.get_user_by_id(transaction.user_id)

        # Update transactions accounts
        if transaction.source_account_id:
            transaction.source_account = await self.get_available_account_by_id(transaction.source_account_id)

        if transaction.target_account_id:
            transaction.target_account = await self.get_available_account_by_id(transaction.target_account_id)

        return transaction
