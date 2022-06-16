import logging
from typing import List

from sweet_cash.api.services.base_service import BaseService
from sweet_cash.api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.api.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.api.repositories.transactions_repository import TransactionsRepository
from sweet_cash.api.types.transactions_types import TransactionModel, CreateTransactionModel
from sweet_cash.api.types.events_participants_types import EventsParticipantsModel
from sweet_cash.api.errors import APIValueNotFound


logger = logging.getLogger(name="transactions")


class CreateTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_repository = transaction_categories_repository
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction: CreateTransactionModel) -> TransactionModel:
        event_id: int = transaction.event_id
        transaction_category_id: int = transaction.category_id

        async with self.transaction_categories_repository.transaction():
            # Checking exist transaction category
            await self.transaction_categories_repository.get_transaction_category_by_id(transaction_category_id)

        async with self.events_participants_repository.transaction():
            # Checking that user in event
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository.\
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

            if len(event_participants) == 0:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

        async with self.transactions_repository.transaction():
            return await self.transactions_repository.create_transaction(user_id=self.user_id,
                                                                         transaction=transaction)
