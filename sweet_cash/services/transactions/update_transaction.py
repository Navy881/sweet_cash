import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_account_by_id import GetAccountById
from sweet_cash.services.account.get_available_account_by_id import GetAvailableAccountById
from sweet_cash.services.transaction_categories.get_transaction_category_by_id import GetTransactionCategoryBiId
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import (
    TransactionModel,
    TransactionType,
    UpdateTransactionModel
)
from sweet_cash.types.events_participants_types import EventParticipantRole

from sweet_cash.errors import APIValueNotFound, APIParamError


logger = logging.getLogger(name="transactions")


class UpdateTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 get_available_account_by_id: GetAvailableAccountById,
                 get_transaction_category_by_id: GetTransactionCategoryBiId,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.get_available_account_by_id = get_available_account_by_id
        self.get_transaction_category_by_id = get_transaction_category_by_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction_id: int, transaction: UpdateTransactionModel) -> TransactionModel:
        transaction_category_id: int = transaction.category_id

        # Checking exist transaction category
        await self.get_transaction_category_by_id(transaction_category_id)

        async with self.transactions_repository.transaction():
            transaction_ = await self.transactions_repository.get_transaction_by_id(transaction_id)
            if transaction_ is None:
                raise APIValueNotFound(f'Transaction {transaction_id} not found')

            event_id: int = transaction_.event_id

            if transaction_.user_id != self.user_id:
                # Checking that user in event
                users_roles: List[EventParticipantRole] = \
                    await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

                if EventParticipantRole.MANAGER not in users_roles:
                    raise APIValueNotFound(f'User {self.user_id} cannot change the transaction {transaction_id}')

            transaction_ = await self.transactions_repository.update_transaction(transaction_id=transaction_id,
                                                                                 transaction=transaction)

            # Update transactions user
            transaction_.user = await self.get_user_by_id(transaction_.user_id)

            return transaction_
        

class UpdateTransactionV2(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 get_account_by_id: GetAccountById,
                 get_available_account_by_id: GetAvailableAccountById,
                 get_transaction_category_by_id: GetTransactionCategoryBiId,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.get_account_by_id = get_account_by_id
        self.get_available_account_by_id = get_available_account_by_id
        self.get_transaction_category_by_id = get_transaction_category_by_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.transactions_repository = transactions_repository
        self.source_account = None
        self.target_account = None

    async def __call__(self, transaction_id: int, transaction: UpdateTransactionModel) -> TransactionModel:
        transaction_category_id: int = transaction.category_id

        # Checking account value
        if transaction.type == TransactionType.EXPENSE and transaction.source_account_id is None:
            raise APIParamError("Field source_account_id should not be empty for expense transaction")
    
        if transaction.type == TransactionType.INCOME and transaction.target_account_id is None:
            raise APIParamError("Field target_account_id should not be empty for income transaction")
        
        # Checking exist accounts
        # Проверка только по id, т.к. пользователь можно изменять 
        # транзкации со счётом, к которому у него нет доступа
        if transaction.source_account_id is not None:
            self.source_account = await self.get_account_by_id(transaction.source_account_id)
            if self.source_account is None:
                raise APIValueNotFound(f'Account {transaction.source_account_id} not found')

        if transaction.target_account_id is not None:
            self.target_account = await self.get_account_by_id(transaction.target_account_id)
            if self.target_account is None:
                raise APIValueNotFound(f'Account {transaction.target_account_id} not found')

        # Checking exist transaction category
        await self.get_transaction_category_by_id(transaction_category_id)

        async with self.transactions_repository.transaction():
            # Checking access to transaction
            transaction_model = await self.transactions_repository.get_transaction_by_id(transaction_id)
            if transaction_model is None:
                raise APIValueNotFound(f'Transaction {transaction_id} not found')

            event_id: int = transaction_model.event_id

            if transaction_model.user_id != self.user_id:
                # Checking that user in event
                users_roles: List[EventParticipantRole] = \
                    await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

                if EventParticipantRole.MANAGER not in users_roles:
                    raise APIValueNotFound(f'User {self.user_id} cannot change the transaction {transaction_id}')
                    
            transaction_model = await self.transactions_repository.update_transaction(transaction_id=transaction_id,
                                                                                      transaction=transaction)

        # Update transactions user
        transaction_model.user = await self.get_user_by_id(transaction_model.user_id)

        # Update transactions accounts
        if self.source_account:
            transaction_model.source_account = await self.get_available_account_by_id(self.source_account.id)

        if self.target_account:
            transaction_model.target_account = await self.get_available_account_by_id(self.target_account.id)

        return transaction_model