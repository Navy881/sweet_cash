import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.transactions_types import TransactionModel, CreateTransactionModel
from api.types.events_participants_types import EventsParticipantsModel
from api.errors import APIValueNotFound

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
                raise APIValueNotFound(f'User {self.user_id} not associated with the events {event_id}')

        async with self.transactions_repository.transaction():
            return await self.transactions_repository.create_transaction(transaction)


# import logging
#
# from api.models.transaction_category import TransactionCategoryModel
# from api.services.events.get_event_participant import GetEventParticipant
# from api.services.receipts.get_receipt import GetReceipt
# from api.models.transaction import TransactionModel, TransactionType
# from config import Config
# import api.errors as error
#
# logger = logging.getLogger(name="transactions")
#
#
# class CreateTransaction(object):
#     get_event_participant = GetEventParticipant()
#     get_receipt = GetReceipt()
#
#     def __call__(self, **kwargs) -> TransactionModel:
#         user_id = kwargs.get("user_id")
#         event_id = kwargs.get("event_id")
#         transaction_date = kwargs.get("transaction_date")
#         transactions_type = kwargs.get("type")
#         transactions_category_id = kwargs.get("category_id")
#         amount = kwargs.get("amount")
#         receipt_id = kwargs.get("receipt_id")
#         description = kwargs.get("description")
#
#         if amount < Config.MIN_TRANSACTION_AMOUNT or amount > Config.MAX_TRANSACTION_AMOUNT:
#             logger.warning(f'User {user_id} is trying to create transaction with invalid amount {amount}')
#             raise error.APIParamError(f'Amount must be from {Config.MIN_TRANSACTION_AMOUNT} '
#                                       f'to {Config.MAX_TRANSACTION_AMOUNT}')
#
#         if not TransactionType.has_value(transactions_type):
#             logger.warning(f'User {user_id} is trying to create transaction with invalid '
#                            f'type {transactions_type}')
#             raise error.APIParamError(f'Invalid transaction type {transactions_type}')
#
#         # TODO old Проверять категорию через сервис
#         transactions_category = TransactionCategoryModel.get_by_id(category_id=transactions_category_id)
#         if transactions_category is None:
#             logger.warning(f'User {user_id} is trying to create transaction with a non-existent'
#                            f'category {transactions_category_id}')
#             raise error.APIValueNotFound(f'Transaction category with id {transactions_category_id} not found')
#
#         self.get_event_participant(event_id=event_id, user_id=user_id, accepted=True)
#
#         if receipt_id is not None:
#             self.get_receipt(receipt_id=receipt_id, user_id=user_id)
#
#         transaction = TransactionModel(user_id=user_id,
#                                        event_id=event_id,
#                                        transaction_date=transaction_date,
#                                        type=TransactionType(transactions_type),
#                                        category=transactions_category_id,
#                                        amount=amount,
#                                        receipt_id=receipt_id,
#                                        description=description)
#
#         transaction.create()
#
#         logger.info(f'User {user_id} created transaction {transaction.id}')
#
#         return transaction
