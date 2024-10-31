
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.transactions_repository import TransactionsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.types.transactions_types import TransactionModel, CreateTransactionModel, TransactionType
from sweet_cash.types.events_participants_types import EventsParticipantsModel
from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.types.accounts_types import AccountModel, AccountResponseModel
from sweet_cash.errors import APIValueNotFound, APIParamError


logger = logging.getLogger(name="transactions")


class CreateTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository,
                 user_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_repository = transaction_categories_repository
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository
        self.user_repository = user_repository

    async def __call__(self, transaction: CreateTransactionModel) -> TransactionModel:
        event_id: int = transaction.event_id
        transaction_category_id: int = transaction.category_id
        
        # Checking exist transaction category
        async with self.transaction_categories_repository.transaction():
            await self.transaction_categories_repository.get_transaction_category_by_id(transaction_category_id)

        # Checking that user in event
        async with self.events_participants_repository.transaction():
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

            if len(event_participants) == 0:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        async with self.transactions_repository.transaction():
            transaction_model =  await self.transactions_repository.create_transaction(user_id=self.user_id,
                                                                                       transaction=transaction)
        
        async with self.user_repository.transaction():
            user = await self.user_repository.get_by_id(transaction_model.user_id)
            transaction_model.user = UserResponseModel(**user.dict())

        return transaction_model
    

class CreateTransactionV2(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository,
                 user_repository: UsersRepository,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_repository = transaction_categories_repository
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository
        self.user_repository = user_repository
        self.accounts_repository = accounts_repository
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
        
        # Checking exist accounts
        # Проверка только по id, т.к. пользователь можно создавать 
        # транзкации со счётом, к которому у него нет доступа
        async with self.accounts_repository.transaction():
            if transaction.source_account_id is not None:
                self.source_account = await self.accounts_repository.get_by_id(account_id=transaction.source_account_id)
                if self.source_account is None:
                    raise APIValueNotFound(f'Account {transaction.source_account_id} not found')
                
            if transaction.target_account_id is not None:
                self.target_account = await self.accounts_repository.get_by_id(account_id=transaction.target_account_id)
                if self.target_account is None:
                    raise APIValueNotFound(f'Account {transaction.target_account_id} not found')

        # Checking exist transaction category
        async with self.transaction_categories_repository.transaction():
            await self.transaction_categories_repository.get_transaction_category_by_id(transaction_category_id)

        # Checking that user in event
        async with self.events_participants_repository.transaction():
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

            if len(event_participants) == 0:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        async with self.transactions_repository.transaction():
            transaction_model =  await self.transactions_repository.create_transaction(user_id=self.user_id,
                                                                                       transaction=transaction)
        # Update transactions user
        async with self.user_repository.transaction():
            user = await self.user_repository.get_by_id(transaction_model.user_id)
            transaction_model.user = UserResponseModel(**user.dict())

        # Update transactions accounts
        if self.source_account:
            if self.source_account.user_id == self.user_id:
                transaction_model.source_account = AccountResponseModel(**self.source_account.dict())
            else:
                transaction_model.source_account = AccountResponseModel(id=self.source_account.id)
        
        if self.target_account:
            if self.target_account.user_id == self.user_id:
                transaction_model.target_account = AccountResponseModel(**self.target_account.dict())
            else:
                transaction_model.target_account = AccountResponseModel(id=self.target_account.id)

        return transaction_model