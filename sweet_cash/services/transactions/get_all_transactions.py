import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transactions.enrich_transactions import EnrichTransactions
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_types import EventParticipantRole
from sweet_cash.errors import APIParamError


logger = logging.getLogger(name="transactions")


class GetAllTransactions(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_transactions: EnrichTransactions,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.enrich_transactions = enrich_transactions
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.transactions_repository = transactions_repository

    async def __call__(self, event_id: int, start: str, end: str, limit: int, offset: int) -> List[TransactionModel]:
        if limit > 100:
            raise APIParamError(f'Limit value must be less than or equal to 100')

        transactions: List[TransactionModel]

        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

        async with self.transactions_repository.transaction():
            if EventParticipantRole.PARTNER in users_roles:
                transactions: List[TransactionModel] = await self.transactions_repository. \
                    get_transactions_page(event_id=event_id,
                                          start=start,
                                          end=end,
                                          user_id=self.user_id,
                                          limit=limit,
                                          offset=offset)

            else:
                transactions: List[TransactionModel] = await self.transactions_repository. \
                    get_transactions_page(event_id=event_id,
                                          start=start,
                                          end=end,
                                          limit=limit,
                                          offset=offset)

            result = await self.enrich_transactions(transactions)
            return result
