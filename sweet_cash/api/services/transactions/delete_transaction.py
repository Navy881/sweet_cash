import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.transactions_types import TransactionModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from api.errors import APIValueNotFound, APIConflict

logger = logging.getLogger(name="transactions")


class DeleteTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction_id: int) -> TransactionModel:
        async with self.transactions_repository.transaction():
            transaction: TransactionModel = await self.transactions_repository.get_transaction_by_id(transaction_id)
            event_id: int = transaction.event_id

            async with self.events_participants_repository.transaction():
                # Checking that user in event
                event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                    get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

                if len(event_participants) == 0:
                    raise APIValueNotFound(f'User {self.user_id} not associated with the event for transaction '
                                           f'{transaction_id}')

                if self.user_id != transaction.user_id:
                    if EventParticipantRole.MANAGER not in \
                            [event_participant.role for event_participant in event_participants]:
                        raise APIConflict(f'Updating a transaction {transaction_id} unavailable for user {self.user_id}')

                return await self.transactions_repository.delete_transaction(transaction_id)

# import logging
#
# from api.models.transaction import TransactionModel
# from api.models.event_participants import EventParticipantRole
# from api.services.transactions.get_transaction import GetTransactions
# from api.services.events.get_event_participant import GetEventParticipant
# import api.errors as error
#
# logger = logging.getLogger(name="transactions")
#
#
# class DeleteTransaction(object):
#     get_transactions = GetTransactions()
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, user_id: int, transaction_id: int) -> int:
#         # Get transaction
#         transaction = self.get_transactions(user_id=user_id, transaction_ids=[transaction_id])[0]
#
#         if transaction.user_id != user_id:
#             # Checking that user is a participant in event
#             participant = self.get_event_participant(event_id=transaction.event_id, user_id=user_id, accepted=True)
#             if participant.role != EventParticipantRole.MANAGER:
#                 logger.warning(f'User {user_id} is trying to update a unavailable transaction {transaction_id}')
#                 raise error.APIConflict(f'Deleting a transaction {transaction_id} unavailable for user {user_id}')
#
#         transaction_deleted_num = TransactionModel.delete_transaction(transaction_id=transaction_id)
#
#         if transaction_deleted_num > 0:
#             logger.info(f'User {user_id} deleted transaction {transaction_id}')
#
#         return transaction_deleted_num
