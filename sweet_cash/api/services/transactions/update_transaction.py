import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.transactions_types import TransactionModel, CreateTransactionModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from api.errors import APIValueNotFound, APIConflict

logger = logging.getLogger(name="transactions")


class UpdateTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_repository = transaction_categories_repository
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction_id: int, transaction: CreateTransactionModel) -> TransactionModel:
        transaction_category_id: int = transaction.category_id

        async with self.transaction_categories_repository.transaction():
            # Checking exist transaction category
            await self.transaction_categories_repository.get_transaction_category_by_id(transaction_category_id)

        async with self.transactions_repository.transaction():
            transaction_: TransactionModel = await self.transactions_repository.get_transaction_by_id(transaction_id)
            event_id: int = transaction_.event_id

            async with self.events_participants_repository.transaction():
                # Checking that user in event
                event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                    get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

                if len(event_participants) == 0:
                    raise APIValueNotFound(f'User {self.user_id} not associated with the event for transaction '
                                           f'{transaction_id}')

            if self.user_id != transaction_.user_id:
                if EventParticipantRole.MANAGER not in \
                        [event_participant.role for event_participant in event_participants]:
                    raise APIConflict(f'Updating a transaction {transaction_id} unavailable for user {self.user_id}')

            return await self.transactions_repository.update_transaction(transaction_id=transaction_id,
                                                                         transaction=transaction)


# import logging
#
# from api.models.transaction import TransactionModel, TransactionType
# from api.models.transaction_category import TransactionCategoryModel
# from api.models.event_participants import EventParticipantRole
# from api.services.transactions.get_transaction import GetTransactions
# from api.services.events.get_event_participant import GetEventParticipant
# from api.services.receipts.get_receipt import GetReceipt
# import api.errors as error
# from config import Config
#
#
# logger = logging.getLogger(name="events")
#
#
# class UpdateTransaction(object):
#     get_transactions = GetTransactions()
#     get_event_participant = GetEventParticipant()
#     get_receipt = GetReceipt()
#
#     def __call__(self, **kwargs) -> TransactionModel:
#         user_id = kwargs.get("user_id")
#         transaction_id = kwargs.get("transaction_id")
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
#         if receipt_id is not None:
#             self.get_receipt(receipt_id=receipt_id, user_id=user_id)
#
#         # Get transaction
#         transaction = self.get_transactions(user_id=user_id, transaction_ids=[transaction_id])[0]
#
#         if transaction.user_id != user_id:
#             # Checking that user is a participant in event
#             participant = self.get_event_participant(event_id=transaction.event_id, user_id=user_id, accepted=True)
#             if participant.role != EventParticipantRole.MANAGER:
#                 logger.warning(f'User {user_id} is trying to update a unavailable transaction {transaction_id}')
#                 raise error.APIConflict(f'Updating a transaction {transaction_id} unavailable for user {user_id}')
#
#         transaction.update(transaction_date=transaction_date,
#                            type=TransactionType(transactions_type),
#                            category=transactions_category_id,
#                            amount=amount,
#                            receipt_id=receipt_id,
#                            description=description)
#
#         logger.info(f'User {user_id} updated transaction {transaction.id}')
#
#         return transaction
