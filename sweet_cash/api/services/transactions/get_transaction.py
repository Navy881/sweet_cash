import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.transactions_types import TransactionModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from api.api import ids2list


logger = logging.getLogger(name="categories")


class GetTransactions(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, transaction_ids: str) -> List[TransactionModel]:
        transaction_ids: List[id] = ids2list(transaction_ids)
        result: List = []

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository.get_transactions(transaction_ids)

        async with self.events_participants_repository.transaction():
            for transaction in transactions:
                if transaction.user_id != self.user_id:
                    event_participant: EventsParticipantsModel = await self.events_participants_repository. \
                        get_events_participant_by_role(user_id=self.user_id,
                                                       event_id=transaction.event_id,
                                                       role=EventParticipantRole.MANAGER)
                    if event_participant is None:
                        continue

                result.append(transaction)
            return result

# import logging
#
# from api.models.transaction import TransactionModel
# from api.models.event_participants import EventParticipantRole
# from api.services.events.get_event_participant import GetEventParticipant
# from api.api import ids2list
# import api.errors as error
#
# logger = logging.getLogger(name="transactions")
#
#
# class GetTransactions(object):
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> [TransactionModel]:
#         user_id = kwargs.get("user_id")
#         transaction_ids = ids2list(kwargs.get("transaction_ids"))
#
#         transactions = []
#         for transaction_id in transaction_ids:
#
#             transaction = TransactionModel.get_by_id(transaction_id=transaction_id)
#
#             if transaction is None:
#                 logger.warning(f'User {user_id} is trying to get a non-existent transaction {transaction_id}')
#                 raise error.APIValueNotFound(f'Transaction {transaction_id} not found for user {user_id}')
#
#             if transaction.user_id != user_id:
#                 # Checking that user is a participant in event
#                 participant = self.get_event_participant(event_id=transaction.event_id, user_id=user_id, accepted=True)
#                 if participant.role == EventParticipantRole.PARTNER:
#                     logger.warning(f'User {user_id} is trying to get a unavailable transaction {transaction_id}')
#                     raise error.APIConflict(f'Transaction {transaction_id} unavailable for user {user_id}')
#
#             transactions.append(transaction)
#
#         logger.info(f'User {user_id} got transactions')
#
#         return transactions
