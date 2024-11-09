import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_account_by_id import GetAccountById
from sweet_cash.services.account.get_available_account_by_id import GetAvailableAccountById
from sweet_cash.services.transaction_categories.get_transaction_category_by_id import GetTransactionCategoryBiId
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel, CreateTransactionModel, TransactionType
from sweet_cash.types.events_participants_types import EventParticipantRole


from sweet_cash.errors import APIValueNotFound, APIParamError


logger = logging.getLogger(name="transactions")


class CreateTransaction(BaseService):
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

    async def __call__(self, transaction: CreateTransactionModel) -> TransactionModel:
        event_id: int = transaction.event_id
        transaction_category_id: int = transaction.category_id

        # Checking exist transaction category
        await self.get_transaction_category_by_id(transaction_category_id)

        # Checking that user in event
        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

        if len(users_roles) == 0:
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        async with self.transactions_repository.transaction():
            transaction_model =  await self.transactions_repository.create_transaction(user_id=self.user_id,
                                                                                       transaction=transaction)

        transaction_model.user = await self.get_user_by_id(transaction_model.user_id)

        return transaction_model
    

class CreateTransactionV2(BaseService):
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

    async def __call__(self, transaction: CreateTransactionModel) -> TransactionModel:
        event_id: int = transaction.event_id
        transaction_category_id: int = transaction.category_id

        # Checking account value
        if transaction.type == TransactionType.EXPENSE and transaction.source_account_id is None:
            raise APIParamError("Field source_account_id should not be empty for expense transaction")
    
        if transaction.type == TransactionType.INCOME and transaction.target_account_id is None:
            raise APIParamError("Field target_account_id should not be empty for income transaction")

        # Проверка только по id, т.к. пользователь можно создавать 
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

        # Checking that user in event
        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

        if len(users_roles) == 0:
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        async with self.transactions_repository.transaction():
            transaction_model =  await self.transactions_repository.create_transaction(user_id=self.user_id,
                                                                                       transaction=transaction)
        # Update transactions user
        transaction_model.user = await self.get_user_by_id(transaction_model.user_id)

        # Update transactions accounts
        if self.source_account:
            transaction_model.source_account = await self.get_available_account_by_id(self.source_account.id)

        if self.target_account:
            transaction_model.target_account = await self.get_available_account_by_id(self.target_account.id)

        return transaction_model