import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.transactions_types import TransactionModel, CreateTransactionModel
from api.types.events_participants_types import EventsParticipantsModel, EventParticipantRole

logger = logging.getLogger(name="transactions")


class GetAllTransactions(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository

    async def __call__(self, event_id: int, start: str, end: str, limit: int, offset: int) -> List[TransactionModel]:
        async with self.events_participants_repository.transaction():
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel]

            if len(event_participants) == 0:
                transactions = []

            elif EventsParticipantsModel.role.PARTNER in [event_participant.role for event_participant in
                                                          event_participants]:
                transactions = await self.transactions_repository.get_transactions_page(event_id=event_id,
                                                                                        start=start,
                                                                                        end=end,
                                                                                        user_id=self.user_id,
                                                                                        limit=limit,
                                                                                        offset=offset)

            else:
                transactions = await self.transactions_repository.get_transactions_page(event_id=event_id,
                                                                                        start=start,
                                                                                        end=end,
                                                                                        limit=limit,
                                                                                        offset=offset)

            return transactions

# import logging
#
# from api.models.transaction import TransactionModel
# from api.services.events.get_event_participant import GetEventParticipant
# from api.api import str2datetime
# import api.errors as error
#
# logger = logging.getLogger(name="transactions")
#
#
# class GetAllTransactions(object):
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> [TransactionModel]:
#         user_id = kwargs.get("user_id")
#         event_id = kwargs.get("event_id")
#         start = kwargs.get("start")
#         end = kwargs.get("end")
#         limit = kwargs.get("limit")
#         offset = kwargs.get("offset")
#
#         if start is not None and end is not None:
#             if str2datetime(start) > str2datetime(end):
#                 raise error.APIParamError(f'Start {start} must be less than End {end}')
#
#         # Checking that user is the event manager
#         participant = self.get_event_participant(event_id=event_id, user_id=user_id, accepted=True)
#
#         if participant.role == 'Partner':
#             transactions = TransactionModel.get_transactions_by_user_id(user_id=user_id,
#                                                                         start=start,
#                                                                         end=end,
#                                                                         limit=int(limit),
#                                                                         offset=int(offset))
#         else:
#             transactions = TransactionModel.get_transactions_by_event_id(event_id=event_id,
#                                                                          start=start,
#                                                                          end=end,
#                                                                          limit=int(limit),
#                                                                          offset=int(offset))
#
#         transactions = [t for t in transactions]
#
#         logger.info(f'User {user_id} got transactions')
#
#         return transactions
